"""Delphi Round 1 analysis — applies the Stage 1 analysis plan (rules R1-R10) mechanically.

Input : round1-responses.json (transcribed from the MS Forms results; researcher's test submission removed)
Output: round1-results.json, round1-results.md

The coding of open answers (R4-R7) is a researcher judgement. It is recorded in CODING below, one
line per answer, so that it can be published and checked (Stage 1 plan, R4: "The coding of every A7
response is published").

Checks NOT in the plan are labelled 'data-quality check' or 'sensitivity' and never change a decision.
"""
import json, itertools
import numpy as np
from scipy.stats import spearmanr

D = json.load(open('round1-responses.json'))
IDS = D['respondents']
CRIT = ['CARB', 'TTDP', 'AIRD', 'PORT', 'TCO', 'SECC']
N = len(IDS)

# ---------------------------------------------------------------- quartiles
# The plan does not fix a quartile definition. With n = 6 the definitions differ, so every
# definition in common use is computed and any decision that depends on the choice is flagged.
def tukey_hinges(x):
    x = np.sort(x); n = len(x); h = (n + 1) // 2
    return float(np.median(x[:h])), float(np.median(x[n - h:]))

QMETHODS = {
    'type7 (R/numpy default)': lambda x: tuple(np.percentile(x, [25, 75], method='linear')),
    'type6 (SPSS/Minitab)':    lambda x: tuple(np.percentile(x, [25, 75], method='weibull')),
    'type8 (Hyndman-Fan rec.)': lambda x: tuple(np.percentile(x, [25, 75], method='median_unbiased')),
    'Tukey hinges':            tukey_hinges,
}
PRIMARY_Q = 'type7 (R/numpy default)'

def r2_decision(med, iqr):
    if med >= 4.0:
        return 'Retained' if iqr <= 1.0 else 'Retained, contested'
    if med >= 3.0:
        return 'Retained, definition reviewed'
    return 'EXCLUDED from Round 2'

# ---------------------------------------------------------------- Part A treatments
# Primary: data as recorded (the plan has no rule for suspected scale reversal).
# Sensitivity: R05 reversed (6 - x) and R05 excluded — see the data-quality check.
def partA(treatment):
    out = {}
    for c in CRIT:
        rel = np.array(D['partA'][c]['relevance'], float); cla = np.array(D['partA'][c]['clarity'], float)
        if treatment == 'R05 reversed':
            i = IDS.index('R05'); rel[i] = 6 - rel[i]; cla[i] = 6 - cla[i]
        elif treatment == 'R05 excluded':
            keep = [k for k, r in enumerate(IDS) if r != 'R05']; rel, cla = rel[keep], cla[keep]
        out[c] = (rel, cla)
    return out

TREATMENTS = ['as recorded', 'R05 reversed', 'R05 excluded']
import platform, sys, datetime, scipy
R = {'environment': {'python': sys.version.split()[0], 'numpy': np.__version__, 'scipy': scipy.__version__,
                     'platform': platform.platform(),
                     'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')},
     'n_respondents': N, 'excluded_submissions': D['excluded']}

# R1 — completeness
R['R1'] = {'items_per_response': 12, 'excluded_from_R2_R3': 0,
           'note': 'All six responses complete on Part A.'}

# R2, R3
R['R2_R3'] = {}
for t in TREATMENTS:
    data = partA(t); rows = {}
    for c in CRIT:
        rel, cla = data[c]
        med = float(np.median(rel))
        per_method = {}
        for m, f in QMETHODS.items():
            q1, q3 = f(rel); per_method[m] = {'IQR': round(q3 - q1, 2), 'decision': r2_decision(med, q3 - q1)}
        decisions = {v['decision'] for v in per_method.values()}
        rows[c] = {
            'relevance': rel.astype(int).tolist(), 'median_relevance': med,
            'IQR_primary': per_method[PRIMARY_Q]['IQR'], 'R2_decision': per_method[PRIMARY_Q]['decision'],
            'R2_depends_on_quartile_method': len(decisions) > 1, 'R2_by_method': per_method,
            'clarity': cla.astype(int).tolist(), 'median_clarity': float(np.median(cla)),
            'R3_revise_definition': float(np.median(cla)) < 4.0,
        }
    R['R2_R3'][t] = rows

