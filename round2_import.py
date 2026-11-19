"""Delphi Round 2 — import of the Microsoft Forms exports (one .xlsx per form version).

What it does (Stage 2 plan A1–A3, A8, E-C1 and amendment 1; instrument record round2-instrument-as-fielded.md):
  1. reads each version's export and checks that its header row has the structure of the form as built:
     metadata columns, 3 profile questions, then 3 scenario sections of 15 questions each;
  2. maps every row to a panellist code through a separate, non-published key (panel-key.json) and removes the
     researcher's own test rows;
  3. maps each scenario section to its scenario through the file's version (Latin square A/B/C), which is the order
     the respondent saw. It stops if no respondent in a file is assigned to that file's version (a mislabelled
     export), and flags any single respondent who answered a version other than the one assigned;
  4. resolves duplicate rows by a value-blind rule (amendment 1): the row on the assigned version wins, then the
     latest completion time; the others are excluded and reported;
  5. validates every value, codes the carbon question (engine.exploratory.code_carbon_answer), and runs A1 and the
     A3 consistency check (engine.bwm, with amendment 1);
  6. if the researcher's own test row names, in each rationale field, the scenario heading seen ("Regulated finance",
     "High-growth start-up", "Sustainability" or S1/S2/S3), checks that the export's section order matches the
     version; a mismatch stops the import;
  7. writes round2-responses.json (data; codes only, no names) and a Markdown report.

The report shows counts and flags only: no ratings, weights, best/worst choices or carbon answers. Error messages
never echo the respondent's value, so the report can be read without seeing the panel's priorities.

Usage (from this folder):
  python round2_import.py --A <export A.xlsx> --B <export B.xlsx> --C <export C.xlsx>
  options: --key panel-key.json  --out round2-responses.json  --report round2-import-report.md
           --include-researcher      keep the researcher's rows as TEST1, TEST2, ... (to check parsing)
           --allow-version-mismatch  import a file even if none of its respondents is assigned to its version
           --corrections corrections.json  apply panellists' own written corrections (amendment 3)
A version without an export can be left out."""
import argparse, datetime, hashlib, json, os, re, sys, unicodedata
import numpy as np
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'engine'))
from engine import CRITERIA                                   # noqa: E402  ['TTDP','AIRD','PORT','TCO','SECC']
from engine.bwm import BWMResponse, evaluate                  # noqa: E402
from engine.exploratory import code_carbon_answer             # noqa: E402

VERSIONS = {'A': ['S1', 'S2', 'S3'], 'B': ['S2', 'S3', 'S1'], 'C': ['S3', 'S1', 'S2']}
OPTION_TEXT = ['TTDP — Time-to-data-product', 'AIRD — AI and GenAI readiness', 'PORT — Portability and lock-in',
               'TCO — Total cost of ownership', 'SECC — Security and compliance']
EMAIL_HEADERS = {'email', 'e-mail', 'почта', 'электронная почта', 'електронна пошта', 'пошта'}
NAME_HEADERS = {'name', 'имя', "ім'я", 'імя'}
PROFILE = {
    'role': ('Your current role', ['Data / Solution / Enterprise Architect', 'Lead or Principal Data Engineer',
                                   'Head of Data, Data Platform or Analytics']),           # plus free-text Other
    'experience': ('Years of experience in data architecture or data platform engineering',
                   ['Less than 3 years', '3 to less than 5 years', '5 to 10 years', 'More than 10 years']),
    'participation': ('Have you personally taken part in a decision to select a data platform or to migrate to one?',
                      ['No', 'Yes, as a contributor to the evaluation', 'Yes, as the decision owner or co-owner']),
}
A8_EXPERIENCE = {'5 to 10 years', 'More than 10 years'}
A8_PARTICIPATION = {'Yes, as a contributor to the evaluation', 'Yes, as the decision owner or co-owner'}
SCENARIO_MARKERS = {'S1': ['s1', 'regulated finance', 'nordbank', 'finance'],
                    'S2': ['s2', 'start-up', 'startup', 'flowlytics', 'high-growth'],
                    'S3': ['s3', 'sustainability', 'veridia']}
