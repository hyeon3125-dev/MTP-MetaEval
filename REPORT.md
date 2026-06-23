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

### 7.1 Live application — the capability-measurement problem (why "LLM saturation" is ill-posed)

This section is **not** a verdict on whether LLMs have saturated. It is the sharper,
*metrology* claim: **"capability saturation" is not a well-formed statement without a
capability metric, and no cross-vendor capability metric exists** — so the
pro-saturation and the anti-saturation positions are *both* assumed-not-earned. As
in physics, an unmeasurable quantity is an undefined one; here, "Capability
Saturation" presupposes a "Capability Metric" that has not been built. Applying the
overhead boundary to LLM *generations* is the lens that surfaces this: the verdict is
clean only on the one axis we actually instrument, and that axis is not capability.

The one exact ingredient is LMArena's own Elo→blind-win-rate map,
`P(win) = 1/(1+10^(−ΔElo/400))` (100 Elo → 0.640; identity, no data). Pre-registered
perceptibility floors: "barely perceptible" at a 55% win-rate (ΔElo ≥ 35),
"noticeable" at 60% (≥ 70). Real per-model Elo are cited, not invented (openlm.ai /
arena.ai overall leaderboard, June 2026).

**(1) The one axis we measure — aggregate blind preference — has gone flat.** Note
this axis is *everyday-text preference*, not capability. The real overall/text top-10
spans **14 Elo** (Fable 5 = 1510 down to Grok-4.20 = 1496), so the largest adjacent
gap is **~7 Elo → ~51% blind preference** — well below the 35-Elo floor. The
per-generation marginal gain on this axis has *crossed* the floor over time:

| transition | ΔElo | blind win | regime |
|---|---:|---:|---|
| GPT-3.5 → GPT-4 (2023) | ~100 | 0.64 | earned |
| GPT-4 → GPT-4o / Claude 3.5 (2024) | ~50 | 0.57 | earned |
| 2025–26 adjacent frontier | ~4–14 | ~0.51 | **overhead** |

On the median everyday prompt, recent frontier improvement is in the overhead
region: capability is still bought, perceptible marginal difference ≈ 0.

**(2) But the verdict is a projection — quantified.** "Still earned on *hard*
tasks" is under-specified; that under-specification is the finding. **Capability is
a vector, not a scalar**, and the verdict is a projection onto one axis. On the
**coding** projection the *same* frontier spans **~256 Elo** (top tier 1310–1566) —
**18× the overall spread** — so there the models are clearly distinguishable
(earned). Of seven capability axes the overhead verdict is *measurable* on three
(all text) and *undetermined / unmeasurable* on four:

| capability axis | cross-vendor metric? | verdict |
|---|---|---|
| everyday text (aggregate Elo) | yes | overhead |
| coding / math (text) | partial (SWE-bench, AIME) | re-ranked → earned on-axis |
| agentic / tool-use | weak (τ²-Bench, bespoke) | undetermined |
| long-context fidelity | weak | undetermined |
| multimodal (vision/audio/video) | fragmented, not unified | unmeasurable |
| vendor-specific architecture | none (incomparable) | ill-posed |

Verifiable, cited: Arena category leaderboards *re-rank* models (overall #1 can be
#5 in coding), the leader tops no single automated benchmark, and benchmarks are
fragmented (HLE, ARC-AGI-2, AIME, FrontierMath, SWE-bench, τ²-Bench) with no
vendor-neutral basis, least of all for multimodal. So **"has scaling entered
overhead?" is ill-posed without naming the projection.** Asserting *global*
overhead from aggregate Elo is itself **assumed-not-earned** — it assumes one
easy-text projection captures the whole vector.

**(3) Even "everyday" is unmeasured — the confound** (`adapters/info_content.py`).
"Everyday text" was itself a colloquial proxy. The real axis is information-theoretic
— the **shared context** between sender and receiver — measurable by deictic density
(falls monotonically casual→formal), lexical diversity, and most faithfully LM
perplexity. High-shared-context prompts have a *narrow correct-answer space — low
capability-SNR by construction* — so competent models tie there regardless of
saturation. The aggregate verdict thus **conflates (a) capability saturation with
(b) a prompt mix dominated by low-information tasks**, and Arena does not stratify
by information content, so it cannot separate them. For the saturation question the
benchmark is, in this respect, *broken* — an uncontrolled mixture. The defensible
claim is only "adjacent models tie on the aggregate mixture," **not** "capability
has saturated"; the earned claim needs stratified evaluation (do gaps shrink across
generations *within* high-information strata?).

