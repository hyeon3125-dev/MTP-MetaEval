"""
llm_overhead — the overhead boundary applied to LLM capability accumulation.

Question: has frontier-model improvement entered the OVERHEAD REGION — where the
marginal capability gain per generation has fallen below the threshold of
user-PERCEPTIBLE difference? This is the project's overhead boundary
(docs/overhead_boundary.md) with a different accumulation axis: not zeros or
samples, but model generations / training compute.

This analysis is STRUCTURAL and non-fabricating. The only exact ingredient is the
Arena Elo -> blind-win-rate map (LMArena's own definition):

    P(win) = 1 / (1 + 10^(-dElo/400))           # 100 Elo -> 0.640 (cited)

The perceptibility FLOOR is pre-registered, not tuned. Real-world input is the
*structural* leaderboard fact, cited, not invented per-model scores:

  LMArena / arena.ai, June 2026: the top tier is clustered within ~55 Elo — the
  tightest spread on record; the all-time-low successive-leader gap was ~4 Elo
  (2025-02). (https://openlm.ai/chatbot-arena/ , https://benchlm.ai/llm-leaderboard-history)

Heavy caveats are in main() and REPORT — Elo is aggregate blind preference over
mostly-everyday prompts; "imperceptible" means on the median prompt, NOT that
capability is equal. That task-dependence IS the §6.1 SNR law.
"""
from __future__ import annotations

import math
import os

# Pre-registered perceptibility floors (Elo gaps), via the win-rate map.
def winrate(dElo: float) -> float:
    return 1.0 / (1.0 + 10 ** (-dElo / 400.0))


def elo_for_winrate(p: float) -> float:
    return -400.0 * math.log10(1.0 / p - 1.0)


# A difference is "perceptible" if blind preference clears these win-rates.
FLOOR_WINRATES = {"barely (55%)": 0.55, "noticeable (60%)": 0.60, "clear (67%)": 0.667}

# Real structural anchors (cited). Adjacent-frontier gaps over time, approximate
# and used only for the trend; the conclusion rests on the clustering, not exact
# per-model scores.
HISTORICAL_GAPS = [
    ("2023-03  GPT-3.5 -> GPT-4", 100.0),     # GPT-4 launched ~100+ Elo above 3.5
    ("2024     GPT-4 -> GPT-4o/Claude3.5", 50.0),
    ("2025-02  successive-leader low", 4.0),  # cited all-time low
    ("2026-06  top-5 cluster (per-gap)", 55.0 / 4),  # ~55 Elo across top 5 -> ~14/gap
]

TOP_TIER_SPREAD_2026 = 55.0    # cited: top tier within ~55 Elo (June 2026)
TOP_TIER_N = 5

# Capability is a VECTOR, not a scalar. The overhead verdict is a projection onto
# an axis, and the axes are measured very unequally. Fields: (axis, cross-vendor
# quantitative benchmark?, what the overhead verdict can be). Verifiable
# qualitative facts only — no invented per-model scores.
#   Cited: Arena category leaderboards RE-RANK models (overall #1 can be #5 in
#   coding; Claude->Expert/Coding, Gemini->Vision/Multi-Turn, DeepSeek->Math).
#   The Arena leader tops no single automated benchmark. Benchmarks are
#   fragmented (HLE, ARC-AGI-2, AIME, FrontierMath, SWE-bench, tau2-Bench, ...).
CAPABILITY_AXES = [
    # axis, measured cross-vendor?, verdict basis
    ("everyday text preference (aggregate Elo)", "yes (Arena overall)",
     "OVERHEAD confirmed (~14 Elo adjacent, 52% pref)"),
    ("coding (text)", "partial (Arena Coding, SWE-bench)",
     "RE-RANKED vs overall -> projection-dependent; plausibly still earned"),
    ("math / reasoning (text)", "partial (AIME, FrontierMath, Arena Math)",
     "RE-RANKED; specialist models lead -> earned on this axis"),
    ("agentic / tool-use (end-to-end)", "weak / non-comparable (tau2-Bench, bespoke)",
     "UNDETERMINED — no stable cross-vendor metric"),
    ("long-context retrieval fidelity", "weak / non-comparable",
     "UNDETERMINED — harnesses and context lengths differ per vendor"),
    ("multimodal (vision/audio/video) quality", "fragmented, NOT cross-vendor unified",
     "UNMEASURABLE at parity — no common basis"),
    ("vendor-specific architecture features", "none (by definition incomparable)",
     "ILL-POSED — the axis is not shared across vendors"),
]


