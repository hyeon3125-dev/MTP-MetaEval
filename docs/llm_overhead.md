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

## Why this is the §6.1 SNR law, not a ceiling

Overall Elo averages over a prompt mix dominated by easy/everyday queries — a
*low capability-SNR* regime where even large underlying capability gaps produce
near-coin-flip preferences. On hard distributions (frontier math, agentic coding,
long-context reasoning, tool-use) the capability-SNR is high and the gaps remain
earned (Arena's hard-prompt / coding category spreads are wider than the overall).
So "overhead entered" is **task-conditional**: position on the same detection curve
as `earned_threshold.py`, evaluated per task difficulty.

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