# data-quality check: agreement of each respondent's relevance profile with the others' medians
dq = {}
for k, r in enumerate(IDS):
    own = [D['partA'][c]['relevance'][k] for c in CRIT]
    others = [np.median([v for j, v in enumerate(D['partA'][c]['relevance']) if j != k]) for c in CRIT]
    rho = spearmanr(own, others).statistic
    rev = spearmanr([6 - x for x in own], others).statistic
    cla = [D['partA'][c]['clarity'][k] for c in CRIT]
    dq[r] = {'spearman_with_others_median': round(float(rho), 2),
             'spearman_if_reversed': round(float(rev), 2),
             'clarity_straightlined': len(set(cla)) == 1}
R['data_quality_check'] = dq

# ---------------------------------------------------------------- coding of open answers
# Pre-specified construct list (R4): GF Governance Friction; CLTR Cognitive Load and Talent Risk;
# DCQA Data Contract and Quality Accountability; DS Data Sovereignty. Anything else is NEW.
CODING = {
    'A7': {
        'R02': (['NEW:Operational reliability', 'CLTR'],
                'Primary: pipeline success rate, freshness SLA. Secondary: talent availability (time-to-hire) = CLTR.'),
        'R04': (['NEW:Operational reliability'], 'Availability/SLA, recovery time, RPO/RTO, incident frequency.'),
        'R05': (['NEW:Platform-partner ecosystem'], 'Solution shape set by the chosen platform partner.'),
        'R06': ([], 'Not a criterion: reads as a proposed trade-off question (30% lower TCO vs 30% shorter TTDP).'),
    },
    'A8': {
        'R02': ([('TTDP', 'TCO'), ('AIRD', 'SECC')], 'People cost; governed machine-readable catalogue access.'),
        'R04': ([('PORT', 'TCO')], 'Migration/exit cost in both.'),
        'R06': ([('PORT', 'TCO')], 'Migration effort and proprietary dependencies create future cost.'),
    },
    'A9': {
        'R02': ([('AIRD', 'SECC')], 'AI value conditional on governance. "TTDP trades off against Security" is a '
                                    'performance trade-off, not preferential dependence: not counted.'),
        'R04': ([('AIRD', 'TTDP'), ('PORT', 'TCO')], 'AI value higher under delivery pressure; portability matters more when long-term cost is high.'),
        'R06': ([('PORT', 'TCO')], 'Portability matters more when long-term cost or switching exposure is high.'),
    },
    'B2': {
        'R02': (['Hybrid / multi-platform'], 'Lakehouse core + warehouse serving layer, or Snowflake and Databricks coexisting.'),
        'R03': ([], 'Not a configuration: proposes a criterion (team expertise / ease of staffing) = CLTR.'),
        'R04': (['Hybrid / multi-platform'], 'Both technologies used deliberately; sometimes multi-cloud.'),
        'R05': ([], 'Not a configuration: organisational politics.'),
        'R06': (['Hybrid / multi-platform'], 'Hybrid architecture is the main configuration seen.'),
    },
    'C4': {
        'R02': (['Regulated scale-up'], 'Small team, high AI ambition, strict PHI/HIPAA.'),
        'R04': (['Legacy-heavy enterprise in modernisation'], 'Legacy, existing investment, migration risk.'),
        'R06': (['Legacy-heavy enterprise in modernisation'], 'Tight budget, legacy, no dominant driver.'),
    },
}
# Mentions outside A7 that name a criterion construct (reported, not counted under R4, which covers A7 only)
OUTSIDE_A7 = {'R03 (B2)': 'CLTR', 'R05 (B2)': 'NEW:Organisational politics'}

