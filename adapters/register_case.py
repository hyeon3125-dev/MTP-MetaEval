"""
register_case — a within-speaker case study: 'everyday' fails a third time.

A within-speaker self-experiment (one author, casual vs technical messages from a
single working session) measured five register proxies. This module re-analyses
ONLY the derived metrics (no raw utterances are stored here -- the session text
contains personal and IP-sensitive material and is deliberately excluded). It
fixes the original analysis (which used a hand-weighted composite + arbitrary
threshold and classified everything 'non-everyday') by reporting per-proxy
separation instead.

Finding: for this speaker the *register-complexity* proxies (lexical diversity,
sentence length, compressibility) do NOT separate casual from technical text; only
the *surface-lexicon* proxies (slang density, jargon density) do. So 'everyday'
here is not a difference in cognitive register -- only in surface vocabulary. This
is the non-circular result (labelling samples by technical topic makes 'jargon
separates' nearly tautological; the informative fact is that everything else fails).

It also exposes a THIRD level of assumed-not-earned: the everyday proxies are
calibrated to a population prior ('everyday speech = low complexity') that does not
hold for an atypical speaker. The instrument that measures whether structure is
earned must itself be calibrated to the real distribution -- the same recursion as
the detector self-test (earned_threshold) and the prior-match condition
(sequential).
"""
from __future__ import annotations

import os

# Derived metrics only (from the within-speaker experiment). NOT raw text.
# Each: (label, group, compression, colloquial_pct, tech_density, ttr, sent_len)
ROWS = [
    ("casual_A",        "casual",    0.688,  9.7, 0.000, 0.952, 31.0),
    ("casual_B",        "casual",    0.749,  5.3, 0.000, 1.000,  9.5),
    ("technical_1",     "technical", 0.872,  0.0, 0.554, 0.982, 11.4),
    ("technical_2",     "technical", 0.743,  0.0, 0.218, 0.836, 55.0),
    ("technical_3",     "technical", 0.826,  0.0, 0.080, 0.880, 17.3),
    ("mixed",           "mixed",     0.703,  7.0, 0.000, 1.000, 43.0),
]
# Proxy -> (column index, kind). 'surface' = vocabulary on the surface;
# 'register' = cognitive/syntactic complexity (the axis 'everyday' should track).
PROXIES = [
    ("compression",  2, "register"),
    ("colloquial%",  3, "surface"),
    ("tech_density", 4, "surface"),
    ("TTR",          5, "register"),
    ("sentence_len", 6, "register"),
]


def _vals(group, idx):
    return [r[idx] for r in ROWS if r[1] == group]


def analyse():
    out = []
    for name, idx, kind in PROXIES:
        c = _vals("casual", idx)
        t = _vals("technical", idx)
        c_lo, c_hi = min(c), max(c)
        t_lo, t_hi = min(t), max(t)
        overlap = not (c_hi < t_lo or t_hi < c_lo)        # ranges overlap?
        mean_gap = abs(sum(t) / len(t) - sum(c) / len(c))
        separates = not overlap
        out.append(dict(proxy=name, kind=kind, casual_mean=sum(c) / len(c),
                        tech_mean=sum(t) / len(t), mean_gap=mean_gap,
                        overlap=overlap, separates=separates))
    return out


def main():
    rows = analyse()
    print("=" * 76)
    print("  Within-speaker register case study (derived metrics only)")
    print("  casual vs technical text from ONE author; does each proxy separate them?")
    print("=" * 76)
    print(f"  {'proxy':<14}{'kind':<10}{'casual':>9}{'technical':>11}{'gap':>8}{'separates?':>12}")
    print("-" * 76)
    for r in rows:
        print(f"  {r['proxy']:<14}{r['kind']:<10}{r['casual_mean']:>9.3f}"
              f"{r['tech_mean']:>11.3f}{r['mean_gap']:>8.3f}   "
              f"{('YES' if r['separates'] else 'no (overlap)'):<12}")

    surface_sep = [r for r in rows if r["kind"] == "surface" and r["separates"]]
    register_sep = [r for r in rows if r["kind"] == "register" and r["separates"]]
    print(f"\n  Surface-lexicon proxies that separate : "
          f"{[r['proxy'] for r in surface_sep]}")
    print(f"  Register-complexity proxies that separate: "
          f"{[r['proxy'] for r in register_sep] or 'NONE'}")
    print("\n  Reading:")
    print("   - Only the SURFACE-lexicon proxies (slang%, jargon density) separate")
    print("     casual from technical. The REGISTER-complexity proxies (lexical")
    print("     diversity, sentence length, compressibility) do NOT.")
    print("   - So for this speaker 'everyday' is not lower cognitive register --")
    print("     only different surface vocabulary. The classic assumption")
    print("     'everyday speech = low complexity' is false here.")
    print("   - Non-circular: samples were labelled by technical TOPIC, so 'jargon")
    print("     separates topics' is near-tautological; the informative result is")
    print("     that everything ELSE fails to separate.")
    print("\n  THIRD level of assumed-not-earned:")
    print("   - 'hard' was undefined (capability vector); 'everyday' was undefined")
    print("     (info-content axis); and now the everyday PROXIES are themselves")
    print("     calibrated to a population prior (everyday=low-complexity) that does")
    print("     not hold per-speaker. The instrument measuring 'earned' must itself")
    print("     be earned -- the same recursion as the detector self-test and the")
    print("     prior-match condition. The law applies to its own measuring tools.")

    print("\n  Caveats (this is an illustrative n=5 case study, not statistics):")
    print("   - the original hand-weighted composite + 0.35 threshold are dropped")
    print("     (post-hoc weighting is itself assumed-not-earned); per-proxy only.")
    print("   - gzip ratio is confounded by character-set entropy (Greek letters /")
    print("     math symbols inflate it), so it tracks notation, not information.")
    print("   - whitespace tokenization distorts Korean (agglutinative); a morpheme")
    print("     analyzer would sharpen TTR / deixis. Raw session text is excluded")
    print("     for privacy/IP; only derived metrics are stored.")

    res = os.path.join(os.path.dirname(__file__), "..", "results")
    os.makedirs(res, exist_ok=True)
    import csv
    with open(os.path.join(res, "register_case.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["proxy", "kind", "casual_mean",
                                          "tech_mean", "mean_gap", "separates"])
        w.writeheader()
        for r in rows:
            w.writerow({k: r[k] for k in
                        ["proxy", "kind", "casual_mean", "tech_mean", "mean_gap", "separates"]})
    print("\nWrote: results/register_case.csv")


if __name__ == "__main__":
    main()
