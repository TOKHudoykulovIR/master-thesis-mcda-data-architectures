"""
CARB draft estimate — Software Carbon Intensity (ISO/IEC 21031): SCI = (E*I + M) / R
Thesis: multi-criteria framework for data-architecture configurations C1–C7.
Status: v0.2 (29 Sep 2026). Region (AWS eu-central-1) and workload scale (5 TB) set on the technical
supervisor's advice. Overrides for checks: env CARB_DATA_TB, CARB_GRID='lo,hi', CARB_OUT (file prefix).
v0.2 adds S7 (provisioning floor sized for BI concurrency): C1-vs-C2 checks S7a-c and joint draws for all
configurations (npz key R2_floor) for the Stage 2 A14 sensitivity run. Primary draws (R1, R2, R3) unchanged.

Every number below carries a source ID (see carb-assumptions.md). Ranges are sampled
uniformly (Monte Carlo); the output feeds SMAA as ranges, never as point values (kit K1).
"""
import numpy as np, csv, json, sys, os
rng = np.random.default_rng(20260926)
N = 10_000
U = lambda lo, hi: rng.uniform(lo, hi, N)

# ---------------- PARAMETERS (pending confirmation) ----------------
DATA_TB           = float(os.environ.get('CARB_DATA_TB', 5))   # P1 managed data volume (TB) — 5 TB per technical supervisor
DAYS              = 365 * 3     # 3-year horizon
DATA_PRODUCTS     = 20          # for R3 (same for every configuration)
W_TB_EQ_PER_DAY   = DATA_TB * U(0.2, 0.6)   # A1 daily work = 20–60% of managed data, in TPC-DS-power-run TB-equivalents
ELT_SHARE         = U(0.3, 0.6) # A2 share of daily work that is the ELT pipeline run (R1)

# ---------------- COEFFICIENTS ----------------
W_MIN, W_MAX = 0.74, 3.5        # CCF AWS avg min/max W per vCPU            [CCF-1]
UTIL          = U(0.3, 0.8)     # A3 CPU utilisation during runs (CCF default 0.5)
MEM_KWH_GBH   = 0.000392        # CCF memory kWh per GB-hour                [CCF-2]
HDD_WH_TBH    = 0.65            # CCF HDD Wh per TB-hour (object storage)   [CCF-3]
S3_REPL       = 3               # A4 object-storage replication factor (≥3 AZs)
PUE           = 1.135           # CCF AWS PUE                               [CCF-4]
GRID_G_KWH    = U(*[float(x) for x in os.environ.get('CARB_GRID', '320,420').split(',')])  # A5 eu-central-1; CCF/EEA 368 g/kWh [CCF-5]
EMB_G_VCPUH   = U(0.3, 1.0)     # A6 embodied g CO2e per vCPU-hour (TE 1.5–3 t / 4 y / ~96 vCPU)
EMB_G_GBH     = U(0.005, 0.02)  # A7 embodied g CO2e per GB-RAM-hour (memory-heavy servers)

# ---------------- PLATFORM EFFICIENCY (vCPU-seconds and GB-seconds per TB-equivalent) -------
# Cloud DWH — Snowflake 4XL, TPC-DS 100 TB power run: 3,760 s (Snowflake-reported) to
# 7,276 s (Databricks-measured on official data) [B-1, B-2]; 4XL = 128 nodes x 8 vCPU x 16 GB [B-3]
sf_vcpu, sf_gb = 128 * 8, 128 * 16
sf_t = U(3760, 7276)
sf_vcpus_per_tb = sf_vcpu * sf_t / 100
sf_gbs_per_tb   = sf_gb   * sf_t / 100
# Open lakehouse — Spark + Iceberg on S3, TPC-DS 3 TB, 9 x r5d.4xlarge (144 vCPU, 1,152 GB):
# 1,535.6 s (EMR 7.5 optimised runtime) to 5,546.2 s (open-source Spark 3.5.3 + Iceberg 1.6.1) [B-4]
lh_vcpu, lh_gb = 144, 1152
lh_t = U(1535.6, 5546.2)
lh_vcpus_per_tb = lh_vcpu * lh_t / 3
lh_gbs_per_tb   = lh_gb   * lh_t / 3
# A8 cross-scale normalisation (100 TB vs 3 TB runs are not linearly comparable)
sf_vcpus_per_tb *= U(0.8, 1.25); sf_gbs_per_tb *= 1  # memory scales with same run
lh_vcpus_per_tb *= U(0.8, 1.25)
# A9 production idle/over-provisioning vs benchmark: Snowflake auto-suspend, per-second billing
# (60 s min) [N09a]; open stack with always-on interactive (Trino) cluster + ephemeral Spark jobs
IDLE_SF = U(1.05, 1.30)
IDLE_LH = U(1.20, 2.00)
# A10 storage retention overhead (Time Travel/Fail-safe; Iceberg snapshots)
RET_SF, RET_LH = U(1.0, 1.3), U(1.0, 1.3)

