"""U2 analysis + U5 flagging and mitigation suggestions."""
import numpy as np
try:
    from scipy import stats as sps
except Exception:
    sps = None

def paired_gap(base_scores, var_scores):
    d = np.array(var_scores) - np.array(base_scores)   # variant - base (per repetition)
    k = len(d)
    mean = float(d.mean())
    sd = float(d.std(ddof=1)) if k > 1 else 0.0
    if k > 1 and sd > 0:
        tcrit = float(sps.t.ppf(0.975, k - 1)) if sps else 1.96
        half = tcrit * sd / np.sqrt(k)
    else:
        half = 0.0
    return mean, mean - half, mean + half

def classify(mean, lo, hi, threshold):
    sig = lo > 0 or hi < 0
    if abs(mean) >= threshold and sig:
        return "FLAG"
    if sig or abs(mean) >= threshold:
        return "WATCH"
    return "OK"

MITIGATIONS = {
 "gender": [
    "Strip or tokenise first names and gendered pronouns before the LLM sees the resume (blind screening).",
    "Add an explicit instruction to judge only skills and evidence, then re-run this tester to measure whether the gap closes.",
    "Score against a fixed rubric (per-criterion 1-5) instead of one holistic score; holistic scores leak more bias.",
 ],
 "name_origin": [
    "Remove names AND email addresses from the screener input; names are the strongest proxy here.",
    "Use anonymised IDs and re-attach identity only after shortlisting.",
    "Add a counterfactual consistency check in production: re-score with a swapped name and escalate to a human if the gap exceeds the threshold.",
 ],
 "hometown": [
    "Drop the hometown line entirely; it is not job-relevant (keep current location only if needed for logistics).",
    "Do not let the screener see institution prestige or locality unless the role requires it; replace with structured criteria.",
    "Calibrate: add small-town and metro exemplars with equal scores to the prompt and re-test.",
 ],
 "general": [
    "Average over several samples and report uncertainty; one-shot scores are noisy.",
    "Fix the temperature low and pin the model version so audits are reproducible.",
    "Keep a human in the loop for borderline candidates and re-run this tester after every prompt or model change.",
 ],
}
