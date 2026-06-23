# Pre-registration — MTP explanatory-efficiency scorecard

> Fixed **before** computing any scorecard result. The point of pre-registering
> operational definitions, baselines, and tolerances is to stop the evaluation
> from degenerating into numerology: every number in the scorecard must be
> extracted mechanically from a real run under the rules below, not hand-assigned
> after seeing the outcome.

## 0. What is actually being tested

The MTP axiom is a **meta-modeling principle**, not a cosmological model:

> *Optimal verification/control accumulates only up to a non-refutation / precision
> floor; past that floor marginal information gain falls below marginal entropy
> cost, so further accumulation is waste.*

Claim under test (per-domain, falsifiable): **adopting this principle re-expresses
a domain's task with equal-or-better adequacy at lower cost/complexity than the
standard approach.** Windowed-IDE cosmology was *one instantiation*; its failure
is a data point, not a refutation of the principle. Equally, a win in one domain
is not a proof of the principle — support requires it holding across *multiple*
domains against *genuine* baselines.

## 1. Core metric

For each domain, two approaches — `baseline` (standard) and `mtp` (principle-framed):

```
efficiency E = phenomena_covered / (free_params + assumptions + compute_norm)
ratio        = E_mtp / E_baseline          # the ONLY cross-domain-comparable number
```

- `compute_norm` is the measured cost divided by the baseline's cost (so the
  baseline's compute_norm = 1 by construction).
- Only the **ratio** is reported per domain. **No single aggregate index** across
  domains (incommensurable units). The meta-result is the *pattern* of ratios
  plus a per-domain verdict.

Verdict thresholds (fixed now):
- `ratio > 1.10` → "improves" ; `0.90–1.10` → "neutral" ; `< 0.90` → "worse".
- A win is **discounted** if it is true essentially by construction (flagged
  per domain below); such wins are weak evidence for the principle.

## 2. Term definitions (operational, mechanical)

`phenomena_covered` — count of distinct phenomena/cases the approach accounts for
within the domain tolerance (below). `free_params` — number of tunable parameters.
`assumptions` — counted with the rubric in §4. `compute_cost` — a measured runtime
or entropy proxy, specified per domain.

## 3. Domains, baselines, tolerances

### 3a. Cosmology  (reuses MTP-Cosmology comparison engine)
- **baseline** = ΛCDM (0 free DE params). **mtp** = windowed IDE (mtp_3p).
- **reference comparators** (reported, not the head-to-head): CPL, constant IDE,
  sign-switching IDE, HDE, RVM.
- `phenomena_covered` = number of data blocks fit at χ²/dof ≤ **2.0**
  (blocks: BAO-geometry, RSD-growth, CMB-distance). Tolerance 2.0 fixed now.
- `free_params` = k (DE-sector). `assumptions` per §4.
- `compute_cost` = number of model H(z) evaluations to fit (∝ optimizer calls);
  normalized to ΛCDM.
- **Construction flag**: none — this is a genuine, already-published-style test.

### 3b. Number theory / RH  (reuses riemann_explorer.c)
- **baseline** = *exhaustive accumulation*: scan to a fixed large t_max with no
  stopping rule ("more zeros = more confidence").
- **mtp** = *non-refutation stop*: scan only until the non-refutation criterion is
  met (Z(t) sign-changes within the θ error bound), then stop.
- `phenomena_covered` = 1 if "RH non-refuted on the critical line over the scanned
  range" holds (both approaches reach it); else 0.
- `free_params` = number of free knobs in the stopping rule: baseline = 1
  (arbitrary t_max — an unjustified choice), mtp = 0 (stop is determined by the
  error bound, not chosen).
- `assumptions` per §4.
- `compute_cost` = Landauer entropy proxy (J) accumulated, from the program's
  Stage-3 output (the baseline scans ~4× further in t, accruing more J at zero
  added refutation power).
- **Construction flag**: PARTIAL — the entropy saving follows from Landauer once
  one accepts "stop at the floor"; flagged as such.

### 3c. Engineering control  (reuses thermal_controller.c)
- **baseline** = fixed-window controller, always N = N_MAX iterations/step.
- **mtp** = adaptive precision-floor controller, stop at σ/√N noise floor.
- `phenomena_covered` = number of scenarios (step, ramp, slow-sinusoid) tracked
  with mean abs error ≤ **0.15** (see AMENDMENTS §A1; was 0.05). NOTE: a lost
  scenario is a real cost and must be reported, not hidden. The tolerance-robust
  finding (reported alongside) is whether one arm Pareto-dominates the other
  (≤ error AND ≤ iterations in every scenario).
- `free_params` = controller knobs: baseline = 1 (N_MAX, chosen), mtp = 1 (the
  floor multiplier) — equal, so this term does not bias the comparison.
- `assumptions` per §4.
- `compute_cost` = mean iterations/step (total work), normalized to baseline.
- **Construction flag**: PARTIAL — "adaptive ≤ fixed in iterations" is nearly
  tautological; the *non-trivial* question is whether it keeps phenomena_covered.
  The honest test is the accuracy/coverage trade, not the iteration saving alone.