# ---------------- OPERATING-MODEL OVERHEAD (declared assumptions, kit M1 rule) ----------------
OPM = {  # (compute multiplier range, storage multiplier range)
  'central':   ((1.00, 1.00), (1.00, 1.00)),
  'hub':       ((1.00, 1.15), (1.00, 1.10)),   # A11
  'federated': ((1.10, 1.50), (1.00, 1.30)),   # A12
}
FABRIC = ((1.05, 1.20), (1.10, 1.40))           # A13 C7 coexistence overhead: copies between lakehouse core and warehouse serving layer (kit K15; values unchanged)

def platform(kind):
    if kind == 'dwh':
        return sf_vcpus_per_tb * IDLE_SF, sf_gbs_per_tb * IDLE_SF, RET_SF
    return lh_vcpus_per_tb * IDLE_LH, lh_gbs_per_tb * IDLE_LH, RET_LH

def daily(kind, cm, sm):
    vcs, gbs, ret = platform(kind)
    w = W_TB_EQ_PER_DAY
    vcpu_h = vcs * w / 3600 * cm
    gb_h   = gbs * w / 3600 * cm
    e_cpu  = vcpu_h * (W_MIN + UTIL * (W_MAX - W_MIN)) / 1000          # kWh
    e_mem  = gb_h * MEM_KWH_GBH
    e_sto  = DATA_TB * S3_REPL * ret * sm * HDD_WH_TBH * 24 / 1000       # kWh/day
    e      = (e_cpu + e_mem + e_sto) * PUE
    op_g   = e * GRID_G_KWH
    emb_g  = vcpu_h * EMB_G_VCPUH + gb_h * EMB_G_GBH
    return op_g + emb_g, (e_cpu + e_mem) * PUE * GRID_G_KWH + emb_g      # total, compute part

def config(kind, opm, fabric=False):
    (c_lo, c_hi), (s_lo, s_hi) = OPM[opm]
    cm, sm = U(c_lo, c_hi), U(s_lo, s_hi)
    if not fabric:
        return daily(kind, cm, sm)
    fc, fs = U(*FABRIC[0]), U(*FABRIC[1])
    a_tot, a_c = daily('dwh', fc, fs); b_tot, b_c = daily('lh', fc, fs)
    return 0.5 * (a_tot + b_tot), 0.5 * (a_c + b_c)

CONFIGS = {
  'C1': ('dwh', 'central'), 'C2': ('lh', 'central'),
  'C3': ('dwh', 'hub'),     'C4': ('lh', 'hub'),
  'C5': ('dwh', 'federated'), 'C6': ('lh', 'federated'),
  'C7': ('mix', 'central'),
}
results, draws = {}, {}
for c, (k, o) in CONFIGS.items():
    tot, comp = config(k, o, fabric=(k == 'mix'))
    r1 = comp * ELT_SHARE + (tot - comp) / 1              # g per daily pipeline run (+ day's storage)
    r2 = tot * 30 / (W_TB_EQ_PER_DAY * 30)                # g per TB-equivalent processed
    r3 = tot * 30 / DATA_PRODUCTS                         # g per data product per month
    draws[c] = {'R1': r1, 'R2': r2, 'R3': r3, 'R2_compute': comp / W_TB_EQ_PER_DAY}
    results[c] = {R: np.percentile(v, [5, 50, 95]).round(1).tolist() for R, v in draws[c].items() if R != 'R2_compute'}

