"""
control adapter — reuses MTP-riemann-z explorer/thermal_controller.c.

baseline = fixed-window controller (N = N_MAX every step).
mtp = adaptive precision-floor controller (stop at sigma/sqrt(N)).

Both arms run on the SAME noisy signal inside the C program (the baseline arm was
added to thermal_controller.c for this head-to-head). phenomena_covered = #
scenarios tracked with mean abs error <= TOL; compute_cost = mean iterations/step.
Also reports Pareto-dominance (tolerance-independent). See PREREGISTRATION.md §3c.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys

_RH_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "MTP-riemann-z explorer")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from scorecard.schema import ApproachScore, DomainScore     # noqa: E402
from scorecard import assumptions                           # noqa: E402

TOL = 0.15                       # pre-registered (amended A1)
SENS_TOLS = (0.10, 0.15, 0.20)


def _build():
    subprocess.run(["make", "thermal_controller"], cwd=_RH_DIR,
                   check=True, capture_output=True)


def _run():
    out = subprocess.run(["./thermal_controller"], cwd=_RH_DIR,
                         capture_output=True, text=True, check=True).stdout
    # per scenario: adaptive "Mean abs error", adaptive "Mean iters/step",
    # and "Fixed-N baseline: err X iters/step Y"
    ad_err = [float(x) for x in re.findall(r"Mean abs error\s*:\s*([\d.]+)", out)]
    ad_it = [float(x) for x in re.findall(r"Mean iters/step\s*:\s*([\d.]+)", out)]
    fx = re.findall(r"Fixed-N baseline:\s*err\s*([\d.]+)\s*iters/step\s*([\d.]+)", out)
    fx_err = [float(a) for a, _ in fx]
    fx_it = [float(b) for _, b in fx]
    return ad_err, ad_it, fx_err, fx_it


def _coverage(errs, tol):
    return sum(1 for e in errs if e <= tol)


def score() -> DomainScore:
    _build()
    ad_err, ad_it, fx_err, fx_it = _run()
    n = len(ad_err)

    ad_iters_mean = sum(ad_it) / n
    fx_iters_mean = sum(fx_it) / n

    base = ApproachScore(
        name="fixed_window",
        phenomena=_coverage(fx_err, TOL),
        free_params=1, assumptions=assumptions.CONTROL["baseline"],
        compute_cost=fx_iters_mean, compute_norm=1.0,
    )
    mtp = ApproachScore(
        name="adaptive_precision_floor",
        phenomena=_coverage(ad_err, TOL),
        free_params=1, assumptions=assumptions.CONTROL["mtp"],
        compute_cost=ad_iters_mean,
        compute_norm=ad_iters_mean / fx_iters_mean if fx_iters_mean > 0 else 1.0,
    )

    pareto = all(a <= f for a, f in zip(ad_err, fx_err)) and \
             all(a <= f for a, f in zip(ad_it, fx_it))
    sens = {t: (_coverage(ad_err, t), _coverage(fx_err, t)) for t in SENS_TOLS}
    sens_str = ", ".join(f"tol{t}:{a}/{f}" for t, (a, f) in sens.items())

    return DomainScore(
        domain="engineering_control",
        baseline=base, mtp=mtp,
        construction_flag="partial",
        notes=(f"adaptive err {ad_err} iters {ad_it} vs fixed err {fx_err} "
               f"iters {fx_it}; adaptive Pareto-dominates: {pareto}; "
               f"coverage(adaptive/fixed) {sens_str}."),
    )


if __name__ == "__main__":
    ds = score()
    print(ds.summary())
    for a in (ds.baseline, ds.mtp):
        print(ds.row(a))
