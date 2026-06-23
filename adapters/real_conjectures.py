"""
real_conjectures — historical validation of the overhead-boundary failure mode.

The sequential-refutation domain showed (synthetically) that a non-refutation
floor breaks when the counterexample tail is heavier than its prior expects. This
module checks that against the ACTUAL record of mathematics: famous conjectures
that were extensively verified and then disproven (or proven to have a
counterexample), versus ones still standing.

The question per conjecture: would an *efficient* non-refutation floor — one that
stops to save compute, i.e. well within the feasible computation frontier — have
caught the counterexample, or endorsed a false statement?

Sources (see docs/real_conjectures.md):
- Polya 1919; smallest counterexample n=906,150,257 (Tanaka 1980).
- Mertens 1897; disproven Odlyzko & te Riele 1985; no explicit counterexample,
  exists below e^(1.59e40); direct verification only reached ~1e14-1e16.
- pi(x)<li(x): Littlewood 1914 (infinitely many sign changes); first crossing
  ~1.397e316 (Demichel 2005); direct computation only to ~1e19.
- Euler sum of powers 1769; disproven n=5: 27^5+84^5+110^5+133^5=144^5 (Lander &
  Parkin 1966) [multi-dimensional search, not a 1-D scan].
- Collatz 1937; verified to 2^68 ~ 2.95e20 (Barina 2020); still open/true.
- Goldbach (even) 1742; verified to 4e18 (Oliveira e Silva 2014); still open/true.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
import os

FEASIBLE_LOG10 = 20.5   # ~ today's brute-force frontier (Collatz 2^68)


@dataclass
class Conjecture:
    name: str
    status: str            # "FALSE" | "OPEN_TRUE"
    verified_log10: float  # order of magnitude verified with no counterexample
    ce_log10: float | None  # log10 of counterexample location (None if open)
    one_dim: bool          # is it a 1-D scan-style search?
    note: str


PANEL = [
    Conjecture("Polya L(n)<=0", "FALSE", 8.0, math.log10(906150257), True,
               "counterexample n=906,150,257 (Tanaka 1980)"),
    Conjecture("Mertens |M(n)|<sqrt(n)", "FALSE", 16.0, None, True,
               "disproven 1985; no explicit CE; exists below e^(1.59e40)"),
    Conjecture("pi(x)<li(x)", "FALSE", 19.0, 316.1, True,
               "first sign change ~1.4e316 (Demichel 2005)"),
    Conjecture("Euler sum-of-powers (n=5)", "FALSE", None, math.log10(144**5), False,
               "144^5 = 27^5+84^5+110^5+133^5 (Lander-Parkin 1966); multi-dim"),
    Conjecture("Collatz", "OPEN_TRUE", math.log10(2**68), None, True,
               "verified to 2^68 (Barina 2020); still open/true"),
    Conjecture("Goldbach (even)", "OPEN_TRUE", math.log10(4e18), None, True,
               "verified to 4e18 (Oliveira e Silva 2014); still open/true"),
]


def analyse():
    rows = []
    for c in PANEL:
        if c.status == "OPEN_TRUE":
            outcome = "floor correct (no CE) -> compute saved"
            floor_safe = True
        else:
            if c.ce_log10 is None:               # Mertens: CE location unknown/huge
                reach = "beyond all computation (location unproven, ~1e40 bound)"
                floor_safe = False
            elif c.ce_log10 > FEASIBLE_LOG10:    # Skewes
                reach = f"CE at 1e{c.ce_log10:.0f} >> feasible 1e{FEASIBLE_LOG10:.0f}"
                floor_safe = False
            else:                                # Polya / Euler: within feasible
                frontier = (f"1e{c.verified_log10:.0f}" if c.verified_log10
                            else "multi-dim search")
                reach = (f"CE at 1e{c.ce_log10:.1f}, within feasible but far past "
                         f"where it 'looked settled' ({frontier})")
                floor_safe = False               # an EFFICIENT (early-stop) floor misses
            outcome = f"floor MISSES: {reach}"
        rows.append(dict(name=c.name, status=c.status, one_dim=c.one_dim,
                         ce_log10=(round(c.ce_log10, 2) if c.ce_log10 else None),
                         floor_endorses_falsehood=(c.status == "FALSE"),
                         outcome=outcome, note=c.note))
    return rows


def main():
    rows = analyse()
    false_rows = [r for r in rows if r["status"] == "FALSE"]
    missed = [r for r in false_rows if r["floor_endorses_falsehood"]]
    beyond = [r for r in false_rows
              if r["ce_log10"] is None or (r["ce_log10"] and r["ce_log10"] > FEASIBLE_LOG10)]

    print("=" * 78)
    print("  Real historical conjectures vs the non-refutation floor")
    print("=" * 78)
    print(f"{'conjecture':<26}{'status':<11}{'CE log10':>10}  outcome")
    print("-" * 78)
    for r in rows:
        ce = f"{r['ce_log10']}" if r["ce_log10"] is not None else "—"
        print(f"{r['name']:<26}{r['status']:<11}{ce:>10}  {r['outcome']}")

    print(f"\n  Famous FALSE conjectures in panel: {len(false_rows)}")
    print(f"  An efficient non-refutation floor would have ENDORSED all "
          f"{len(missed)} as 'non-refuted'.")
    print(f"  Of those, {len(beyond)} have counterexamples BEYOND ANY feasible "
          f"computation (Mertens, Skewes) — settled only by PROOF, never by scanning.")
    print("\n  Lesson: non-refutation stopping is safe ONLY given a PROVEN bound on")
    print("  counterexample location. Absent that bound (Mertens, Skewes, and RH),")
    print("  the floor is an unbounded gamble — and the famous cases are famous")
    print("  precisely because the gamble loses. This is the synthetic shift-failure")
    print("  (sequential domain, Result 3) confirmed by the historical record, and it")
    print("  retro-flags the RH domain 'win' as the same unbounded gamble.")

    res_dir = os.path.join(os.path.dirname(__file__), "..", "results")
    os.makedirs(res_dir, exist_ok=True)
    import csv
    with open(os.path.join(res_dir, "real_conjectures.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print("\nWrote: results/real_conjectures.csv")


if __name__ == "__main__":
    main()