def p_less(a, b, R='R2'):
    return float(np.mean(draws[a][R] < draws[b][R]))

PFX = os.environ.get('CARB_OUT', 'carb')
with open(f'{PFX}-results.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['config', 'R', 'p5_g', 'median_g', 'p95_g', 'unit'])
    units = {'R1': 'g CO2e per daily pipeline run', 'R2': 'g CO2e per TB-equivalent processed',
             'R3': 'g CO2e per data product per month'}
    for c, rr in results.items():
        for R, (lo, med, hi) in rr.items():
            w.writerow([c, R, lo, med, hi, units[R]])

summary = {
  'results_p5_p50_p95': results,
  'P(C1 < C2) on R2': p_less('C1', 'C2'),
  'P(C3 < C4) on R2': p_less('C3', 'C4'),
  'P(C1 < C5) on R2': p_less('C1', 'C5'),
  'P(C2 < C6) on R2': p_less('C2', 'C6'),
  'P(C4 < C6) on R2': p_less('C4', 'C6'),
  'ranking_invariant_to_R': all(
      np.array_equal(np.argsort([results[c][R][1] for c in CONFIGS]),
                     np.argsort([results[c]['R2'][1] for c in CONFIGS])) for R in ['R1', 'R3']),
}
json.dump(summary, open(f'{PFX}-summary.json', 'w'), indent=2)
print(json.dumps(summary, indent=2))
# joint draws for the engine (SMAA samples CARB rows jointly, A14); one array per functional unit
np.savez_compressed(f'{PFX}-draws.npz', configs=np.array(list(CONFIGS)),
                    **{R: np.column_stack([draws[c][R] for c in CONFIGS]) for R in ['R1', 'R2', 'R3']})

# ---------------- SENSITIVITY: what drives C1 vs C2? ----------------
def c1_vs_c2(lh_gb_per_vcpu=8, idle_lh=(1.20, 2.00), lh_t=(1535.6, 5546.2), sf_node_scale=1.0):
    """Re-sample only the lakehouse side under an alternative assumption; P(C1 < C2) on R2."""
    t = U(*lh_t)
    vcs = lh_vcpu * t / 3 * U(0.8, 1.25) * U(*idle_lh)
    gbs = lh_vcpu * lh_gb_per_vcpu * t / 3 * U(*idle_lh)
    w = W_TB_EQ_PER_DAY
    vcpu_h, gb_h = vcs * w / 3600, gbs * w / 3600
    e = (vcpu_h * (W_MIN + UTIL * (W_MAX - W_MIN)) / 1000 + gb_h * MEM_KWH_GBH
         + DATA_TB * S3_REPL * RET_LH * HDD_WH_TBH * 24 / 1000) * PUE
    c2 = (e * GRID_G_KWH + vcpu_h * EMB_G_VCPUH + gb_h * EMB_G_GBH) / w
    c1 = draws['C1']['R2'] + (sf_node_scale - 1) * draws['C1']['R2_compute']
    return round(float(np.mean(c1 < c2)), 3), np.percentile(c2, [5, 50, 95]).round(1).tolist()

sens = {
  'baseline (r5d memory 8 GB/vCPU, idle 1.2-2.0, OSS..EMR runtime)': c1_vs_c2(),
  'S1 compute-optimised lakehouse nodes (2 GB/vCPU, as Snowflake)': c1_vs_c2(lh_gb_per_vcpu=2),
  'S2 lakehouse idle equal to warehouse (1.05-1.30)': c1_vs_c2(idle_lh=(1.05, 1.30)),
  'S3 S1 + S2 together': c1_vs_c2(lh_gb_per_vcpu=2, idle_lh=(1.05, 1.30)),
  'S4 S3 + optimised engine only (EMR 7.5 runtime)': c1_vs_c2(lh_gb_per_vcpu=2, idle_lh=(1.05, 1.30), lh_t=(1535.6, 1535.7)),
  'S5 Snowflake nodes 2x larger than the 8-vCPU estimate': c1_vs_c2(sf_node_scale=2.0),
  'S6 S4 + S5 (most lakehouse-favourable combination)': c1_vs_c2(lh_gb_per_vcpu=2, idle_lh=(1.05, 1.30), lh_t=(1535.6, 1535.7), sf_node_scale=2.0),
}
# ---------------- S7: provisioning floor (volume-dependent; not in the primary draws) ----------------
# The primary model is linear in DATA_TB, so R2 and the ranking are volume-invariant by construction.
# Real BI engines are sized for concurrency (~100 analysts), not for data volume. S7 adds that floor:
# ELT stays work-proportional; the BI share of compute becomes max(work-proportional, floor).
# F1 floor size: 2-4 nodes x 8 vCPU, each platform's baseline memory ratio (DWH 2, LH 8 GB/vCPU).
# F2 active hours: DWH 8-12 h on working days (auto-suspend); LH S7a always-on 24 h x 7 d, S7b as DWH.
def _day_g(vcpu_h, gb_h, ret):
    e = (vcpu_h * (W_MIN + UTIL * (W_MAX - W_MIN)) / 1000 + gb_h * MEM_KWH_GBH
         + DATA_TB * S3_REPL * ret * HDD_WH_TBH * 24 / 1000) * PUE
    return e * GRID_G_KWH + vcpu_h * EMB_G_VCPUH + gb_h * EMB_G_GBH

def floor_check(lh_always_on=True, lh_gb=8, lh_favourable=False):
    """Same floor capacity (vCPU, sized for concurrency) and working hours for both platforms in
    each draw, so the comparison isolates engine efficiency, memory ratio and suspend behaviour.
    Snowflake node size (sf_scale) affects only the work-proportional part, not the floor.
    lh_favourable: S6 assumptions on top (EMR runtime, lakehouse idle as warehouse, Snowflake nodes 2x)."""
    w = W_TB_EQ_PER_DAY
    nodes, hrs = U(2, 4), U(8, 12) * 5 / 7
    lh_prop = lh_vcpus_per_tb * IDLE_LH
    sf_scale = 1.0
    if lh_favourable:
        lh_prop = lh_vcpu * 1535.6 / 3 * U(0.8, 1.25) * U(1.05, 1.30)
        sf_scale = 2.0
    out = {}
    for kind, prop, gb_per_vcpu, ret in (
            ('dwh', sf_vcpus_per_tb * IDLE_SF * w / 3600 * sf_scale, 2, RET_SF),
            ('lh',  lh_prop * w / 3600, lh_gb, RET_LH)):
        h = 24.0 if (kind == 'lh' and lh_always_on) else hrs
        floor = nodes * 8 * h
        vcpu_h = prop * ELT_SHARE + np.maximum(prop * (1 - ELT_SHARE), floor)
        out[kind] = (_day_g(vcpu_h, vcpu_h * gb_per_vcpu, ret) / w,
                     float(np.mean(floor > prop * (1 - ELT_SHARE))))
    c1, c2 = out['dwh'][0], out['lh'][0]
    return {'P(C1<C2)': round(float(np.mean(c1 < c2)), 3),
            'C1 p50': round(float(np.median(c1)), 1), 'C2 p50': round(float(np.median(c2)), 1),
            'share of draws where floor binds (DWH, LH)': [round(out['dwh'][1], 3), round(out['lh'][1], 3)]}

sens['S7a provisioning floor, lakehouse interactive engine always-on'] = floor_check(True)
sens['S7b provisioning floor, both engines suspend outside working hours'] = floor_check(False)
sens['S7c S7b + S6 assumptions (compute-optimised LH nodes, EMR runtime, LH idle as DWH, Snowflake nodes 2x)'] = \
    floor_check(False, lh_gb=2, lh_favourable=True)
import platform as _pf, datetime   # _pf: this script defines its own platform() function
summary['environment'] = {'python': sys.version.split()[0], 'numpy': np.__version__, 'platform': _pf.platform(),
                          'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')}