MOST = 'For this organisation, which criterion is the MOST important?'
LEAST = 'For this organisation, which criterion is the LEAST important?'


class ImportError_(Exception):
    pass


def _norm(text):
    """Lower-case word tokens with diacritics removed; Latin and Cyrillic letters kept."""
    t = unicodedata.normalize('NFKD', str(text or '').lower())
    t = ''.join(ch for ch in t if not unicodedata.combining(ch))
    return set(re.findall(r'[^\W\d_]+', t))


def _base(header):
    """Header without the numeric suffix Forms appends to repeated question texts ('…2', '…3')."""
    return re.sub(r'\d+$', '', str(header or '').strip()).strip()


def parse_layout(headers):
    """Locate every column the import needs and check the structure. Returns a dict of column indices."""
    h = [_base(x) for x in headers]
    low = [x.lower() for x in h]
    lay = {'id': 0, 'completed': 2}
    email = [i for i, x in enumerate(low) if x in EMAIL_HEADERS]
    name = [i for i, x in enumerate(low) if x in NAME_HEADERS]
    lay['email'] = email[0] if email else 3          # Forms' fixed position when the header language is unknown
    lay['name'] = name[0] if name else 4
    for key, (text, _) in PROFILE.items():
        idx = [i for i, x in enumerate(h) if x.startswith(text)]
        if len(idx) != 1:
            raise ImportError_(f'profile question not found exactly once: {text!r}')
        lay[key] = idx[0]
    if min(lay['role'], lay['experience'], lay['participation']) <= max(lay['email'], lay['name']):
        raise ImportError_('identity columns not found before the profile questions')
    starts = [i for i, x in enumerate(h) if x == MOST]
    if len(starts) != 3:
        raise ImportError_(f'expected 3 scenario sections, found {len(starts)}')
    sections = []
    for s in starts:
        if s + 15 > len(h):
            raise ImportError_(f'section starting at column {s + 1} is truncated')
        sec = {'best': s, 'worst': s + 1, 'bo': list(range(s + 2, s + 7)), 'ow': list(range(s + 7, s + 12)),
               'rationale': s + 12, 'carbon_dir': s + 13, 'carbon_k': s + 14}
        problems = []
        if h[s + 1] != LEAST:
            problems.append('LEAST question not directly after MOST')
        for j, c in enumerate(CRITERIA):
            if not h[s + 2 + j].startswith(f'… than {c} —'):
                problems.append(f'best-to-others column {j + 1} is not {c}')
            if not (h[s + 7 + j].startswith(f'{c} —') and h[s + 7 + j].endswith('than my least important')):
                problems.append(f'others-to-worst column {j + 1} is not {c}')
        if not h[s + 12].startswith('What drove your ranking'):
            problems.append('rationale question not in place')
        if not h[s + 13].startswith('One more question about this organisation. Carbon intensity'):
            problems.append('carbon direction question not in place')
        if not h[s + 14].startswith('By how much?'):
            problems.append('carbon strength question not in place')
        if problems:
            raise ImportError_(f'section starting at column {s + 1}: ' + '; '.join(problems))
        sections.append(sec)
    lay['sections'] = sections
    return lay


def _criterion(value, what):
    """Exact match to one of the five option texts. The error message never contains the value."""
    v = str(value).strip() if value is not None else ''
    if v not in OPTION_TEXT:
        raise ValueError(f'{what} answer missing or not exactly one of the five options')
    return OPTION_TEXT.index(v)


def _rating(v, what):
    try:
        if v is None or isinstance(v, bool) or (isinstance(v, str) and not v.strip()):
            raise ValueError
        f = float(v)
        if f != int(f) or not 1 <= int(f) <= 9:
            raise ValueError
        return int(f)
    except (ValueError, TypeError, OverflowError):
        raise ValueError(f'{what}: rating missing or not an integer 1..9') from None


