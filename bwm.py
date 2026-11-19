"""Best-Worst Method: linear model (Rezaei 2016), input-based consistency (Liang, Brunelli & Rezaei 2020),
attention check (Stage 2 plan A1–A3)."""
from dataclasses import dataclass
import numpy as np
from scipy.optimize import linprog

# Liang, Brunelli & Rezaei (2020), Omega 96:102175, Table 3 — thresholds for the input-based CR.
# Rows: a_BW (the best-to-worst judgement) 3..9; columns: number of criteria 3..9.
# Transcribed 28 Sep 2026 from two independent copies of the paper (TU Delft and UniTN repositories); identical.
CR_THRESHOLDS = {
    # a_BW = 2: not in Table 3; the note to Table 3 says the threshold "should be 0 in this case, because, when the
    # preferences are ordinal-consistent, the CRI = 0" (Liang et al. 2020). Added by Stage 2 amendment 1 (7 Oct 2026).
    2: [0.0] * 7,
    3: [0.1667, 0.1667, 0.1667, 0.1667, 0.1667, 0.1667, 0.1667],
    4: [0.1121, 0.1529, 0.1898, 0.2206, 0.2527, 0.2577, 0.2683],
    5: [0.1354, 0.1994, 0.2306, 0.2546, 0.2716, 0.2844, 0.2960],
    6: [0.1330, 0.1990, 0.2643, 0.3044, 0.3144, 0.3221, 0.3262],
    7: [0.1294, 0.2457, 0.2819, 0.3029, 0.3144, 0.3251, 0.3403],
    8: [0.1309, 0.2521, 0.2958, 0.3154, 0.3408, 0.3620, 0.3657],
    9: [0.1359, 0.2681, 0.3062, 0.3337, 0.3517, 0.3620, 0.3662],
}


@dataclass
class BWMResponse:
    best: int                 # index of best criterion
    worst: int                # index of worst criterion
    bo: np.ndarray            # best-to-others, 1..9, bo[best] == 1
    ow: np.ndarray            # others-to-worst, 1..9, ow[worst] == 1


def attention_check(r: BWMResponse):
    """A1, with Stage 2 amendment 1 (7 Oct 2026). Returns (passed, reasons)."""
    reasons = []
    if r.best == r.worst:
        reasons.append('the same criterion was chosen as best and as worst')
    elif r.bo[r.worst] == 1:
        others = [j for j in range(len(r.bo)) if j not in (r.best, r.worst)]
        if np.any(np.asarray(r.bo)[others] != 1) or np.any(np.asarray(r.ow)[others] != 1):
            reasons.append('best rated equal to worst, but not every criterion is rated 1')
    if r.bo[r.best] != 1:
        reasons.append('best criterion not rated 1 in best-to-others')
    if r.ow[r.worst] != 1:
        reasons.append('worst criterion not rated 1 in others-to-worst')
    if abs(r.bo[r.worst] - r.ow[r.best]) > 1:
        reasons.append('best-to-worst differs between the vectors by more than 1')
    return (not reasons), reasons


def reconcile(r: BWMResponse) -> BWMResponse:
    """A2: where the two vectors disagree on best-to-worst by exactly 1, the best-to-others value is used."""
    ow = np.array(r.ow, float).copy()
    if abs(r.bo[r.worst] - ow[r.best]) == 1:
        ow[r.best] = r.bo[r.worst]
    return BWMResponse(r.best, r.worst, np.array(r.bo, float), ow)


def linear_bwm(r: BWMResponse):
    """Linear BWM (Rezaei 2016): min xi s.t. |w_B - a_Bj w_j| <= xi, |w_j - a_jW w_W| <= xi, sum w = 1, w >= 0.
    Returns (weights, xi_L)."""
    bo, ow = np.asarray(r.bo, float), np.asarray(r.ow, float)
    n = len(bo)
    c = np.zeros(n + 1); c[-1] = 1.0          # variables: w_0..w_{n-1}, xi
    A, b = [], []
    for j in range(n):
        for sign in (1, -1):
            row = np.zeros(n + 1); row[r.best] += sign; row[j] -= sign * bo[j]; row[-1] = -1
            A.append(row); b.append(0.0)
            row = np.zeros(n + 1); row[j] += sign; row[r.worst] -= sign * ow[j]; row[-1] = -1
            A.append(row); b.append(0.0)
    Aeq = np.zeros((1, n + 1)); Aeq[0, :n] = 1
    res = linprog(c, A_ub=np.array(A), b_ub=b, A_eq=Aeq, b_eq=[1.0], bounds=[(0, None)] * (n + 1), method='highs')
    if not res.success:
        raise RuntimeError(res.message)
    return res.x[:n], float(res.x[-1])


def consistency_ratio(r: BWMResponse):
    """Input-based CR (Liang et al. 2020): CR_j = |a_Bj a_jW - a_BW| / (a_BW (a_BW - 1)); CR = max_j CR_j.
    Returns (CR, per-criterion CR_j, index of the criterion contributing most)."""
    bo, ow = np.asarray(r.bo, float), np.asarray(r.ow, float)
    a_bw = bo[r.worst]
    if a_bw <= 1:
        crj = np.zeros(len(bo))
    else:
        crj = np.abs(bo * ow - a_bw) / (a_bw * (a_bw - 1))
    return float(crj.max()), crj, int(np.argmax(crj))


def cr_threshold(a_bw: float, n: int):
    """Threshold from Liang et al. (2020) Table 3, plus 0 for a_BW = 2 (note to Table 3). Returns None for a_BW = 1
    or n outside 3..9."""
    a = int(round(a_bw))
    if a not in CR_THRESHOLDS or not 3 <= n <= 9:
        return None
    return CR_THRESHOLDS[a][n - 3]


def evaluate(r: BWMResponse):
    """A1–A3 for one response. Returns a dict with weights, xi_L, CR, threshold, flags."""
    ok, reasons = attention_check(r)
    rr = reconcile(r)
    w, xi = linear_bwm(rr)
    cr, crj, worst_pair = consistency_ratio(rr)
    a_bw = rr.bo[rr.worst]
    thr = cr_threshold(a_bw, len(rr.bo))
    if a_bw <= 1:
        consistent = bool(np.all(rr.bo == 1) and np.all(rr.ow == 1))
        rule = 'a_BW = 1: consistent only if every rating is 1'
    elif int(round(a_bw)) == 2:
        consistent, rule = cr <= thr, 'a_BW = 2: threshold 0 (Liang et al. 2020, note to Table 3)'
    else:
        consistent, rule = cr <= thr, 'table'
    return {'weights': w, 'xi_L': xi, 'CR': cr, 'CR_j': crj, 'threshold': thr, 'threshold_rule': rule,
            'consistent': bool(consistent), 'recontact_pair': worst_pair,
            'attention_ok': ok, 'attention_reasons': reasons}
