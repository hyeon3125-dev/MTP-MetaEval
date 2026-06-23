# Verification efficiency under bounded risk — a cross-domain report

> **Thesis.** Verification efficiency is purchased with assumptions. The value of
> a verification shortcut is exactly proportional to the degree those assumptions
> match reality.

Every experiment below supports that one sentence. Read it as the spine; the
sections are success → failure → real-world failure → another failure →
real-world success → the general law.

## 0. What field is this?

Not physics, not pure mathematics, not control engineering — those are
*application instances*. The subject is:

```yaml
field:
  primary:   [computational verification, statistical decision theory, reliability engineering]
  secondary: [model selection, uncertainty quantification]
```

The question is never "is this hypothesis true?" but **"when should verification
stop, given a cost of checking and a risk of being wrong?"** Cosmology is "how
much do we verify a model," RH is "when to stop searching for a counterexample,"
control is "when does another sample stop adding information." The unit of study
is the **verification system**; the metric is efficiency under a *bounded risk of
misjudgment*.

Pre-registration (`PREREGISTRATION.md`) fixes every definition, baseline, and
tolerance before any result; numbers are parsed mechanically from real runs (one
disclosed amendment). The four-domain efficiency scorecard (`run_scorecard.py`)
is the quantitative backbone; this report is its narrative.

## 1. The claim

The MTP principle, stated as a verification rule: *accumulate evidence only up to
a non-refutation / precision floor; past it, marginal information gain falls below
marginal entropy cost (Landauer), so further checking is waste.* The **overhead
boundary** `t_floor(ε)` is the operational object: after surviving `[0, t)` with
no counterexample, the posterior that one remains is `q(t)`; stop when `q(t) ≤ ε`.

The claim is that stopping there is *efficient*. The rest of the report asks the
only question that matters: **when is it also correct?**

## 2. Success — the floor has provably bounded risk (`docs/overhead_boundary.md`)

On a population of conjectures with a *known, correctly-modeled* counterexample
tail, the floor obeys a theorem, verified to the digit:

> `miss_rate ≤ ε(1−π0)`  —  e.g. ε=0.01 → empirical miss 0.0052, at ~94% compute saved.

So "keep searching, stop at a principled floor" is **not nihilism**: you save
>90% of the work with a misjudgment probability you set in advance. The overhead
boundary is real and risk-controlled — *when the assumption is right.*

## 3. Failure — the same floor under a wrong assumption

Make the true counterexample tail 4× heavier than the prior expects. The floor
keeps "saving" 93% of compute but the miss rate jumps to **0.16 — ~31× its
bound**. The risk knob silently lies. The robustness frontier
(`adapters/robustness.py`) shows it breaks at a tail only **2×** heavier, and that
a conservative floor buys safety up to heaviness `s` only by giving back compute
(s=1→94.5%, s=8→63% saved). **Robustness buys range, never invulnerability.**

## 4. Real-world failure — the historical record (`docs/real_conjectures.md`)

Section 3 is not contrived; it is the norm. Of four famous **disproven**
conjectures, an efficient floor would have endorsed **all four** as "non-refuted":

| conjecture | counterexample | floor outcome |
|---|---|---|
| Pólya | n ≈ 9×10⁸ | misses (far past "settled") |
| Euler n=5 | 144⁵ | misses |
| Mertens | beyond all computation (≤ e^(1.59×10⁴⁰)) | misses — only a *proof* found it |
| π(x)<li(x) | ≈ 1.4×10³¹⁶ | misses — only a *proof* found it |

Collatz and Goldbach (true to 10²⁰, 10¹⁸) are correctly endorsed by stopping. The
lesson is sharp: **non-refutation stopping is safe only given a *proven bound* on
where a counterexample can live.** RH has no such bound — so the RH-domain "win"
in the scorecard (already construction-flagged) is the *same unbounded gamble* as
Mertens and Skewes.

## 5. Negative case — cosmology (`MTP-Cosmology`)

Now the other face of the same law: not stopping, but *adding structure*. The
windowed-IDE model adds a localized dark-sector coupling — an *assumed* structural
feature. Across DESI DR1 BAO + Gold-2018 RSD + Planck distance priors the data
drive the coupling to zero; the model never beats ΛCDM on AIC/BIC, and its
scorecard efficiency ratio is ≈0.02 (worse). The assumed structure was not in the
data, so it was pure cost.

## 6. Positive case — earned structure on real data (`adapters/changepoint.py`)

The *same* "add a localized (windowed) structure" move, on the real Nile series
(1871–1970), which has a documented 1899 regime shift (Aswan dam). Here the
structure **is** real: a changepoint model selects index 28 (year 1899) with
**ΔAIC = −53, permutation p < 0.001**, and is **not** selected under a shuffled
null. Identical move, opposite verdict — decided entirely by whether the structure
exists.

### 6.1 One curve, not two anecdotes (`adapters/earned_threshold.py`)

