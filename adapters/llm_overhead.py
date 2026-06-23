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

    print("\n  BUT — the task-dependence IS the §6.1 SNR law (NOT a universal ceiling):")
    print("    Overall Elo averages over mostly-easy prompts (low capability-SNR ->")
    print("    imperceptible). On HARD distributions (frontier math, agentic coding,")
    print("    long-context, tool-use) the capability-SNR is high and the gaps are")
    print("    still earned. 'Overhead entered' is true for commodity use, false for")
    print("    frontier-hard use — position on the same SNR curve, per task.")

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