### 3d. Sequential refutation — the un-flagged stopping test (added 2026-06-23)

The RH and control wins are construction-flagged ("accept the stop ⇒ you save").
This domain removes the flag by giving the stopping rule a **ground truth it can
get wrong**: it must locate the *overhead boundary* — the point past which
continuing to search is genuinely wasteful — without stopping so early that it
misses a real counterexample.

- Population of conjectures, each with a hidden truth: TRUE (no counterexample in
  the horizon [0, M)) with prob 1−π0, or FALSE with a counterexample at location
  x ~ Geometric(r_true). Checking candidate t reveals whether t refutes; cost 1
  per check (+ Landauer entropy).
- **baseline** = exhaustive scan to M (stops early only if it *finds* a
  counterexample); always correct within M.
- **mtp** = *non-refutation floor*: having survived [0, t) with no counterexample,
  the Bayesian posterior that one still remains is
  `q(t) = π0·S(t) / [(1−π0) + π0·S(t)]`, S(t)=P(x≥t) under an assumed prior
  Geometric(r_assumed). Stop at the smallest t with `q(t) ≤ ε`. ε is set by the
  Landauer marginal-cost / stake ratio (principled, not tuned).
- `phenomena_covered` = fraction of conjectures given the **correct** verdict
  (refuted iff false). baseline ≈ 1.0; mtp = 1 − miss_rate, where a miss is a
  FALSE conjecture whose counterexample sits at x ≥ t_floor (stopped too early).
- `free_params`: baseline 1 (horizon M), mtp 1 (floor ε) — equal.
- `compute_cost` = total checks, normalized to baseline.
- **Operating point for the scorecard row**: in-distribution (r_assumed=r_true),
  ε = 0.01.
- **Construction flag: NONE.** Ground truth makes the rule falsifiable — it can
  miss.

Pre-registered claims (report as-is, even if contradicted):
1. **Risk bound**: under a correct prior, the floor bounds the miss rate by
   ≈ ε (theorem: miss_rate = π0·S(t_floor) ≤ ε(1−π0)). Verified empirically.
2. **In-distribution**: mtp should win on efficiency (un-flagged) — large compute
   saving at miss_rate ≤ ε.
3. **Failure mode** (the anti-rigging control): under distribution shift
   (r_true heavier-tailed than r_assumed, e.g. a Pareto tail the prior does not
   expect), the miss rate should exceed ε and the win should degrade or flip.

This is the non-nihilism test: if (1)+(2) hold, "keep searching but stop at a
principled floor" is a valid methodology with *quantitatively bounded* risk — not
a surrender. (3) names exactly when it breaks (prior misspecification).

## 4. Assumption-counting rubric (applied identically to every approach)

Count **+1** for each independent, explicit modeling commitment beyond raw
observation. Shared substrate assumptions that BOTH approaches in a domain make
are counted for both (they cancel in the ratio but are recorded for transparency).

Cosmology base (all models): GR, FRW homogeneity/isotropy, CDM, fixed-Planck
early universe → 4. Each model then adds its DE mechanism's commitments
(e.g. Λ = +1; CPL w(a) form = +1; windowed IDE: coupling ansatz +1, F_hier
hierarchy +1, sign-switch +1).

RH: "Z(t) sign-change ⇒ zero on the line" +1; "θ error bound valid" +1; baseline
adds "more scanning ⇒ more confidence" +1 (an unjustified premise the mtp
approach drops).

Control: "Gaussian noise, CLT error ~σ/√N" +1; "moving-average model adequate"
+1; baseline adds "fixed N is safe everywhere" +1; mtp adds "noise-floor stop is
safe" +1.

The exact per-approach counts are tabulated in `scorecard/assumptions.py` and are
frozen with this document.

## 5. Reporting rules

- Report each domain's `(phenomena, params, assumptions, compute_norm, E, ratio,
  verdict, construction_flag)`.
- State explicitly when a domain's win is construction-flagged.
- The meta-conclusion is a **qualitative pattern over the three ratios**, with the
  honest expectation registered up front: the principle is a *cost/compression*
  principle, so it is expected to help where the bottleneck is wasteful
  accumulation (RH entropy, control iterations) and **not** where the task
  requires adding explanatory structure (cosmology). If the data contradict this
  expectation, that is reported as-is.

## AMENDMENTS (disclosed)

**A1 (control tolerance, 0.05 → 0.15).** The original 0.05 was set without
knowledge of the achievable error scale. On running both arms, the mean abs
errors are *lag-dominated* on the dynamic signals (≈0.07–0.21 on unit-range
signals), well above the σ=0.005 noise floor — so 0.05 is below what *any*
moving-average controller achieves on these transients and fails to
discriminate. Amended to 0.15 (≈15% of the unit signal range, the scale at which
a moving-average tracker is "following" rather than lagging). To prevent
result-shopping, the scorecard also reports the tolerance-independent
**Pareto-dominance** check and a coverage sensitivity at {0.10, 0.15, 0.20}. The
verdict is robust: the adaptive arm has lower error AND fewer iterations in every
scenario, so it Pareto-dominates regardless of the tolerance.