def count(field):
    c = {}
    for r, (codes, _) in CODING[field].items():
        for code in set(codes):
            key = ' – '.join(code) if isinstance(code, tuple) else code
            c.setdefault(key, []).append(r)
    return dict(sorted(c.items(), key=lambda kv: -len(kv[1])))

a7 = count('A7')
R['R4'] = {'counts_A7': {k: len(v) for k, v in a7.items()}, 'who': a7,
           'readmitted': [k for k, v in a7.items() if len(v) >= 3],
           'outside_A7_not_counted': OUTSIDE_A7,
           'counts_if_all_open_fields_were_counted': {'NEW:Operational reliability': 2, 'CLTR': 2,
                                                      'NEW:Platform-partner ecosystem': 1, 'NEW:Organisational politics': 1}}
a8, a9 = count('A8'), count('A9')
R['R5'] = {'counts': {k: len(v) for k, v in a8.items()}, 'triggered': [k for k, v in a8.items() if len(v) >= 3]}
R['R6'] = {'counts': {k: len(v) for k, v in a9.items()}, 'triggered': [k for k, v in a9.items() if len(v) >= 3]}

# R7 — configurations
b1 = D['B1_coverage']; b2 = count('B2')
share_b1 = sum(x in ('Yes, fully', 'Mostly') for x in b1) / N
R['R7'] = {'B1': {x: b1.count(x) for x in ['Yes, fully', 'Mostly', 'Partly', 'No']},
           'B1_share_fully_or_mostly': round(share_b1, 3), 'configuration_set_review': share_b1 < 0.5,
           'B2_counts': {k: len(v) for k, v in b2.items()},
           'B2_considered_for_addition': [k for k, v in b2.items() if len(v) >= 3]}
for q, e in (('B3_separation', 'E1'), ('B4_middle_row', 'E2')):
    v = D[q]; share = sum(x in ('Yes', 'Partly') for x in v) / N
    R[e] = {q: {x: v.count(x) for x in ['Yes', 'Partly', 'No']}, 'share_yes_or_partly': round(share, 3),
            'met': share > 0.5, 'share_yes': round(v.count('Yes') / N, 3)}

# R8 — manipulation check
INTENDED = {'S1': ['SECC'], 'S2': ['TTDP', 'AIRD'], 'S3': ['CARB']}
R['R8'] = {}
for s, d in D['scenarios'].items():
    sel = {c: sum(c in e for e in d['emphasis']) / N for c in CRIT}
    best_intended = max(sel[c] for c in INTENDED[s])
    no_share = d['realistic'].count('No') / N
    R['R8'][s] = {'emphasis_share': {c: round(v, 3) for c, v in sorted(sel.items(), key=lambda kv: -kv[1])},
                  'intended': INTENDED[s], 'intended_share': round(best_intended, 3),
                  'realism': {x: d['realistic'].count(x) for x in ['Yes', 'Mostly', 'No']},
                  'no_share': round(no_share, 3),
                  'passes': best_intended >= 0.6 and no_share < 0.3}
R['C4'] = {k: len(v) for k, v in count('C4').items()}

# R10 — assignment. Shown first as written in the plan, then as amended (Stage 1 amendment 7):
# with n = 6 the written rule cannot reach its target, so every panellist rates all three scenarios.
cs = dict(zip(IDS, D['closest_scenario']))
own = {s: list(cs.values()).count(s) for s in ['S1', 'S2', 'S3']}
load, second = dict(own), {}
for r in IDS:                                          # as written: own + least-loaded other scenario
    opts = sorted([s for s in load if s != cs[r]], key=lambda s: (load[s], s))
    second[r] = opts[0]; load[opts[0]] += 1
