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

## 2026-06-23 (cont.) — the un-flagged stopping test (sequential refutation)

Built the test the worklog above asked for: a domain where the floor has a
**ground truth it can get wrong** (`adapters/sequential.py`,
PREREGISTRATION §3d, `docs/overhead_boundary.md`). A population of conjectures
(TRUE = no counterexample in `[0,M)`, FALSE = counterexample at `x~Geometric(r)`);
baseline = exhaustive scan; mtp = stop at the non-refutation floor `q(t) ≤ ε`.

Motivated by the question "is MTP-as-stopping nihilism?" — answer: **no, with a
caveat.**

1. **Risk is provably bounded** (non-nihilism): under a correct prior,
   `miss_rate ≤ ε(1−π0)`; confirmed empirically (ε=0.01 → miss 0.0052 vs bound
   0.005) at ~94% compute saved. The overhead boundary is real and the risk is a
   knob you set. Plot: `results/sequential_overhead_boundary.png`.
2. **But the efficiency ratio is only neutral (0.98)**: the floor buys its 94%
   compute saving with an *extra prior assumption*, which cancels the gain in
   `phenomena/(params+assumptions+compute_norm)`. MTP = assumption-for-compute
   trade, not free compression.
3. **Failure mode = prior misspecification**: under a 4× heavier true tail the
   miss rate jumps to 0.156 (~31× the bound) while still "saving" 93% — the bound
   is only as good as the prior. This is the same reason windowed-IDE failed in
   cosmology (added structure the data did not reward).

This is the **un-flagged** evidence (construction_flag = none, ground truth):
MTP is a **risk-bounded verification-stopping** principle, not a universal
compression. It earns its keep cutting wasteful accumulation under a correct
model, and fails when it must add believed structure or when its prior is wrong.

Updated scorecard now runs 4 domains; meta-pattern reading in `run_scorecard.py`
revised accordingly.

## 2026-06-23 (cont.) — three strengthening tests + consolidated report

The single un-flagged ground-truth result (sequential) used a synthetic
population. Added three stronger tests and reframed the whole project's field.

- **① Historical validation** (`adapters/real_conjectures.py`,
  `docs/real_conjectures.md`): Pólya / Euler-n5 / Mertens / π(x)<li(x) vs
  Collatz / Goldbach. An efficient floor would have endorsed all 4 famous
  *disproven* conjectures; 2 (Mertens, Skewes) have counterexamples beyond all
  computation — settled only by proof. The synthetic shift-failure is the
  historical norm, and RH (no proven counterexample bound) is the same unbounded
  gamble. Retro-flags the RH-domain win.
- **② Robustness frontier** (`adapters/robustness.py`): the naive floor turns
  unsafe at a true tail only 2× heavier (miss ~10× bound). A conservative floor
  is safe up to heaviness s but compute-saved falls 94.5%→63% (s=1→8). Robustness
  buys range, never invulnerability; unbounded tails admit no safe finite floor.
- **③ Earned vs assumed structure** (`adapters/changepoint.py`): the same
  add-localized-structure move that windowed-IDE LOST in cosmology is WON on the
  real Nile series — changepoint at 1899 (Aswan dam), ΔAIC −53, permutation
  p<0.001 — and NOT selected under a shuffled null. Cosmology's loss generalizes
  conditionally: assumed structure loses, earned structure wins.

**Unifying law (REPORT.md):** across all six un-flagged rows, MTP earns its keep
exactly to the degree its assumption matches reality; the failure mode is always
assumed-not-earned. **Field placement:** this is Computational Verification +
Decision Theory (optimal stopping) + Reliability Engineering — "when to stop
verifying" — not physics / pure math / control. Those are application instances.

Consolidated write-up: `REPORT.md`.

## 2026-06-23 (cont.) — earned/assumed as one calibrated curve

