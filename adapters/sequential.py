"""
sequential refutation adapter — the un-flagged stopping test (PREREGISTRATION §3d).

A population of conjectures, each TRUE (no counterexample in [0,M)) or FALSE
(counterexample at x ~ Geometric(r_true)). The non-refutation FLOOR must locate
the overhead boundary without stopping early enough to miss a real
counterexample. Ground truth makes the rule falsifiable, so a win here is NOT
construction-flagged.

baseline = exhaustive scan to M (always correct within M).
mtp = stop at smallest t with posterior q(t) <= eps that a counterexample remains.

Reports: the risk-bound check (miss_rate <= eps under correct prior), the
in-distribution efficiency, and the distribution-shift failure mode.
"""
from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from scorecard.schema import ApproachScore, DomainScore     # noqa: E402
from scorecard import assumptions                           # noqa: E402

# Generative + assumed prior (in-distribution: equal). Pre-registered.
M = 5000            # search horizon
PI0 = 0.5           # fraction of FALSE conjectures
R_ASSUMED = 0.02    # prior geometric rate for counterexample location
N_POP = 20000       # population size
EPS_OP = 0.01       # operating floor for the scorecard row
SEED = 42


def _t_floor(eps: float, r_assumed: float = R_ASSUMED, pi0: float = PI0) -> int:
    """Smallest t with q(t) <= eps, q(t)=pi0 S(t)/((1-pi0)+pi0 S(t)),
    S(t)=(1-r)^t. Solve (1-r)^t <= eps(1-pi0)/(pi0(1-eps))."""
    rhs = eps * (1.0 - pi0) / (pi0 * (1.0 - eps))
    if rhs >= 1.0:
        return 0
    t = np.log(rhs) / np.log(1.0 - r_assumed)
    return int(min(np.ceil(t), M))


def _draw_population(r_true: float, rng) -> np.ndarray:
    """Counterexample location for each conjecture, or -1 if TRUE (no CE)."""
    is_false = rng.random(N_POP) < PI0
    # Geometric(r_true) on {0,1,...}; clip to horizon (CE beyond M is unreachable
    # => effectively TRUE within the horizon, handled below).
    x = rng.geometric(r_true, size=N_POP) - 1
    loc = np.where(is_false, x, -1)
    return loc


def _evaluate(loc: np.ndarray, t_floor: int):
    """Return (exhaustive_checks, mtp_checks, mtp_misses, n) for a population.
    A conjecture is 'reachably false' if 0 <= loc < M."""
    has_ce = (loc >= 0) & (loc < M)
    ce = np.where(has_ce, loc, M)            # effective CE position (M if none)

    # exhaustive: stops at CE if reachable, else scans full M. Always correct.
    exh_checks = np.where(has_ce, ce + 1, M).sum()

    # mtp: stops at min(t_floor, CE+1 if CE<t_floor). If CE >= t_floor -> miss.
    found = has_ce & (ce < t_floor)
    mtp_checks = np.where(found, ce + 1, t_floor).sum()
    misses = int((has_ce & (ce >= t_floor)).sum())
    return int(exh_checks), int(mtp_checks), misses, len(loc)


def run_full():
    rng = np.random.default_rng(SEED)
    # in-distribution population
    loc_in = _draw_population(R_ASSUMED, rng)

    # (1) risk-bound sweep: miss_rate vs eps, in-distribution
    sweep = []
    for eps in (0.05, 0.02, 0.01, 0.005, 0.002, 0.001):
        tf = _t_floor(eps)
        exh, mtp, miss, n = _evaluate(loc_in, tf)
        sweep.append(dict(eps=eps, t_floor=tf, miss_rate=miss / n,
                          bound=eps * (1 - PI0), saved=1 - mtp / exh))

    # (3) distribution shift: true rate heavier-tailed (smaller r => CE further out)
    rng2 = np.random.default_rng(SEED + 1)
    loc_shift = _draw_population(R_ASSUMED / 4.0, rng2)   # 4x heavier tail
    tf_op = _t_floor(EPS_OP)
    exh_s, mtp_s, miss_s, n_s = _evaluate(loc_shift, tf_op)

    return dict(t_floor_op=tf_op, sweep=sweep,
                shift=dict(miss_rate=miss_s / n_s, saved=1 - mtp_s / exh_s,
                           bound=EPS_OP * (1 - PI0)))


