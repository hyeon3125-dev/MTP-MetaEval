# MTP-MetaEval — explanatory-efficiency scorecard

Tests the **MTP axiom as a meta-modeling principle**, not as a cosmological
model. The principle:

> *Optimal verification/control accumulates only up to a non-refutation /
> precision floor; past that floor, marginal information gain falls below
> marginal entropy cost, so further accumulation is waste.*

The question is **not** whether a specific dark-energy model fits the data. It is
whether adopting this principle lets a domain's task be re-expressed with
**fewer assumptions / parameters / compute at equal-or-better adequacy** than the
standard approach — measured across domains by

```
efficiency = phenomena_covered / (free_params + assumptions + compute_norm)
ratio      = efficiency_mtp / efficiency_baseline      # per domain
```

> The windowed-IDE cosmology work (sibling repo `MTP-Cosmology`) was **one failed
> instantiation** of the principle in one domain — a single data point in this
> scorecard, not a test of the axiom itself.

## What it does

Three domains, each reusing an existing artifact, each a `baseline` (standard)
vs `mtp` (principle-framed) head-to-head under one schema:

| domain | baseline | mtp | artifact reused |
|--------|----------|-----|-----------------|
| cosmology | ΛCDM | windowed IDE | `MTP-Cosmology/` engine (+CPL/IDE/HDE/RVM refs) |
| number theory (RH) | exhaustive zero accumulation | non-refutation stop | `MTP-riemann-z explorer/riemann_explorer.c` |
| engineering control | fixed-window N_MAX | adaptive precision-floor | `…/thermal_controller.c` |

All operational definitions, baselines, tolerances, and the assumption-counting
rubric are fixed up front in [PREREGISTRATION.md](PREREGISTRATION.md) (with a
disclosed amendment). Every number is extracted mechanically from a real run — no
hand-assigned scores.

## Run

```bash
python run_scorecard.py                      # all three domains -> results/scorecard.csv
python adapters/cosmology.py                 # one domain at a time
python adapters/riemann.py
python adapters/control.py
```

Requires the sibling repos `MTP-Cosmology/` and `MTP-riemann-z explorer/` next to
this one, plus their deps (numpy/scipy for cosmology; gcc for the C artifacts).

## Layout

```
PREREGISTRATION.md     pre-fixed definitions / baselines / tolerances / amendments
scorecard/schema.py    ApproachScore, DomainScore, efficiency + verdict
scorecard/assumptions.py  frozen assumption counts (rubric §4)
adapters/{cosmology,riemann,control}.py   run artifact -> parse -> ApproachScore
run_scorecard.py       cross-domain table + qualitative meta-pattern
results/scorecard.csv  generated
```

## Result (see worklog for the run)

The pattern is honest and mixed (and was the pre-registered expectation): the
principle improves efficiency where the bottleneck is **wasteful accumulation**
(RH entropy, control iterations) but **not** where the task requires **adding
explanatory structure** (cosmology). Crucially, both "improves" verdicts are
*construction-flagged* (weak evidence), while the one genuine-baseline test
(cosmology) goes **against** MTP. So MTP is supported as a **verification-stopping
heuristic**, **not** as a universal modeling principle. See [worklog.md](worklog.md).
