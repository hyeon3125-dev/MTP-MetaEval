# Historical validation — when the floor would have lied

The sequential-refutation domain showed *synthetically* that the non-refutation
floor breaks under a heavier-than-expected counterexample tail. This checks it
against the **actual record of mathematics** (`adapters/real_conjectures.py`).

For each famous conjecture: would an *efficient* non-refutation floor (one that
stops early to save compute, within the feasible computation frontier ≈ 10^20)
have caught the counterexample, or endorsed a false statement?

| conjecture | status | counterexample location | floor outcome |
|------------|--------|-------------------------|---------------|
| Pólya `L(n)≤0` | FALSE | n ≈ 9.06×10⁸ (Tanaka 1980) | **misses** — far past where it looked settled |
| Euler sum-of-powers (n=5) | FALSE | 144⁵ ≈ 6.2×10¹⁰ (Lander–Parkin 1966) | **misses** (and multi-dimensional) |
| Mertens `|M(n)|<√n` | FALSE | unknown; exists below e^(1.59×10⁴⁰) | **misses** — beyond all computation |
| π(x) < li(x) | FALSE | ≈ 1.4×10³¹⁶ (Demichel 2005) | **misses** — astronomically beyond |
| Collatz | open/true | none to 2⁶⁸ (Barina 2020) | correct — compute saved |
| Goldbach (even) | open/true | none to 4×10¹⁸ (Oliveira e Silva 2014) | correct — compute saved |

## What it shows

Of the four famous **disproven** conjectures, an efficient floor would have
endorsed **all four** as "non-refuted." Two of them (Mertens, π(x)<li(x)) have
counterexamples **beyond any feasible computation** — they were settled *only by
proof*, never by scanning. The two true conjectures (Collatz, Goldbach) are
correctly endorsed by stopping.

So the synthetic Result 3 is the historical norm, not a contrived shift: the
real-world counterexample tail is so heavy that **no efficient floor is safe**.

## The sharp consequence (and the retro-flag on RH)

Non-refutation stopping is safe **only given a proven bound on where a
counterexample can live**. With such a bound, the floor's risk is controlled (the
sequential domain's in-distribution theorem). Without it, the floor is an
*unbounded gamble*, and history shows the gamble loses on exactly the famous
cases.

The Riemann Hypothesis has **no** such bound: there is no theorem confining a
hypothetical off-line zero to a computable height. So the RH-domain "win" earlier
in this scorecard — already construction-flagged — is revealed here to be the
*same unbounded gamble* as Mertens and Skewes. The Z(t) scanner's "RH not refuted
for t < T" is exactly the statement that fooled mathematicians about π(x) < li(x)
for 10^316. Numerical non-refutation is evidence, not a risk-bounded verification,
unless a counterexample-location bound exists.

This is the honest synthesis of the whole project: **the value of a
non-refutation floor is exactly the strength of the bound that justifies it.**