summary['data_TB'] = DATA_TB
summary['grid_g_per_kWh'] = os.environ.get('CARB_GRID', '320,420')
summary['sensitivity_C1_vs_C2_R2 [P(C1<C2), C2 p5/p50/p95]'] = sens
json.dump(summary, open(f'{PFX}-summary.json', 'w'), indent=2)
print(json.dumps(sens, indent=2))

# ---------------- S7 for all configurations: joint draws for the SMAA sensitivity run (Stage 2 A14) ----------
# Same structure as the primary model, but the BI share of compute is max(work-proportional, floor).
# Floor (F1, F2): 2-4 nodes x 8 vCPU, same capacity for every configuration in a draw; warehouse active
# 8-12 h on working days; lakehouse active hours sampled uniformly between the warehouse's and 24 h x 7 d
# (auto-terminating to always-on). Operating-model and fabric multipliers apply to the floor as to compute.
F_NODES, F_HRS, F_LHFRAC = U(2, 4), U(8, 12) * 5 / 7, U(0, 1)

def daily_floor(kind, cm, sm):
    vcs, gbs, ret = platform(kind)
    w = W_TB_EQ_PER_DAY
    v_prop, g_prop = vcs * w / 3600 * cm, gbs * w / 3600 * cm
    h = F_HRS if kind == 'dwh' else F_HRS + F_LHFRAC * (24 - F_HRS)
    fl = F_NODES * 8 * h * cm
    gb_per_vcpu = sf_gb / sf_vcpu if kind == 'dwh' else lh_gb / lh_vcpu
    vcpu_h = v_prop * ELT_SHARE + np.maximum(v_prop * (1 - ELT_SHARE), fl)
    gb_h   = g_prop * ELT_SHARE + np.maximum(g_prop * (1 - ELT_SHARE), fl * gb_per_vcpu)
    e = ((vcpu_h * (W_MIN + UTIL * (W_MAX - W_MIN)) / 1000 + gb_h * MEM_KWH_GBH) * PUE
         + DATA_TB * S3_REPL * ret * sm * HDD_WH_TBH * 24 / 1000 * PUE)
    return e * GRID_G_KWH + vcpu_h * EMB_G_VCPUH + gb_h * EMB_G_GBH

