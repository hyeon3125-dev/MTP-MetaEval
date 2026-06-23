# The LLM capability-measurement problem

**Not a verdict on whether LLMs have saturated** — the sharper, *metrology* claim:
"capability saturation" is undefined without a cross-vendor capability metric, and
none exists, so both the pro- and the anti-saturation position are
assumed-not-earned (as in physics, an unmeasurable quantity is an undefined one).
Applying the overhead boundary (`docs/overhead_boundary.md`) to LLM *generations*
(floor = user-perceptible difference) is the lens that surfaces this: the verdict
is clean only on the one axis we instrument, and that axis is not capability.
`adapters/llm_overhead.py`.

## The one exact ingredient (no fabrication)

LMArena defines the blind pairwise win-rate from the Elo gap:

```
P(win) = 1 / (1 + 10^(-ΔElo/400))      # 100 Elo -> 0.640
```

Everything else is either pre-registered (the floor) or a *cited structural fact*
(the leaderboard spread). No invented per-model scores for preview models.

## Pre-registered perceptibility floor

A capability difference is perceptible only if blind preference clears a win-rate:

| floor | win-rate | required ΔElo |
|-------|---------:|-------------:|
| barely | 0.55 | 35 |
| noticeable | 0.60 | 70 |
| clear | 0.667 | 121 |

## Real anchor and verdict