def score() -> DomainScore:
    rng = np.random.default_rng(SEED)
    loc_in = _draw_population(R_ASSUMED, rng)
    tf = _t_floor(EPS_OP)
    exh, mtp, miss, n = _evaluate(loc_in, tf)

    base = ApproachScore(
        name="exhaustive_scan",
        phenomena=1.0,                       # always correct within M
        free_params=1, assumptions=assumptions.SEQUENTIAL["baseline"],
        compute_cost=exh, compute_norm=1.0,
    )
    mtp_s = ApproachScore(
        name="non_refutation_floor",
        phenomena=1.0 - miss / n,            # ground-truth verdict accuracy
        free_params=1, assumptions=assumptions.SEQUENTIAL["mtp"],
        compute_cost=mtp, compute_norm=mtp / exh if exh > 0 else 1.0,
    )
    full = run_full()
    sh = full["shift"]
    return DomainScore(
        domain="sequential_refutation",
        baseline=base, mtp=mtp_s,
        construction_flag="none",
        notes=(f"in-dist eps={EPS_OP}: t_floor={tf}, miss_rate={miss/n:.4f} "
               f"(bound {EPS_OP*(1-PI0):.4f}), compute_saved={1-mtp/exh:.3f}. "
               f"SHIFT (4x tail): miss_rate={sh['miss_rate']:.4f} >> bound "
               f"{sh['bound']:.4f}, saved={sh['saved']:.3f} -> floor breaks."),
    )


def make_plot(full, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    eps = [s["eps"] for s in full["sweep"]]
    miss = [s["miss_rate"] for s in full["sweep"]]
    bound = [s["bound"] for s in full["sweep"]]
    saved = [s["saved"] for s in full["sweep"]]
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    ax[0].plot(eps, miss, "o-", label="empirical miss rate")
    ax[0].plot(eps, bound, "k--", label="bound  ε(1−π0)")
    ax[0].scatter([EPS_OP], [full["shift"]["miss_rate"]], c="red", zorder=5,
                  label=f"shift (4× tail): {full['shift']['miss_rate']:.2f}")
    ax[0].set_xscale("log"); ax[0].set_xlabel("floor ε"); ax[0].set_ylabel("miss rate")
    ax[0].set_title("Risk bound holds in-distribution, breaks under shift")
    ax[0].legend(fontsize=8); ax[0].grid(alpha=0.3)
    ax[1].plot(miss, saved, "s-")
    ax[1].set_xlabel("miss rate"); ax[1].set_ylabel("compute saved")
    ax[1].set_title("Overhead boundary: compute saved vs risk")
    ax[1].grid(alpha=0.3)
    for s in full["sweep"]:
        ax[1].annotate(f"ε={s['eps']}", (s["miss_rate"], s["saved"]), fontsize=6)
    fig.tight_layout(); fig.savefig(path, dpi=130, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    import csv
    full = run_full()
    print(f"t_floor(eps=0.01) = {full['t_floor_op']}  (horizon M={M})\n")
    print("Risk-bound sweep (in-distribution):")
    print(f"  {'eps':>7}{'t_floor':>9}{'miss_rate':>11}{'bound~eps(1-pi0)':>18}{'compute_saved':>15}")
    for s in full["sweep"]:
        ok = "OK" if s["miss_rate"] <= s["bound"] * 1.5 else "!!"
        print(f"  {s['eps']:>7.3f}{s['t_floor']:>9}{s['miss_rate']:>11.4f}"
              f"{s['bound']:>18.4f}{s['saved']:>14.1%} {ok}")
    sh = full["shift"]
    print(f"\nDistribution shift (true tail 4x heavier than prior), eps=0.01:")
    print(f"  miss_rate={sh['miss_rate']:.4f}  vs bound {sh['bound']:.4f}  "
          f"compute_saved={sh['saved']:.1%}  -> prior misspecification breaks the bound")
    print()
    ds = score()
    print(ds.summary())
    for a in (ds.baseline, ds.mtp):
        print(ds.row(a))

    res_dir = os.path.join(os.path.dirname(__file__), "..", "results")
    os.makedirs(res_dir, exist_ok=True)
    with open(os.path.join(res_dir, "sequential_sweep.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["eps", "t_floor", "miss_rate", "bound", "saved"])
        w.writeheader(); w.writerows(full["sweep"])
    make_plot(full, os.path.join(res_dir, "sequential_overhead_boundary.png"))
    print("\nWrote: results/sequential_sweep.csv, results/sequential_overhead_boundary.png")