Cosmology (assumed, lost) and Nile (earned, won) are the two ends of a single
quantity — the **signal-to-noise ratio** of the localized structure. Sweeping SNR
(noise calibrated to Nile's within-segment scatter) gives a detection-power curve
with a threshold: null-calibrated power crosses 95% at **SNR ≈ 0.9**. Nile sits at
SNR ≈ 2.0 (power ~1.0); cosmology's windowed signal was sub-percent versus the
data errors, i.e. SNR ≪ 1, below threshold. *Assumed-vs-earned is position on this
curve, not a binary.* (`results/earned_threshold.png`.)

A self-referential bonus: the **detector must itself be earned**. Naive AIC<0
selects the localized model **~48% of the time from pure noise** — the
changepoint-location search overfits and AIC doesn't penalize it — so the
detection method falls into the *same* assumed-not-earned trap, fixed only by
calibrating against the null (the permutation test). The verification of "is this
structure earned?" is itself a verification that can be assumed-not-earned.

## 7. The general law

| test | MTP assumption | matches reality? | outcome |
|------|----------------|------------------|---------|
| sequential (in-dist) | prior tail = true tail | yes | bounded-risk win |
| sequential shift / real conjectures | prior tail ≥ true tail | **no** | unbounded miss |
| robustness | tail ≤ s× | up to s | safe at a compute price |
| cosmology | a windowed signal exists | **no** | worse |
| changepoint (Nile) | a localized shift exists | yes | strongly better |
| changepoint (null) | a localized shift exists | **no** | not selected |

Six rows, one law:

> **MTP earns its keep exactly to the degree its assumption is true, and its
> failure mode is always *assumed-not-earned*.**

Whether the MTP move is a *stopping floor* (sections 2–4) or an *added structure*
(sections 5–6), the value tracks the assumption-reality match, and the failure is
always the same: a structure or bound believed but not present. The risk knob and
the AIC gain are both only as good as that match — and §6.1 shows the law even
applies *to the detector*: deciding whether structure is earned is itself a
verification that must be null-calibrated, or it manufactures structure from noise
half the time.

### 7.1 Live application — has LLM capability entered the overhead region? (`adapters/llm_overhead.py`)

The same overhead boundary, with model *generations* as the accumulation axis.
The only exact ingredient is LMArena's own Elo→blind-win-rate map,
`P(win) = 1/(1+10^(−ΔElo/400))` (100 Elo → 0.640). Pre-registered perceptibility
floors: a difference is "barely perceptible" at a 55% win-rate (ΔElo ≥ 35),
"noticeable" at 60% (≥ 70).

Real, *structural* anchor (cited, not invented per-model scores): as of June 2026
the LMArena top tier is clustered within **~55 Elo — the tightest spread on
record** (the successive-leader gap hit an all-time low of ~4 Elo in 2025-02).
That puts adjacent frontier models ~14 Elo apart → **~52% blind preference**,
*below* the 55% floor. The per-generation marginal gain has crossed the floor:
GPT-3.5→GPT-4 was ~100 Elo (earned); 2025–26 adjacent gaps are ~4–14 Elo
(overhead). **On the median everyday prompt, recent frontier improvement is in the
overhead region — more capability bought, ~zero perceptible marginal difference.**

This is *not* a universal capability ceiling — it is the §6.1 SNR law per task.
Overall Elo averages over mostly-easy prompts (low capability-SNR → imperceptible);
on hard distributions (frontier math, agentic coding, long-context, tool-use) the
SNR is high and the gaps are still earned. "Overhead entered" is true for commodity
use, false for frontier-hard use. Caveats (Elo ≠ capability; aggregate ≠ per-task;
benchmark saturation is a measurement ceiling) are in `docs/llm_overhead.md`. This
is the framework's most load-bearing application: the same assumed-not-earned /
overhead-boundary law that judged a dark-energy model now dates the diminishing
returns of LLM scaling — and locates them precisely on the easy-task axis.

## 8. What this is / is not

- **Is:** a method for choosing where to stop verifying (or how much structure to
  posit), with a *provable risk knob when the counterexample/structure scale is
  bounded*, and one clearly named failure mode — *assumed-not-earned* — when it is
  not. A calibrated way to spend compute against risk.
- **Is not:** a universal compression principle, a law of physics, or a proof
  technique. It does not tell you *whether* a hypothesis is true; it tells you
  *how much it costs to be a given amount of wrong*.

## 9. Suggested titles (verification-science framing)

- *Risk-Bounded Verification Stopping*
- *Overhead Boundaries in Sequential Refutation*
- *Assumed-not-Earned: When Verification Shortcuts Pay*
- *A Cross-Domain Framework for Verification Efficiency*

## 10. Reproduce

```bash
python run_scorecard.py                  # 4-domain efficiency table
python adapters/sequential.py            # §2-3 overhead boundary: bound + shift
python adapters/robustness.py            # §3 robustness frontier
python adapters/real_conjectures.py      # §4 historical validation
python adapters/changepoint.py           # §6 earned vs assumed structure (real Nile)
python adapters/earned_threshold.py      # §6.1 the SNR detection curve + threshold
python adapters/llm_overhead.py          # §7.1 overhead region in LLM capability
```

Navigation: [README](README.md) · [PREREGISTRATION](PREREGISTRATION.md) ·
[worklog](worklog.md) · docs/[overhead_boundary](docs/overhead_boundary.md) ·
docs/[real_conjectures](docs/real_conjectures.md) · `results/`.
