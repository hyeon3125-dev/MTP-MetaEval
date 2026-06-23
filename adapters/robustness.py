"""
robustness frontier — how far can the floor be made safe, and at what cost?

Extends the sequential domain. Two questions:
  (1) Breakdown: as the TRUE counterexample tail gets heavier than the prior
      assumes, at what heaviness does the naive floor's miss rate exceed its bound?
  (2) Recovery: a CONSERVATIVE floor (assume the tail is heavier than naive)
      restores bounded risk over a wider range — at the cost of less compute saved.
      What is the trade frontier, and what is the hard limit?

Reuses adapters/sequential.py. Heaviness h = r_assumed / r_true (h>1 => true tail
heavier than the prior expects; counterexamples sit further out).
"""
from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from adapters.sequential import (                            # noqa: E402
    _t_floor, _draw_population, _evaluate, M, PI0, R_ASSUMED, EPS_OP, N_POP,
)

HEAVINESS = [1, 2, 3, 4, 6, 8]          # true-tail heaviness vs prior
SAFETY = [1, 2, 4, 8]                    # conservative-prior factors
SEED = 7


def _miss_and_saved(r_true, r_assumed_for_floor):
    rng = np.random.default_rng(SEED)
    loc = _draw_population(r_true, rng)
    tf = _t_floor(EPS_OP, r_assumed=r_assumed_for_floor)
    exh, mtp, miss, n = _evaluate(loc, tf)
    return miss / n, (1 - mtp / exh), tf


def breakdown():
    """Naive floor (prior=R_ASSUMED) miss rate vs heaviness."""
    bound = EPS_OP * (1 - PI0)
    out = []
    for h in HEAVINESS:
        miss, saved, tf = _miss_and_saved(R_ASSUMED / h, R_ASSUMED)
        out.append(dict(heaviness=h, miss_rate=miss, bound=bound,
                        over_bound=miss / bound, saved=saved, t_floor=tf))
    return out


def recovery():
    """Conservative floor (prior=R_ASSUMED/safety): safe-up-to-h and compute cost."""
    bound = EPS_OP * (1 - PI0)
    out = []
    for s in SAFETY:
        r_cons = R_ASSUMED / s
        # max heaviness kept safe (miss <= 2x bound), and compute saved at h=1
        safe_h = 0
        for h in HEAVINESS:
            miss, _, _ = _miss_and_saved(R_ASSUMED / h, r_cons)
            if miss <= 2 * bound:
                safe_h = h
        _, saved_at1, tf = _miss_and_saved(R_ASSUMED, r_cons)
        out.append(dict(safety=s, t_floor=tf, saved_indist=saved_at1,
                        safe_up_to_heaviness=safe_h))
    return out


def main():
    bound = EPS_OP * (1 - PI0)
    print("=" * 74)
    print(f"  Robustness frontier (eps={EPS_OP}, bound={bound:.4f})")
    print("=" * 74)
    print("\n(1) Breakdown — naive floor as the true tail gets heavier:")
    print(f"  {'heaviness':>10}{'t_floor':>9}{'miss_rate':>11}{'x bound':>9}{'compute_saved':>15}")
    bd = breakdown()
    for r in bd:
        flag = "" if r["over_bound"] <= 2 else "  <- unsafe"
        print(f"  {r['heaviness']:>10}{r['t_floor']:>9}{r['miss_rate']:>11.4f}"
              f"{r['over_bound']:>9.1f}{r['saved']:>14.1%}{flag}")
    first_unsafe = next((r["heaviness"] for r in bd if r["over_bound"] > 2), None)
    print(f"  -> naive floor becomes unsafe (miss > 2x bound) at heaviness "
          f"{first_unsafe}.")

    print("\n(2) Recovery — conservative floor (assume heavier tail):")
    print(f"  {'safety':>8}{'t_floor':>9}{'saved@h=1':>12}{'safe_up_to_h':>14}")
    for r in recovery():
        print(f"  {r['safety']:>8}{r['t_floor']:>9}{r['saved_indist']:>11.1%}"
              f"{r['safe_up_to_heaviness']:>14}")
    print("\n  Robustness has a price: a more conservative floor stays safe over a")
    print("  wider tail range but saves less compute. And the hard limit (from")
    print("  docs/real_conjectures.md): against an UNBOUNDED tail — no proven bound on")
    print("  counterexample location (Mertens, Skewes, RH) — NO finite-compute floor")
    print("  is safe. Robustness buys range, never invulnerability.")

    res_dir = os.path.join(os.path.dirname(__file__), "..", "results")
    os.makedirs(res_dir, exist_ok=True)
    import csv
    with open(os.path.join(res_dir, "robustness_breakdown.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(bd[0].keys()))
        w.writeheader(); w.writerows(bd)
    print("\nWrote: results/robustness_breakdown.csv")


if __name__ == "__main__":
    main()