Idle-time research to harden the central law (not a new model). Unified the
cosmology (assumed, lost) and Nile (earned, won) cases on a single axis — the SNR
of the localized structure (`adapters/earned_threshold.py`, noise calibrated to
Nile's within-segment scatter).

- Null-calibrated detection power crosses 95% at SNR ≈ 0.9. Nile sits at SNR ≈ 2.0
  (power ~1.0); cosmology's windowed signal was sub-percent vs data errors
  (SNR ≪ 1, below threshold). Assumed-vs-earned is *position on this curve*.
- Bonus, self-referential: naive AIC<0 selects the localized model ~48% of the
  time from pure NOISE (the changepoint-location search overfits, unpenalized).
  The detector itself is assumed-not-earned unless calibrated against the null —
  the law applies to the verification of the verification.

Plot: `results/earned_threshold.png`. Folded into REPORT §6.1.

## 2026-06-23 (cont.) — live application: LLM capability overhead

Applied the overhead boundary to LLM progress (`adapters/llm_overhead.py`,
`docs/llm_overhead.md`). Accumulation axis = model generations; floor =
user-perceptible difference via LMArena's exact Elo->win-rate map
P=1/(1+10^(-dElo/400)). Pre-registered floors: 55% win -> 35 Elo, 60% -> 70 Elo.

Structural, non-fabricating: the verdict rests on the CITED clustering fact
(LMArena June 2026: top tier within ~55 Elo, tightest on record; successive-leader
low ~4 Elo in 2025-02) + the exact Elo math, not invented per-model scores.

- Adjacent frontier models ~14 Elo -> ~52% blind preference -> below the 35-Elo
  floor -> INSIDE the overhead region. Trend: GPT-3.5->GPT-4 ~100 Elo (earned) ->
  2025-26 ~4-14 Elo (overhead). On the median everyday prompt, recent frontier
  improvement buys capability with ~0 perceptible marginal difference.
- NOT a ceiling: this is the §6.1 SNR law per task. Easy prompts = low
  capability-SNR (imperceptible); hard distributions (math/agentic/long-context)
  = high SNR, gaps still earned. Overhead is easy-task-only -> falsifiable
  predictions in docs/llm_overhead.md.
- Caveats: Elo != capability; aggregate != per-task; benchmark saturation is a
  measurement ceiling.

This is the framework's most load-bearing application and the strongest
why-care-now hook for a preprint: the same overhead-boundary law dates the
diminishing returns of LLM scaling and locates them on the easy-task axis.

## 2026-06-23 (cont.) — capability is a vector; "hard" is undefined (+ submittable form)

Sharpened the LLM domain after a key objection: "hard tasks still earn" is
under-specified because capability is a VECTOR, not a scalar, and most of it is
not benchmarked cross-vendor.

- `adapters/llm_overhead.py` now reports a capability-axis table: of 7 axes the
  overhead verdict is *measurable* on 3 (all text; everyday→overhead, coding/math
  →re-ranked) and *undetermined/unmeasurable* on 4 (agentic, long-context,
  multimodal, vendor-specific) — no cross-vendor quantitative basis exists.
  Verifiable, cited: Arena categories re-rank models; the leader tops no single
  automated benchmark; benchmarks are fragmented (HLE/ARC-AGI-2/AIME/FrontierMath/
  SWE-bench/τ²-Bench), least unified for multimodal.
- New position: "has scaling entered overhead?" is ILL-POSED without naming the
  projection; confirmed only on the everyday-text axis, unanswerable on multimodal/
  agentic/vendor-specific for lack of measurement. Asserting GLOBAL overhead from
  aggregate Elo is itself assumed-not-earned. docs/llm_overhead.md fully updated.

Submittable-form pass:
- REPORT §7.2 scope (RH/control are construction-flagged demonstrations, not
  contributions; the un-flagged work is load-bearing).
- REPORT §7.3 related work (SPRT/optimal stopping, AIC/BIC/MDL, Landauer/Bekenstein,
  permutation/selective inference, Arena + scaling laws) — novelty claimed only in
  synthesis + falsification discipline + the LLM projection framing, not new theory.

## 2026-06-23 (cont.) — quantified LLM projections + arXiv manuscript

- item 3 (quantify): real Arena Elo (openlm.ai/chatbot-arena, June 2026) folded
  into `llm_overhead.py`. Overall/text top-10 within 14 Elo (adjacent ~7 ->
  ~51% blind preference -> overhead) vs coding top tier ~256 Elo spread (18x
  wider -> earned). Projection-dependence now quantified, not asserted.
- item 1+2 (manuscript): `paper/main.tex` — self-contained arXiv-ready paper
  (abstract, 9 sections, 2 figures, embedded bibliography so it compiles with no
  bibtex pass). `paper/refs.bib` optional. RH/control labeled demonstrations;
  related work positions vs SPRT/optimal stopping, AIC/BIC/MDL, Landauer, Arena,
  scaling laws; novelty scoped to synthesis + protocol + LLM projection framing.
- `paper/ARXIV_SUBMISSION.md`: honest "no git-push to arXiv" + 10-min Overleaf/
  direct-upload paths + endorsement note. cs.LG primary, stat.ME/cs.AI cross-list.

Repo is in submittable form; the manual step is a ~10-minute web upload.

## 2026-06-23 (cont.) — 'everyday' is unmeasured too (pre-arXiv fix)

Reviewer objection (correct): the LLM verdict was stated on "everyday text," but
"everyday" is not a measured quantity -- the same assumed-not-earned trap as
"hard." `adapters/info_content.py` makes the axis measurable (deictic density
falls monotonically casual 0.35 -> formal 0.00; gzip is a weak, non-monotone proxy
since it ignores external shared context; the faithful measure is LM perplexity).

The deeper consequence: high-shared-context prompts have a narrow correct-answer
space (low capability-SNR by construction), so models tie there regardless of
saturation. Aggregate Arena indistinguishability therefore CONFLATES (a) capability
saturation with (b) a low-information prompt mix, and Arena does not stratify by
information content -> for the saturation question the measurement is an
uncontrolled mixture (broken in that respect). Fix: stratified evaluation (do gaps
shrink across generations within high-information strata?). Until then the
defensible claim is only "adjacent models tie on the aggregate mixture," not
"capability has saturated."

Updated REPORT §7.1, docs/llm_overhead.md, paper/main.tex (abstract, §7, limits).