def match_code(name, email, key):
    """Returns a panel code, 'RESEARCHER', None (no unique match) or 'CONFLICT' (researcher and panellist)."""
    e = str(email or '').strip().lower()
    tokens = _norm(name) | _norm(e.split('@')[0].replace('_', ' ').replace('.', ' ').replace('-', ' '))
    researcher = bool(tokens & {t for v in key['researcher'] for t in _norm(v)})
    hits = []
    for code, p in key['panel'].items():
        if e and e in [x.strip().lower() for x in p.get('emails', [])]:
            hits.append(code); continue
        first = {t for v in p.get('first_names', []) for t in _norm(v)}
        last = {t for v in p['surnames'] for t in _norm(v)}
        if tokens & first and tokens & last:
            hits.append(code)
    if researcher and hits:
        return 'CONFLICT'
    if researcher:
        return 'RESEARCHER'
    return hits[0] if len(hits) == 1 else None


def read_export(path):
    ws = openpyxl.load_workbook(path, data_only=True).worksheets[0]   # not read_only: Forms files lack dimensions
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        raise ImportError_(f'{os.path.basename(path)}: empty file')
    body = [(n, r) for n, r in enumerate(rows[1:], start=2) if any(v not in (None, '') for v in r)]
    return list(rows[0]), body


def _marker(text):
    """Scenario named in a researcher's rationale field (order check), or None."""
    t = str(text or '').strip().lower()
    hits = [sc for sc, words in SCENARIO_MARKERS.items() if any(re.search(rf'(?<![a-z0-9]){re.escape(w)}(?![a-z0-9])', t) for w in words)]
    return hits[0] if len(hits) == 1 else None


def order_check(r, lay, version):
    """If the researcher wrote the scenario heading seen into each rationale field, compare it with the version's
    order. Returns None (no markers), True (all three agree) or a list of disagreements."""
    seen = [_marker(r[sec['rationale']]) for sec in lay['sections']]
    if not any(seen):
        return None
    bad = [f'section {k + 1}: marked {m}, expected {e}' for k, (m, e) in enumerate(zip(seen, VERSIONS[version])) if m != e]
    return True if not bad else bad


