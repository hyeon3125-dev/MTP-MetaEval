# Worklog — MTP-MetaEval

## 2026-06-23 — reframing and the cross-domain scorecard

**Why this repo exists.** The cosmology work (`MTP-Cosmology`) had been treated as
*the* test of MTP. That was a category error: the windowed-IDE model is one
instantiation of the MTP principle in one domain, and its (real) failure there is
a single data point, not a refutation of the axiom. The axiom is a *meta-modeling*
claim — that a non-refutation / precision-floor stopping principle compresses a
task's description (fewer assumptions/params/compute) at equal-or-better adequacy.
This repo tests that claim **across domains** with a pre-registered scorecard.

**Method.** `efficiency = phenomena / (params + assumptions + compute_norm)`,
`ratio = E_mtp / E_baseline` per domain. Definitions, baselines, tolerances, and
the assumption rubric were fixed in `PREREGISTRATION.md` before computing any
result; one tolerance amendment (control 0.05→0.15) is disclosed there. Each
domain reuses an existing artifact; numbers are parsed mechanically from real runs.

Added to `MTP-Cosmology`: HDE (event-horizon) and RVM (running-vacuum) reference
models. Added to `thermal_controller.c`: a fixed-N baseline arm (same noise) so
the control comparison is a true head-to-head; the adaptive output is unchanged.

**Results (per-domain; no cross-domain aggregate by design).**

| domain | baseline | mtp | ratio | verdict | flag |
|--------|----------|-----|-------|---------|------|
| cosmology | ΛCDM (E=0.50) | windowed IDE (E=0.008) | **0.017** | worse | none |
| number theory (RH) | exhaustive accum. (E=0.20) | non-refutation stop (E=0.46) | **2.31** | improves | partial |
| engineering control | fixed-N (E=0.40) | adaptive floor (E=0.70) | **1.74** | improves | partial |

Details:
- **Cosmology**: windowed IDE adds 3 params + 3 assumptions and an ODE-cost H(z)
  (~350× ΛCDM) while covering the same 3 data blocks → far lower efficiency.
  Compute-excluded sensitivity: ratio still 0.50 (worse) → verdict robust. RVM
  (E≈0.42) and CPL (E≈0.35) are the efficient reference models; the IDE/ODE
  models all score low. Genuine baseline, **no construction flag**.
- **RH**: both arms reach "RH non-refuted on the critical line"; the
  non-refutation stop (t<50, 9 zeros) uses ~1/6 the Landauer entropy of exhaustive
  accumulation (t<200, 79 zeros) and drops one arbitrary knob → higher efficiency.
  Flagged **partial** (entropy saving follows from Landauer once you accept the
  stop).
- **Control**: the adaptive arm **Pareto-dominates** — lower error *and* fewer
  iterations in all three scenarios (step/ramp/sinusoid) — so the win is
  tolerance-robust. compute_norm 0.30. Flagged **partial** (adaptive ≤ fixed
  iterations is near-tautological; the non-trivial part is that accuracy improves
  too).

**Meta-pattern (qualitative, as pre-registered).** MTP behaves as a
**cost/compression principle**: it improves efficiency where the bottleneck is
*wasteful accumulation* (RH entropy, control iterations) but **not** where the
task requires *adding explanatory structure* (cosmology). Both "improves"
verdicts are construction-flagged → weak evidence; the single genuine-baseline
test (cosmology) goes against MTP.

**Verdict.** MTP is supported as a **verification/stopping heuristic**, *not* as a
universal modeling principle that compresses arbitrary scientific descriptions.
This is a real, falsifiable conclusion — and it correctly does NOT rest on the
cosmology failure alone (that was always just one domain).

**Next (if pursued).** Stronger test = a domain where MTP must *add* structure and
a genuine (un-flagged) baseline exists, like cosmology — e.g. apply the
non-refutation principle to an inference/active-learning task and check whether it
beats a standard stopping rule on real held-out data.