floor_r2 = {}
for c, (k, o) in CONFIGS.items():
    (c_lo, c_hi), (s_lo, s_hi) = OPM[o]
    if k == 'mix':
        fc, fs = U(*FABRIC[0]), U(*FABRIC[1])
        tot = 0.5 * (daily_floor('dwh', fc, fs) + daily_floor('lh', fc, fs))
    else:
        tot = daily_floor(k, U(c_lo, c_hi), U(s_lo, s_hi))
    floor_r2[c] = tot / W_TB_EQ_PER_DAY
summary['S7_all_configs_R2 (floor model, p5/p50/p95)'] = {
    c: np.percentile(v, [5, 50, 95]).round(1).tolist() for c, v in floor_r2.items()}
summary['S7_all_configs P(C1 < C2) on R2'] = float(np.mean(floor_r2['C1'] < floor_r2['C2']))
json.dump(summary, open(f'{PFX}-summary.json', 'w'), indent=2)
np.savez_compressed(f'{PFX}-draws.npz', configs=np.array(list(CONFIGS)),
                    **{R: np.column_stack([draws[c][R] for c in CONFIGS]) for R in ['R1', 'R2', 'R3']},
                    R2_floor=np.column_stack([floor_r2[c] for c in CONFIGS]))
print(json.dumps({k: summary[k] for k in list(summary)[-2:]}, indent=2))