def _sha256(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def _record(r, lay, version, assigned):
    comp = r[lay['completed']]
    rec = {'version_answered': version, 'version_assigned': assigned, 'wrong_version': assigned != version,
           'response_id': r[lay['id']],
           'completed': comp.isoformat() if isinstance(comp, datetime.datetime) else str(comp),
           'profile': {}, 'scenarios': {}, 'problems': []}
    for k, (_, options) in PROFILE.items():
        v = r[lay[k]]
        v = None if v is None or not str(v).strip() else str(v).strip()
        if v is None:
            rec['problems'].append(f'profile {k} missing')
        elif k != 'role' and v not in options:
            rec['problems'].append(f'profile {k}: answer is not one of the options')
            v = None
        rec['profile'][k] = v
    p = rec['profile']
    p['role_other'] = p['role'] is not None and p['role'] not in PROFILE['role'][1]
    p['A8_qualified'] = None if (p['experience'] is None or p['participation'] is None) else \
        (p['experience'] in A8_EXPERIENCE and p['participation'] in A8_PARTICIPATION)
    p['A8_participation_only'] = None if p['participation'] is None else p['participation'] in A8_PARTICIPATION
    for pos, (sec, scen) in enumerate(zip(lay['sections'], VERSIONS[version]), start=1):
        s = {'position': pos, 'valid': False}
        # carbon question first, so that it is kept even when the BWM part is invalid
        try:
            k = _rating(r[sec['carbon_k']], 'carbon strength')
            a, consistent = code_carbon_answer(r[sec['carbon_dir']], k)
            s['carbon'] = {'direction': str(r[sec['carbon_dir']]).strip(), 'rating': k, 'a': a, 'consistent': consistent}
        except ValueError:
            s['carbon'] = None
            rec['problems'].append(f'{scen}: carbon answer missing or not one of the options')
        s['rationale'] = str(r[sec['rationale']]).strip() if r[sec['rationale']] not in (None, '') else None
        try:
            best = _criterion(r[sec['best']], 'MOST')
            worst = _criterion(r[sec['worst']], 'LEAST')
            bo = np.array([_rating(r[i], f'best-to-others {c}') for i, c in zip(sec['bo'], CRITERIA)], float)
            ow = np.array([_rating(r[i], f'others-to-worst {c}') for i, c in zip(sec['ow'], CRITERIA)], float)
        except ValueError as e:
            rec['problems'].append(f'{scen}: {e}')
            rec['scenarios'][scen] = s
            continue
        ev = evaluate(BWMResponse(best, worst, bo, ow))
        s.update({'valid': True, 'best': CRITERIA[best], 'worst': CRITERIA[worst],
                  'bo': dict(zip(CRITERIA, bo.astype(int).tolist())), 'ow': dict(zip(CRITERIA, ow.astype(int).tolist())),
                  'A1': {'passed': ev['attention_ok'], 'reasons': ev['attention_reasons']},
                  'A3': {'consistent': ev['consistent'], 'rule': ev['threshold_rule'],
                         'recontact_criterion': None if ev['consistent'] else CRITERIA[ev['recontact_pair']]}})
        rec['scenarios'][scen] = s
    return rec


def import_versions(files, key, include_researcher=False, allow_version_mismatch=False):
    """files: {'A': path, ...}. Returns (data, report). Raises ImportError_ on structural problems."""
    candidates, excluded, problems, file_info, n_test = {}, [], [], {}, 0
    for version, path in sorted(files.items()):
        headers, body = read_export(path)
        lay = parse_layout(headers)
        file_info[version] = {'file': os.path.basename(path), 'sha256': _sha256(path), 'rows': len(body)}
        matched_assigned = []
        for rownum, r in body:
            where = f'{version}: sheet row {rownum}'
            code = match_code(r[lay['name']], r[lay['email']], key)
            if code == 'CONFLICT':
                excluded.append({'where': where, 'reason': 'matches both the researcher and a panellist'})
                problems.append(f'{where}: matches both the researcher and a panellist — resolve in panel-key.json')
                continue
            if code == 'RESEARCHER':
                oc = order_check(r, lay, version)
                if oc is not None:
                    file_info[version]['order_check'] = 'passed' if oc is True else oc
                    if oc is not True and not allow_version_mismatch:
                        raise ImportError_(f'version {version}: section order check failed ({"; ".join(oc)}); '
                                           'the export order does not match the version, or the file is mislabelled')
                if not include_researcher:
                    excluded.append({'where': where, 'reason': "researcher's own test response"})
                    continue
                n_test += 1
                code = f'TEST{n_test}'
            if code is None:
                excluded.append({'where': where, 'reason': 'not matched to exactly one panel code'})
                problems.append(f'{where}: unmatched respondent — add a name variant or e-mail to panel-key.json')
                continue
            assigned = key['panel'].get(code, {}).get('version', version)
            matched_assigned.append(assigned)
            rec = _record(r, lay, version, assigned)
            rec['_where'] = where
            candidates.setdefault(code, []).append(rec)
        real = [a for a in matched_assigned]
        if real and version not in real and not allow_version_mismatch:
            raise ImportError_(f'file given as version {version} has no respondent assigned to {version}; '
                               'it is probably a different version\'s export (override: --allow-version-mismatch)')
    respondents = {}
    for code, recs in candidates.items():
        recs.sort(key=lambda x: (not x['wrong_version'], x['completed']), reverse=True)  # assigned first, then latest
        keep, drop = recs[0], recs[1:]
        for d in drop:
            excluded.append({'where': d['_where'], 'reason': f'duplicate row for {code}; kept {keep["_where"]} '
                                                            '(rule: assigned version first, then latest completion)'})
            problems.append(f'{d["_where"]}: duplicate for {code}, not used')
        keep.pop('_where')
        respondents[code] = keep
    data = {'_source': 'Microsoft Forms exports of Round 2; imported by round2_import.py. Codes only; the key to '
                       'names is kept separately.',
            '_criteria_order': CRITERIA, '_versions': VERSIONS, '_files': file_info,
            '_imported': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
            'respondents': respondents, 'excluded_rows': excluded}
    return data, {'problems': problems}


def apply_corrections(data, corrections):
    """Panellists' own written corrections of the comparison blocks (Stage 2 plan, amendment 3, point 6).
    Replaces the two vectors of one scenario response, keeps the first submission under 'first_submission', and
    re-runs A1 and A3. MOST and LEAST are not changed: a correction that does not give 1 to that response's MOST
    criterion in block 1 and to its LEAST criterion in block 2 is rejected, since it cannot be matched to it.
    corrections: [{'code', 'scenario', 'bo': {criterion: rating}, 'ow': {...}, 'source', 'recorded', 'evidence'?}]"""
    applied = []
    for c in corrections:
        code, scen = c['code'], c['scenario']
        r = data['respondents'].get(code)
        s = r['scenarios'].get(scen) if r else None
        if not s or not s.get('valid'):
            raise ImportError_(f'correction for {code} {scen}: no parsed response to correct')
        try:
            bo = np.array([_rating(c['bo'][k], f'correction block 1 {k}') for k in CRITERIA], float)
            ow = np.array([_rating(c['ow'][k], f'correction block 2 {k}') for k in CRITERIA], float)
        except (KeyError, ValueError) as e:
            raise ImportError_(f'correction for {code} {scen}: {e}') from None
        b, w = CRITERIA.index(s['best']), CRITERIA.index(s['worst'])
        if bo[b] != 1 or ow[w] != 1:
            raise ImportError_(f'correction for {code} {scen} does not match the MOST and LEAST choices of that response')
        ev = evaluate(BWMResponse(b, w, bo, ow))
        s['first_submission'] = {k: s[k] for k in ('bo', 'ow', 'A1', 'A3')}
        s.update({'bo': dict(zip(CRITERIA, bo.astype(int).tolist())), 'ow': dict(zip(CRITERIA, ow.astype(int).tolist())),
                  'A1': {'passed': ev['attention_ok'], 'reasons': ev['attention_reasons']},
                  'A3': {'consistent': ev['consistent'], 'rule': ev['threshold_rule'],
                         'recontact_criterion': None if ev['consistent'] else CRITERIA[ev['recontact_pair']]},
                  'correction': {k: c.get(k) for k in ('source', 'recorded', 'evidence')}})
        applied.append({'code': code, 'scenario': scen, 'source': c['source'], 'recorded': c['recorded']})
    data['corrections_applied'] = applied
    return data


def load_responses(data, scenario, a1_passed_only=False):
    """Hand-off to the engine: [(code, BWMResponse)] for one scenario, criteria in engine order. The A1 filter is
    applied by pipeline.weights_stage; a1_passed_only is for inspection only."""
    out = []
    for code, r in sorted(data['respondents'].items()):
        s = r['scenarios'].get(scenario)
        if not s or not s.get('valid') or (a1_passed_only and not s['A1']['passed']):
            continue
        out.append((code, BWMResponse(CRITERIA.index(s['best']), CRITERIA.index(s['worst']),
                                      np.array([s['bo'][c] for c in CRITERIA], float),
                                      np.array([s['ow'][c] for c in CRITERIA], float))))
    return out


def report_md(data, rep):
    R = data['respondents']
    files = ', '.join(f"{v}: {i['file']} ({i['rows']} rows, sha256 {i['sha256'][:12]}…, section order check: "
                      f"{i.get('order_check', 'not available')})" for v, i in sorted(data['_files'].items()))
    lines = ['# Round 2 — import report', '',
             f"Imported {data['_imported']}. Files: {files or 'none'}.", '',
             'Counts and flags only — no ratings, weights, best/worst choices or carbon answers.', '',
             f'**Respondents imported:** {len(R)} ({", ".join(sorted(R)) or "none"}). '
             f'**Rows excluded:** {len(data["excluded_rows"])}.', '']
    for e in data['excluded_rows']:
        lines.append(f'- excluded {e["where"]}: {e["reason"]}')
    lines += ['', '| Code | Version answered / assigned | Profile complete | A8 qualified | A1 failures | A3 above threshold | Problems |',
              '|---|---|---|---|---|---|---|']
    for code, r in sorted(R.items()):
        sc = sorted(r['scenarios'].items())
        a1 = [f'{s}: ' + '; '.join(v['A1']['reasons']) for s, v in sc if v.get('valid') and not v['A1']['passed']]
        a3 = [f"{s} ({'a_BW = 2' if v['A3']['rule'].startswith('a_BW = 2') else 'table' if v['A3']['rule'] == 'table' else 'a_BW = 1'};"
              f" recontact on {v['A3']['recontact_criterion']})" for s, v in sc if v.get('valid') and not v['A3']['consistent']]
        prof_ok = all(r['profile'][k] is not None for k in PROFILE)
        lines.append(f"| {code} | {r['version_answered']} / {r['version_assigned']}{' **(wrong link)**' if r['wrong_version'] else ''} "
                     f"| {'yes' if prof_ok else '**no**'} | {r['profile']['A8_qualified']} | {'<br>'.join(a1) or '—'} "
                     f"| {'<br>'.join(a3) or '—'} | {'<br>'.join(r['problems']) or '—'} |")
    if rep['problems']:
        lines += ['', '**Import problems:**'] + [f'- {p}' for p in rep['problems']]
    if data.get('corrections_applied'):
        lines += ['', '**Corrections applied** (panellists\' own, in writing; values not shown):'] + \
                 [f"- {c['code']} {c['scenario']}: {c['source']} (recorded {c['recorded']})" for c in data['corrections_applied']]
    per = {}
    for s in ['S1', 'S2', 'S3']:
        vals = [r['scenarios'].get(s, {}) for r in R.values()]
        per[s] = (sum(1 for v in vals if v.get('valid') and v['A1']['passed']),
                  sum(1 for v in vals if v.get('carbon') and not v['carbon']['consistent']))
    lines += ['', '**Per scenario:** ' + '; '.join(f'{s}: {a} valid and passing A1, {c} inconsistent carbon answers'
                                                   for s, (a, c) in per.items()) +
              '. Minimum for SMAA: 5 valid responses per scenario.', '',
              '**Next.** No recontacts are made (Stage 2 amendment 3). A panellist\'s own written correction is applied '
              'with --corrections and listed above; the first submission is kept in the data file.']
    return '\n'.join(lines) + '\n'


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    for v in VERSIONS:
        ap.add_argument(f'--{v}', help=f'export of version {v}')
    ap.add_argument('--key', default=os.path.join(HERE, 'panel-key.json'))
    ap.add_argument('--out', default=os.path.join(HERE, 'round2-responses.json'))
    ap.add_argument('--report', default=os.path.join(HERE, 'round2-import-report.md'))
    ap.add_argument('--include-researcher', action='store_true')
    ap.add_argument('--allow-version-mismatch', action='store_true')
    ap.add_argument('--corrections', help="JSON file of panellists' own written corrections (amendment 3)")
    a = ap.parse_args(argv)
    files = {v: getattr(a, v) for v in VERSIONS if getattr(a, v)}
    if not files:
        ap.error('give at least one export')
    key = json.load(open(a.key, encoding='utf-8'))
    try:
        data, rep = import_versions(files, key, a.include_researcher, a.allow_version_mismatch)
        if a.corrections:
            apply_corrections(data, json.load(open(a.corrections, encoding='utf-8'))['corrections'])
    except ImportError_ as e:
        sys.exit(f'IMPORT STOPPED: {e}')
    json.dump(data, open(a.out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    md = report_md(data, rep)
    open(a.report, 'w', encoding='utf-8').write(md)
    print(md)


if __name__ == '__main__':
    main()