def capability_vector_report():
    print("\n  Capability is a VECTOR; 'overhead' is a PROJECTION onto an axis.")
    print("  The axes are measured very unequally (cited: Arena categories re-rank")
    print("  models; the Arena leader tops no single automated benchmark):\n")
    print(f"    {'capability axis':<42}{'cross-vendor metric?':<24}verdict")
    measured = unmeasured = 0
    for axis, metric, verdict in CAPABILITY_AXES:
        head = verdict.split(" ")[0].rstrip(";")
        if head in ("UNDETERMINED", "UNMEASURABLE", "ILL-POSED"):
            unmeasured += 1
        else:
            measured += 1
        print(f"    {axis:<42}{metric[:23]:<24}{head}")
    print(f"\n  Of {len(CAPABILITY_AXES)} axes, the overhead verdict is *measurable* on "
          f"{measured} (all text)\n  and *undetermined / unmeasurable* on {unmeasured} "
          f"(agentic, long-context, multimodal,\n  vendor-specific) — no cross-vendor "
          f"quantitative basis exists for them.")
    print("\n  => 'has scaling entered overhead?' is ILL-POSED without naming the")
    print("     projection. It is CONFIRMED only on the everyday-text axis, RE-RANKED")
    print("     (so likely still earned) on specialist text axes, and UNANSWERABLE on")
    print("     the multimodal / agentic / vendor-specific axes for lack of measurement.")
    print("     Asserting GLOBAL overhead from aggregate Elo is itself assumed-not-earned:")
    print("     it assumes one easy-text projection captures the whole capability vector.")
    return measured, unmeasured


def main():
    print("=" * 74)
    print("  LLM capability: has frontier improvement entered the overhead region?")
    print("=" * 74)
    print("  Exact map: P(win) = 1/(1+10^(-dElo/400)).  100 Elo -> %.3f (cited).\n"
          % winrate(100))

    print("  Pre-registered perceptibility floors (Elo gap to clear):")
    for name, p in FLOOR_WINRATES.items():
        print(f"    {name:<18} P(win)={p:.3f}  ->  dElo >= {elo_for_winrate(p):5.1f}")

    per_gap = TOP_TIER_SPREAD_2026 / (TOP_TIER_N - 1)
    print(f"\n  Real anchor (LMArena, June 2026): top {TOP_TIER_N} within "
          f"~{TOP_TIER_SPREAD_2026:.0f} Elo (tightest on record)")
    print(f"    => adjacent-model gap ~{per_gap:.1f} Elo  ->  blind win-rate "
          f"{winrate(per_gap):.3f}")
    floor55 = elo_for_winrate(0.55)
    verdict = "INSIDE the overhead region" if per_gap < floor55 else "outside"
    print(f"    adjacent gap {per_gap:.1f} < barely-perceptible floor "
          f"{floor55:.1f}  ->  {verdict}")

    print("\n  Marginal gain per generation (trend; gaps approximate, cited sources):")
    print(f"    {'transition':<38}{'dElo':>7}{'win':>8}{'>55% floor?':>13}")
    for name, g in HISTORICAL_GAPS:
        flag = "earned" if g >= floor55 else "OVERHEAD"
        print(f"    {name:<38}{g:>7.1f}{winrate(g):>8.3f}{flag:>13}")

    print("\n  VERDICT (aggregate / everyday-prompt distribution):")
    print("    Adjacent frontier models now differ by ~14 Elo (~52% blind preference)")
    print("    — below the 55% perceptibility floor. On the median user prompt,")
    print("    recent generations are in the overhead region: more capability is")
    print("    being bought, but the marginal user-perceptible difference is ~0.")

    print("\n  BUT 'overhead' is per-axis, and 'hard' is not a defined metric ----")
    capability_vector_report()

    print("\n  CAVEATS (non-overclaim):")
    print("   - Elo = aggregate blind preference, dominated by everyday prompts;")
    print("     'imperceptible' != 'equal capability'.")
    print("   - Arena preference is confounded by style/verbosity, not pure capability.")
    print("   - Benchmark saturation (e.g. MMLU ~90%) is a measurement ceiling, not")
    print("     necessarily a capability ceiling.")
    print("   - Exact per-model scores for preview frontier models are not used; the")
    print("     conclusion rests on the cited clustering + the exact Elo->win-rate map.")

    res = os.path.join(os.path.dirname(__file__), "..", "results")
    os.makedirs(res, exist_ok=True)
    import csv
    with open(os.path.join(res, "llm_overhead.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["transition", "dElo", "winrate", "floor55", "regime"])
        for name, g in HISTORICAL_GAPS:
            w.writerow([name, f"{g:.1f}", f"{winrate(g):.3f}", f"{floor55:.1f}",
                        "earned" if g >= floor55 else "overhead"])
        w.writerow(["2026-06 adjacent (top-5 cluster)", f"{per_gap:.1f}",
                    f"{winrate(per_gap):.3f}", f"{floor55:.1f}", "overhead"])
    print("\nWrote: results/llm_overhead.csv")


if __name__ == "__main__":
    main()