**(4) Third level — even the proxies are prior-calibrated** (`adapters/register_case.py`).
A within-speaker case study (one author, casual vs technical text, derived metrics
only) shows that for a high-baseline writer only the *surface-lexicon* proxies
(slang, jargon density) separate casual from technical; every *register-complexity*
proxy (lexical diversity, sentence length, compressibility) fails. The population
prior "everyday speech = low complexity" is false here, so the instrument that
measures whether structure is earned is *itself* prior-calibrated and can be
assumed-not-earned — the same recursion as the §6.1 detector self-test.

**Falsifiable predictions** (`docs/llm_overhead.md`): hard-category Elo gaps stay
above the floor while overall stays below; any >35-Elo *overall* gap refutes the
flatness on that axis for that step; re-weighting Arena toward hard prompts widens
adjacent gaps back above the floor. This is the framework's most load-bearing
application — and a **metrology** result, not a saturation verdict: the same
assumed-not-earned law that judged a dark-energy model shows that "capability
saturation" is undefined until a cross-vendor capability metric exists, and that the
measurement gap recurs at three nested levels (axis, info-content, proxy), each of
which must itself be earned. The contribution is the *capability-measurement
problem*, not a position in the scaling debate.

## 7.2 Scope: demonstrations vs contributions

To avoid overclaiming: the RH-scanner and control-loop domains are **construction-
flagged demonstrations**, not contributions — they illustrate the floor where a
win is near-tautological. The load-bearing evidence is the un-flagged, ground-truth
work: the bounded-risk theorem and its failure (§2–3), the historical record (§4),
the cosmology negative and Nile positive cases with the SNR threshold (§5–6.1), and
the LLM application (§7.1). The contribution is the **cross-domain synthesis**, the
**falsification discipline** (pre-registration, honest negatives, construction
flags, no fabricated numbers), and the **assumed-not-earned law** — not a new
theorem in any single domain.

## 7.3 Related work

This sits at the confluence of mature fields and claims novelty only in their
synthesis and disciplined application, not in their theory:

- **Optimal stopping / sequential analysis** — Wald's SPRT (1945); optimal
  stopping (Chow–Robbins–Siegmund 1971); Bayesian sequential decision theory. The
  overhead boundary `q(t) ≤ ε` is a Bayesian stopping rule; §2's bound is a
  standard risk identity. Our framing adds the *cross-domain* read and the
  assumed-not-earned failure analysis.
- **Model selection / complexity** — AIC (Akaike 1974), BIC (Schwarz 1978), MDL
  (Rissanen 1978). The efficiency metric `phenomena/(params+assumptions+compute)`
  is an explicit, transparent cousin; §6 uses AIC + permutation calibration.
- **Thermodynamics of computation** — Landauer (1961), Bekenstein (1981): the
  entropy floor that makes "stop accumulating" physically, not just statistically,
  motivated (the RH demonstration's premise).
- **Resampling / multiple comparisons** — Fisher permutation tests; the §6.1
  result that a searched changepoint must be null-calibrated is the classic
  selective-inference hazard.
- **LLM evaluation & scaling** — Chatbot Arena / LMArena (Chiang et al. 2024) for
  the Elo↔win-rate map; neural scaling laws (Kaplan et al. 2020; Hoffmann et al.
  2022 "Chinchilla"); the benchmark-saturation and emergent-ability debates. §7.1's
  contribution is to reframe the scaling debate as a *capability-measurement
  (metrology) problem* — "saturation" is undefined without a cross-vendor metric —
  rather than to take a side on whether scaling has stalled.

What is new here is not any of these tools but the demonstration that **one
assumed-not-earned law** organizes verification-stopping *and* structure-adding
across number theory, physics, control, statistics, and LLM evaluation — under a
pre-registered, fabrication-averse protocol that reports its own negatives.

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
python adapters/llm_overhead.py          # §7.1 the capability-measurement problem
```

Navigation: [README](README.md) · [PREREGISTRATION](PREREGISTRATION.md) ·
[worklog](worklog.md) · docs/[overhead_boundary](docs/overhead_boundary.md) ·
docs/[real_conjectures](docs/real_conjectures.md) · `results/`.

## Cite

> Lee, Seung-hyun. *Assumed-not-Earned: Verification Efficiency under Bounded
> Risk.* 2026. Zenodo. DOI: [10.5281/zenodo.20806118](https://doi.org/10.5281/zenodo.20806118).

Concept DOI `10.5281/zenodo.20806118` (always resolves to the latest version);
v0.1 version DOI `10.5281/zenodo.20806119`. Machine-readable metadata in
[CITATION.cff](CITATION.cff).
