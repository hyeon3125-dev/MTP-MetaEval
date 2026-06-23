# Verification efficiency under bounded risk — a cross-domain report

**What field is this?** Not physics, not pure mathematics, not control
engineering — those are *application instances*. The actual subject is

> **Computational Verification + Decision Theory (optimal stopping) + Reliability
> Engineering**: *when should verification stop, given a cost of checking and a
> risk of being wrong?*

Each "domain" here is the same question wearing different clothes. Cosmology is
not "which dark-energy model is true" but "how much, and by what criterion, do we
verify a model." RH is not "prove the hypothesis" but "when to stop searching for
a counterexample." Control is not "tune the PID" but "when does another sample
stop adding information." The unit of study is the **verification system**, and
the metric is **explanatory / verification efficiency under a bounded risk of
misjudgment**.

## Thesis (one line)

> The value of a non-refutation floor — or any MTP-style structural assumption —
> equals the strength of the match between that assumption and reality. It buys
> compute with an assumption; the trade is a net gain exactly when the assumption
> holds, and a hidden, unbounded loss when it does not.

## The core object: the overhead boundary

After surveying [0, t) with no counterexample, the posterior that one still
remains is `q(t)`. The **floor** `t_floor(ε)` is the point where `q(t) ≤ ε`: past
it, more checking spends entropy (Landauer) for ~zero refutation power. The whole
program is the study of this boundary — where it is, when stopping at it is safe,
and what it costs.

## Evidence, in order of strength

### Pre-registered, mechanical (PREREGISTRATION.md)
All definitions/baselines/tolerances and the assumption rubric were fixed before
any result; numbers are parsed from real runs, never hand-assigned. One amendment
(control tolerance) is disclosed.

### The four-domain efficiency scorecard (`run_scorecard.py`)

| domain | ratio E_mtp/E_base | verdict | flag |
|--------|------:|---------|------|
| cosmology (ΛCDM vs windowed IDE) | ≈0.02 | worse | none — genuine baseline |
| number theory / RH (exhaustive vs floor) | 2.31 | improves | **partial — by construction** |
| control (fixed-N vs adaptive floor) | 1.74 | improves | **partial — by construction** |
| sequential refutation (exhaustive vs floor) | 0.98 | neutral | none — ground truth |

The two "improves" are construction-flagged (the saving is near-tautological once
you accept stopping). The two un-flagged, ground-truth tests carry the weight.

### The headline: the overhead-boundary theorem and its failure (`docs/overhead_boundary.md`)

1. **Bounded risk (non-nihilism).** Under a correct prior the floor obeys
   `miss_rate ≤ ε(1−π0)` — verified to the digit (ε=0.01 → miss 0.0052) at ~94%
   compute saved. "Keep searching, stop at a principled floor" is a *legitimate,
   risk-controlled* method, not surrender.
2. **Not free.** The scorecard ratio is only neutral (0.98): the saving is bought
   with an extra prior assumption that cancels it in
   `phenomena/(params+assumptions+compute)`. MTP = assumption-for-compute trade.
3. **Breaks under misspecification.** A 4× heavier true tail sends the miss rate
   to 0.16 (~31× the bound) while still "saving" 93%.

### Strengthening 1 — the historical record (`docs/real_conjectures.md`)

The synthetic failure is the historical norm. Of four famous **disproven**
conjectures, an efficient floor would have endorsed **all four** as "non-refuted":
Pólya (counterexample at 9×10⁸), Euler n=5 (144⁵), Mertens (beyond all
computation), π(x)<li(x) (≈10³¹⁶). Two were settled *only by proof*, never by
scanning. Collatz and Goldbach (true to 10²⁰, 10¹⁸) are correctly endorsed by
stopping. **Consequence:** non-refutation stopping is safe only given a *proven
bound* on counterexample location. RH has none — so the RH-domain "win" is the
same unbounded gamble as Mertens and Skewes.

### Strengthening 2 — the robustness frontier (`adapters/robustness.py`)

The naive floor becomes unsafe at a true tail only 2× heavier (miss ~10× bound).
A conservative floor stays safe up to heaviness `s` but pays in compute saved:
s=1 → 94.5%, s=2 → 90%, s=4 → 81%, s=8 → 63%. **Robustness buys range, never
invulnerability**: against an unbounded tail (no proven bound) no finite-compute
floor is safe.

### Strengthening 3 — earned vs assumed structure (`adapters/changepoint.py`)

The same "add localized structure" question that windowed-IDE *lost* in cosmology
is *won* on the real Nile series: a changepoint model selects the 1899 regime
shift with ΔAIC = −53 (permutation p < 0.001), and is *not* selected under a
shuffled null. So cosmology's loss generalizes **conditionally**: *assumed*
structure loses, *earned* structure wins.

## What every un-flagged test says, together

| test | MTP assumption | matches reality? | outcome |
|------|----------------|------------------|---------|
| sequential (in-dist) | prior tail = true tail | yes | bounded-risk win |
| sequential (shift) / real conjectures | prior tail ≥ true tail | no | unbounded miss |
| robustness | tail ≤ s× | up to s | safe with a compute price |
| cosmology | a windowed signal exists | no (sub-% coupling) | worse |
| changepoint (Nile) | a localized shift exists | yes | strongly better |
| changepoint (null) | a localized shift exists | no | not selected |

One law fits all six rows: **MTP earns its keep exactly to the degree its
assumption is true, and its failure mode is always assumed-not-earned.**

## What this is / is not

- **Is:** a method for choosing where to stop verifying, with a *provable risk
  knob when the counterexample/structure scale is bounded*, and a clear, named
  failure mode (prior misspecification / unbounded tails) when it is not.
- **Is not:** a universal compression principle, a law of physics, or a proof
  technique. It does not tell you *whether* a hypothesis is true; it tells you
  *how much it costs to be a given amount of wrong*.

## Suggested titles (verification-science framing, not physics)

- *Risk-Bounded Verification Stopping*
- *Overhead Boundaries in Sequential Refutation*
- *A Cross-Domain Framework for Verification Efficiency*
- *Entropy-Aware Verification under Bounded Risk*

## Reproduce

```bash
python run_scorecard.py                  # 4-domain efficiency table
python adapters/sequential.py            # overhead boundary + risk bound + shift
python adapters/real_conjectures.py      # historical validation
python adapters/robustness.py            # robustness frontier
python adapters/changepoint.py           # earned vs assumed structure (real Nile)
```
