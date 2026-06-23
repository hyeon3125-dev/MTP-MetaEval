"""
info_content — "everyday" is not a measured axis either (the confound under §7.1).

The LLM overhead claim was stated on "everyday text." But "everyday" was a
colloquial stand-in, not a measured quantity -- the same assumed-not-earned trap
as "hard." Information theory gives the real axis: the SHARED CONTEXT between
sender and receiver. High shared context => the message can be short (deictics,
ellipsis); low shared context => the text must spell the context out (definitions,
proper nouns, full description).

This module demonstrates that the axis is MEASURABLE with deterministic proxies,
and argues the consequence: aggregate Arena preference does NOT stratify by it, so
"overhead on everyday text" conflates capability saturation with the prompt mix
being dominated by low-information (high-shared-context => low capability-SNR)
tasks. The benchmark, for the capability-saturation question, is confounded.

Proxies (all deterministic, no fabrication):
  - gzip ratio    : in-text redundancy only (no external knowledge).
  - deictic ratio : pronouns/demonstratives -- reliance on shared context.
  - type-token    : lexical diversity (specialist text introduces many terms).
  - mean word len : crude technical-vocabulary proxy.
The FAITHFUL measure of shared-context is LM cross-entropy / perplexity -- which a
language model computes directly. That a model is needed to measure the axis the
model is judged on is the point: the measurement instrument and the object are the
same kind of thing.
"""
from __future__ import annotations

import gzip
import os
import re

# Illustrative passages spanning high -> low shared context. Clearly samples for
# the proxy demonstration, NOT a benchmark. ~300-500 chars so gzip is meaningful.
CORPUS = [
    ("casual_chat (high shared context)",
     "ya did you see that thing yesterday? lol it was so them. anyway i told you "
     "it'd go like that, remember? same as last time. she said she'd handle it but "
     "you know how that goes. wanna grab the usual later? same place, same time. "
     "bring the stuff from before, we'll need it. it'll be fine, trust me, we got "
     "this. tell them i said hi and that the other thing is sorted now."),
    ("everyday_email (mid-high)",
     "Hi team, quick note on tomorrow. We'll meet at the usual room after lunch to "
     "go over the numbers. Please bring your updates and anything still open from "
     "last week. If you can't make it, just send your part to me beforehand and "
     "I'll cover it. Nothing major, mostly a check-in to keep things moving. Thanks "
     "and see you then."),
    ("news_report (mid)",
     "The central bank held interest rates steady on Thursday, citing easing "
     "inflation and a cooling labor market. Officials signaled that further "
     "decisions would depend on incoming data, leaving open the possibility of a "
     "cut later this year. Markets reacted modestly, with bond yields slipping and "
     "equities little changed by the close of trading."),
    ("technical_ml (low)",
     "We minimize the negative log-likelihood under a Gaussian observation model, "
     "regularizing the localized changepoint term with a Bayesian information "
     "criterion penalty. The estimator's variance scales as sigma squared over the "
     "effective sample size; under a misspecified prior the posterior contraction "
     "rate degrades and the credible intervals lose nominal coverage at the stated "
     "level."),
    ("formal_math (lowest shared context)",
     "Let f be a measurable function on a sigma-finite measure space. By the "
     "monotone convergence theorem, the integral of the pointwise supremum of an "
     "increasing sequence equals the supremum of the integrals. Define the drag "
     "epoch redshift z_star and the comoving distance D_M(z_star); the acoustic "
     "scale l_A equals pi times D_M(z_star) divided by the sound horizon r_s."),
]

DEICTICS = {
    "this", "that", "these", "those", "it", "its", "they", "them", "their",
    "there", "here", "then", "such", "same", "the other", "the usual", "before",
    "yesterday", "tomorrow", "later", "she", "he", "her", "him", "we", "you",
    "i", "us", "thing", "stuff",
}


def _tokens(t):
    return re.findall(r"[a-zA-Z']+", t.lower())


def proxies(text):
    raw = text.encode("utf-8")
    gz = len(gzip.compress(raw, 9)) / len(raw)
    toks = _tokens(text)
    n = len(toks)
    deictic = sum(1 for w in toks if w in DEICTICS) / n
    ttr = len(set(toks)) / n
    mean_len = sum(len(w) for w in toks) / n
    return dict(gzip=gz, deictic=deictic, ttr=ttr, mean_len=mean_len)


def main():
    print("=" * 82)
    print("  'Everyday' is an information-content axis (shared context) -- and it is")
    print("  measurable. Texts ordered high -> low shared context:")
    print("=" * 82)
    print(f"  {'sample':<38}{'gzip':>7}{'deictic':>9}{'TTR':>7}{'wordlen':>9}")
    rows = []
    for name, text in CORPUS:
        p = proxies(text)
        rows.append((name, p))
        print(f"  {name:<38}{p['gzip']:>7.3f}{p['deictic']:>9.3f}"
              f"{p['ttr']:>7.3f}{p['mean_len']:>9.2f}")

    hi, lo = rows[0][1], rows[-1][1]
    print(f"\n  high-shared-context (casual) vs lowest (formal):")
    print(f"    deictic density {hi['deictic']:.3f} -> {lo['deictic']:.3f}  (falls)")
    print(f"    lexical TTR     {hi['ttr']:.3f} -> {lo['ttr']:.3f}  (rises)")
    print(f"    mean word len   {hi['mean_len']:.2f} -> {lo['mean_len']:.2f}  (rises)")
    print("  -> the proxies order text along a real, measurable everyday<->specialist")
    print("     axis (deictic reliance falls; lexical diversity / word length rise).")

    print("\n  CONSEQUENCE for the LLM overhead claim:")
    print("   - 'everyday text' was a colloquial proxy, not a measured quantity -- the")
    print("     same assumed-not-earned trap as 'hard'.")
    print("   - High-shared-context prompts have a NARROW correct-answer space (low")
    print("     capability-SNR by construction): competent models converge -> ties.")
    print("     So aggregate indistinguishability conflates (a) capability saturation")
    print("     with (b) a prompt mix dominated by low-information tasks.")
    print("   - Arena does NOT stratify preference by information content, so it")
    print("     cannot separate (a) from (b). For the saturation question the")
    print("     measurement is, in this respect, BROKEN: an uncontrolled mixture.")
    print("   - Fix (the missing measurement): stratify prompts by an info-content")
    print("     proxy (gzip / perplexity / deictic density) and test whether model")
    print("     win-rate gaps shrink across generations WITHIN the high-information")
    print("     strata. Only then is 'capability has entered overhead' earned.")
    print("   - Note: the faithful proxy is LM cross-entropy (perplexity) -- the")
    print("     instrument that measures the axis is the same kind of object being")
    print("     judged. The verification needs the thing it verifies.")

    res = os.path.join(os.path.dirname(__file__), "..", "results")
    os.makedirs(res, exist_ok=True)
    import csv
    with open(os.path.join(res, "info_content.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["sample", "gzip", "deictic", "ttr", "mean_len"])
        w.writeheader()
        for name, p in rows:
            w.writerow({"sample": name, **{k: round(v, 4) for k, v in p.items()}})
    print("\nWrote: results/info_content.csv")


if __name__ == "__main__":
    main()
