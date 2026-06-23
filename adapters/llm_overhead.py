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

  openlm.ai/chatbot-arena (overall/text, June 2026), real per-model Elo: the top-10
  spans just 14 Elo (Claude Fable 5 1510 .. Grok-4.20 1496); the all-time-low
  successive-leader gap was ~4 Elo (2025-02). The coding category top tier spans
  ~256 Elo over the same models -> the verdict is per-axis.
  (https://openlm.ai/chatbot-arena/ , https://benchlm.ai/llm-leaderboard-history)

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
    ("2026-06  adjacent (top-10)", 7.0),      # real: max adjacent gap in the top-10
]

# Real Arena overall/text top-10 (openlm.ai/chatbot-arena, June 2026), exact Elo.
OVERALL_TOP10 = [
    ("Claude Fable 5", 1510), ("Claude Opus 4.8 Thinking", 1506),
    ("GPT-5.5-high", 1506), ("Claude Opus 4.7 Thinking", 1505),
    ("Gemini-3.1-Pro", 1505), ("Claude Opus 4.8", 1504),
    ("Gemini-3.5-Flash", 1504), ("Claude Opus 4.7", 1503),
    ("Claude Opus 4.6 Thinking", 1503), ("Grok-4.20", 1496),
]
# Coding category top tier spans ~1310-1566 (same source): a far wider spread on
# the coding projection than on overall -> projection-dependence, quantified.
CODING_TOP_TIER_RANGE = (1310.0, 1566.0)


def projection_contrast():
    elos = [e for _, e in OVERALL_TOP10]
    overall_spread = max(elos) - min(elos)
    adj = [elos[i] - elos[i + 1] for i in range(len(elos) - 1)]
    max_adj = max(adj)
    coding_spread = CODING_TOP_TIER_RANGE[1] - CODING_TOP_TIER_RANGE[0]
    print("\n  Projection-dependence, QUANTIFIED (real Arena Elo, June 2026):")
    print(f"    overall/text top-10 spread : {overall_spread:.0f} Elo "
          f"(max adjacent {max_adj:.0f} Elo -> win {winrate(max_adj):.3f})")
    print(f"    coding top-tier spread     : {coding_spread:.0f} Elo "
          f"(top-vs-floor win {winrate(coding_spread):.3f})")
    print(f"    -> the SAME frontier is indistinguishable on everyday text "
          f"({overall_spread:.0f} Elo) but")
    print(f"       {coding_spread/overall_spread:.0f}x more spread on coding "
          f"({coding_spread:.0f} Elo) — overhead on one axis, earned on another.")
    return overall_spread, max_adj, coding_spread

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

    elos = [e for _, e in OVERALL_TOP10]
    overall_spread = max(elos) - min(elos)
    per_gap = max(elos[i] - elos[i + 1] for i in range(len(elos) - 1))
    print(f"\n  Real anchor (openlm.ai/chatbot-arena overall/text, June 2026):")
    print(f"    top 10 within {overall_spread:.0f} Elo "
          f"({OVERALL_TOP10[0][0]} {elos[0]:.0f} .. {OVERALL_TOP10[-1][0]} {elos[-1]:.0f})")
    print(f"    => max adjacent gap {per_gap:.0f} Elo  ->  blind win-rate "
          f"{winrate(per_gap):.3f}")
    floor55 = elo_for_winrate(0.55)
    verdict = "INSIDE the overhead region" if per_gap < floor55 else "outside"
    print(f"    adjacent gap {per_gap:.0f} < barely-perceptible floor "
          f"{floor55:.1f}  ->  {verdict}")

    print("\n  Marginal gain per generation (trend; gaps approximate, cited sources):")
    print(f"    {'transition':<38}{'dElo':>7}{'win':>8}{'>55% floor?':>13}")
    for name, g in HISTORICAL_GAPS:
        flag = "earned" if g >= floor55 else "OVERHEAD"
        print(f"    {name:<38}{g:>7.1f}{winrate(g):>8.3f}{flag:>13}")

    print("\n  VERDICT (aggregate / everyday-prompt distribution):")
    print(f"    Top-10 frontier within {overall_spread:.0f} Elo, adjacent ~{per_gap:.0f} Elo")
    print(f"    (~{winrate(per_gap):.0%} blind preference) — below the 55% perceptibility")
    print("    floor. On the median user prompt, recent generations are in the")
    print("    overhead region: capability is still bought, perceptible gain ~0.")

    projection_contrast()

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
        w.writerow(["2026-06 adjacent (top-10)", f"{per_gap:.1f}",
                    f"{winrate(per_gap):.3f}", f"{floor55:.1f}", "overhead"])
    print("\nWrote: results/llm_overhead.csv")


if __name__ == "__main__":
    main()
