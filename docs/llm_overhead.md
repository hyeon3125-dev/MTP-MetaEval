# The overhead region in LLM capability

Applying the overhead boundary (`docs/overhead_boundary.md`) to LLM progress, with
model *generations / training compute* as the accumulation axis and
*user-perceptible capability difference* as the floor. `adapters/llm_overhead.py`.

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

LMArena / arena.ai, June 2026: the top tier is clustered within **~55 Elo, the
tightest spread on record**; the successive-leader gap hit an all-time low of ~4
Elo (2025-02). Sources: [openlm.ai/chatbot-arena](https://openlm.ai/chatbot-arena/),
[benchlm.ai history](https://benchlm.ai/llm-leaderboard-history).

- Adjacent frontier models ≈ 14 Elo apart → **52% blind preference** → below the
  35-Elo (55%) floor → **inside the overhead region**.
- Marginal gain per generation, over time: GPT-3.5→GPT-4 ≈ 100 Elo (earned) →
  2024 ≈ 50 (earned) → 2025–26 ≈ 4–14 (overhead). The trend has crossed the floor.

**Conclusion (scoped):** on the distribution of everyday user prompts, recent
frontier improvement is in the overhead region — capability is still being bought
(compute, parameters, training), but the marginal *user-perceptible* difference is
≈ 0.

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