# As amended: everyone rates all three scenarios. Order follows a 3 x 3 Latin square, so that each
# scenario appears in each position equally often (2 panellists per form version); a panellist is put
# on the version that opens with their own scenario while that version has room.
VERSIONS = {'A': ['S1', 'S2', 'S3'], 'B': ['S2', 'S3', 'S1'], 'C': ['S3', 'S1', 'S2']}
cap = {v: N // 3 for v in VERSIONS}; version = {}
for r in sorted(IDS, key=lambda r: (own[cs[r]], r)):   # rarest own scenario first, then by ID
    pref = [v for v in VERSIONS if VERSIONS[v][0] == cs[r] and cap[v] > 0]
    v = pref[0] if pref else next(v for v in VERSIONS if cap[v] > 0)
    version[r] = v; cap[v] -= 1
order = {r: VERSIONS[version[r]] for r in IDS}
position = {s: [sum(order[r][p] == s for r in IDS) for p in range(3)] for s in VERSIONS['A']}
R['R10'] = {'closest': cs, 'closest_counts': own,
            'as_written': {'second': second, 'raters_per_scenario': load,
                           'target_8_per_scenario_met': min(load.values()) >= 8},
            'as_amended': {'all_rate_all_three': True, 'raters_per_scenario': {s: N for s in own},
                           'form_version': version, 'presentation_order': order,
                           'times_in_position_1_2_3': position}}
R['other_comment'] = D.get('other_comment')

json.dump(R, open('round1-results.json', 'w'), indent=2, default=lambda o: o.tolist() if hasattr(o, 'tolist') else str(o))

# ---------------------------------------------------------------- markdown summary
L = ['# Round 1 — results under the Stage 1 rules (generated by round1_analysis.py)', '',
     f'n = {N} (researcher\'s test submission removed). Quartiles: {PRIMARY_Q}; other definitions checked.', '',
     '## R2 / R3 — criteria', '',
     '| Criterion | Relevance | Median | IQR | R2 decision | Method-dependent? | Clarity median | R3 revise? | R2 if R05 reversed | R2 if R05 excluded |',
     '|---|---|---|---|---|---|---|---|---|---|']
for c in CRIT:
    a = R['R2_R3']['as recorded'][c]; b = R['R2_R3']['R05 reversed'][c]; x = R['R2_R3']['R05 excluded'][c]
    L.append(f"| {c} | {a['relevance']} | {a['median_relevance']} | {a['IQR_primary']} | {a['R2_decision']} | "
             f"{'yes' if a['R2_depends_on_quartile_method'] else 'no'} | {a['median_clarity']} | {'yes' if a['R3_revise_definition'] else 'no'} | "
             f"{b['R2_decision']} (clarity {b['median_clarity']}) | {x['R2_decision']} (clarity {x['median_clarity']}) |")
L += ['', '## Data-quality check (not a plan rule)', '', '| Respondent | ρ with others\' medians | ρ if reversed | Clarity straight-lined |', '|---|---|---|---|']
for r, v in dq.items():
    L.append(f"| {r} | {v['spearman_with_others_median']} | {v['spearman_if_reversed']} | {v['clarity_straightlined']} |")
L += ['', '## R4–R7, R8', '', f"R4 A7 counts: {R['R4']['counts_A7']} → re-admitted: {R['R4']['readmitted'] or 'none'}",
      f"R5 overlap counts: {R['R5']['counts']} → triggered: {R['R5']['triggered'] or 'none'}",
      f"R6 dependence counts: {R['R6']['counts']} → triggered: {R['R6']['triggered'] or 'none'}",
      f"R7 B1 fully/mostly: {R['R7']['B1_share_fully_or_mostly']} → review: {R['R7']['configuration_set_review']}; "
      f"B2 counts {R['R7']['B2_counts']} → considered for addition: {R['R7']['B2_considered_for_addition']}",
      f"E1 (B3 yes/partly): {R['E1']['share_yes_or_partly']} met={R['E1']['met']}; E2 (B4): {R['E2']['share_yes_or_partly']} met={R['E2']['met']}", '']
for s, v in R['R8'].items():
    L.append(f"R8 {s}: intended {v['intended']} selected by {v['intended_share']:.0%}; No-realism {v['no_share']:.0%} → "
             f"{'PASS' if v['passes'] else 'FAIL'}; emphasis {v['emphasis_share']}")
L += ['', f"R10: {R['R10']}"]
open('round1-results.md', 'w').write('\n'.join(L) + '\n')
print('\n'.join(L))