openlm.ai / arena.ai overall/text leaderboard, June 2026 (real per-model Elo): the
**top-10 spans just 14 Elo** — Claude Fable 5 (1510) down to Grok-4.20 (1496) — so
the largest adjacent gap is **~7 Elo**. Sources:
[openlm.ai/chatbot-arena](https://openlm.ai/chatbot-arena/),
[benchlm.ai history](https://benchlm.ai/llm-leaderboard-history).

- Adjacent frontier models ~7 Elo apart → **~51% blind preference** → below the
  35-Elo (55%) floor → flat **on this everyday-text axis** (which is not capability).
- Marginal gain per generation, over time: GPT-3.5→GPT-4 ≈ 100 Elo (earned) →
  2024 ≈ 50 (earned) → 2025–26 ≈ 4–14 (overhead). The trend has crossed the floor.
- Projection contrast (same frontier): overall/text spread **14 Elo** vs **coding
  top-tier spread ~256 Elo** (1310–1566) — **18× wider** — so the models that tie on
  everyday text are clearly separated on coding. Overhead is per-axis (next section).

**Conclusion (scoped):** on the *one axis we measure* — aggregate everyday-text
blind preference — adjacent frontier models tie. That is a statement about this
measurement axis, **not** about capability: it does not say "scaling has saturated,"
because (next sections) capability is a vector whose other axes are unmeasured, the
"everyday" axis is itself an unmeasured proxy, and even the proxy is
prior-calibrated. The headline is the *measurement problem*, not a saturation
verdict.

## "Overhead" is a projection — and "hard" is not a defined metric

The naive next move is "but on *hard* tasks the gains are still earned." That is
under-specified, and the under-specification is the real finding. **Capability is
a vector, not a scalar**, and the overhead verdict is a *projection* onto one axis:

| capability axis | cross-vendor quantitative metric? | overhead verdict |
|-----------------|-----------------------------------|------------------|
| everyday text preference (aggregate Elo) | yes (Arena overall) | **OVERHEAD confirmed** |
| coding (text) | partial (Arena Coding, SWE-bench) | **re-ranked** → projection-dependent |
| math / reasoning (text) | partial (AIME, FrontierMath) | **re-ranked** → still earned on-axis |
| agentic / tool-use (end-to-end) | weak / non-comparable (τ²-Bench, bespoke) | **undetermined** |
| long-context retrieval fidelity | weak / non-comparable | **undetermined** |
| multimodal (vision/audio/video) | fragmented, **not** cross-vendor unified | **unmeasurable** |
| vendor-specific architecture features | none (incomparable by definition) | **ill-posed** |

Verifiable, citable facts (no invented scores): Arena category leaderboards
**re-rank** models — a model #1 overall can be #5 in coding; Claude gains on
Expert/Coding, Gemini on Vision/Multi-Turn, DeepSeek on Math/Reasoning — and the
Arena leader tops **no single automated benchmark**. Benchmarks are fragmented
across axes (HLE, ARC-AGI-2, AIME, FrontierMath, SWE-bench, τ²-Bench, …) with **no
unified, vendor-neutral basis**, least of all for **multimodal** capability.

Consequences:

1. **The verdict is projection-dependent.** Overhead is *confirmed* only on the
   everyday-text axis (where the prompt-distribution SNR is low — the §6.1 law);
   on specialist text axes the ordering changes, so the gaps are plausibly still
   earned; on the remaining axes there is **no measurement to project onto**.
2. **For most of the capability vector the question is unanswerable.** Agentic,
   long-context, and especially multimodal capability — and any vendor-specific
   architectural specialization — have no cross-vendor quantitative benchmark. The
   overhead boundary cannot be located on an axis no one measures comparably.
3. **Asserting *global* overhead from aggregate Elo is itself assumed-not-earned.**
   It assumes one easy-text projection captures the whole vector — the exact
   error this framework warns against. The disciplined claim is *scoped*: overhead
   is established on the measured everyday-text projection and is **undetermined**
   elsewhere, pending measurement infrastructure that does not yet exist.

So "hard" should be read not as a metric but as "axes where the capability-SNR is
high" — a set that is *incompletely enumerated and largely unmeasured across
vendors*. The honest research position is not "scaling is over" but "the question
is only decidable on the one axis we instrument, and building vendor-neutral
multimodal / agentic measurement is the prerequisite to deciding it anywhere else."

## The deeper confound: "everyday" is not measured either (`adapters/info_content.py`)

The verdict above is stated on the "everyday-text" projection — but **"everyday"
was a colloquial stand-in, not a measured quantity**, the *same* assumed-not-earned
trap as "hard." Information theory gives the real axis: the **shared context**
between sender and receiver. High shared context ⇒ the message can be short
(deictics, ellipsis); low shared context ⇒ the text must spell the context out
(definitions, proper nouns). The axis is measurable — deictic density falls
monotonically across registers (casual 0.35 → email 0.10 → news 0.06 → technical
0.02 → formal 0.00); lexical diversity and word length rise. (gzip ratio is a
*weak, non-monotone* proxy because it sees only in-text redundancy, not the
external shared context; the faithful measure is LM cross-entropy / perplexity —
i.e. the instrument is the same kind of object being judged.)

This exposes a confound in the overhead verdict. High-shared-context (everyday)
prompts have a **narrow correct-answer space — low capability-SNR by
construction**: competent models converge to nearly the same good answer, so they
*tie*. Therefore aggregate indistinguishability conflates **(a) capability
saturation** with **(b) a prompt mix dominated by low-information tasks**. Arena
preference is *not stratified by information content*, so it cannot separate (a)
from (b). **For the capability-saturation question, the measurement is, in this
respect, broken: an uncontrolled mixture.**

The missing measurement (and the honest claim): stratify prompts by an
info-content proxy (perplexity / deictic density / gzip), then test whether model
win-rate gaps shrink *across generations within the high-information strata*. Only
then is "capability has entered overhead" earned rather than an artifact of the
prompt distribution. Until that stratified evaluation exists, the defensible claim
is narrow: *on the aggregate blind-preference mixture, adjacent frontier models
are near-indistinguishable* — which is true, and is **not** the same as "capability
has saturated."

## A third level: the everyday proxies are themselves prior-calibrated (`adapters/register_case.py`)

A within-speaker self-experiment (one author, casual vs technical messages from a
single session; only derived metrics retained, raw text excluded for privacy/IP)
sharpens the point. Re-analysed per-proxy (dropping the original hand-weighted
composite, which is itself a post-hoc, assumed-not-earned choice):

| proxy | kind | casual | technical | separates? |
|-------|------|-------:|----------:|------------|
| slang density | surface | 7.5% | 0% | **yes** |
| jargon density | surface | 0.00 | 0.28 | **yes** |
| compressibility | register | 0.72 | 0.81 | no (overlap) |
| lexical diversity (TTR) | register | 0.98 | 0.90 | no (overlap) |
| sentence length | register | 20.3 | 27.9 | no (overlap) |

Only the **surface-lexicon** proxies separate casual from technical; every
**register-complexity** proxy fails. So for this speaker "everyday" is not a lower
cognitive register---only a different surface vocabulary. (The result is
non-circular precisely because samples were labelled by technical *topic*, which
makes "jargon separates topics" near-tautological; the informative fact is that
everything else fails.)

This is the **third level of assumed-not-earned** in the same measurement:
"hard" was undefined (capability vector); "everyday" was undefined (info-content
axis the benchmark does not stratify); and now the everyday *proxies themselves*
are calibrated to a population prior ("everyday speech = low complexity") that does
not hold for an atypical speaker. The instrument that measures whether structure is
earned must itself be earned---the same recursion as the detector self-test
(`earned_threshold.py`) and the prior-match condition (`sequential.py`). The law
applies to its own measuring tools, at every level.

Caveats: illustrative $n{=}5$, not statistics; gzip is confounded by character-set
entropy (Greek/math symbols inflate it, so it tracks notation not information);
whitespace tokenization distorts agglutinative Korean (a morpheme analyzer would
sharpen TTR/deixis).

## Caveats (non-overclaim)

- **Elo ≠ capability.** Arena measures aggregate blind *preference*, confounded by
  style, verbosity, and formatting — not pure problem-solving.
- **Aggregate ≠ per-task.** "Imperceptible on the median prompt" does not mean
  "equal capability." The hard-task tail can diverge sharply while the median ties.
- **Benchmark saturation is a measurement ceiling**, not a capability ceiling
  (MMLU ~90% reflects the test, not the model's headroom).
- **Preview-model scores are not used.** The verdict rests only on the cited
  clustering and the exact Elo→win-rate map; it is structural, not a ranking of
  specific unreleased models.

## Falsifiable predictions

1. Overall-Elo adjacent-frontier gaps stay ≤ ~35 Elo while **hard-category** gaps
   stay larger — overhead is easy-task-only.
2. If a future model opens a >35 Elo *overall* gap, the overhead claim is refuted
   for that step (the easy-task SNR rose, i.e. the median prompt got
   discriminating again — unlikely without harder default prompts).
3. Re-weighting Arena toward hard prompts widens adjacent gaps back above the
   floor — the overhead is a property of the *prompt distribution*, not the models.
