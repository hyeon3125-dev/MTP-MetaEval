"""
cosmology adapter — reuses the MTP-Cosmology comparison engine.

baseline = LambdaCDM, mtp = windowed IDE (mtp_3p); references = CPL, constant
IDE, sign-switching IDE, HDE, RVM. Each model is fit jointly to
Planck(R,l_A) + DESI DR1 BAO + Gold-2018 RSD; phenomena_covered counts the data
blocks reproduced at chi2/N <= 2.0 at the joint best fit. compute_cost is the
wall-time of one H(z) evaluation (analytic models cheap, ODE models costly),
normalized to LambdaCDM. See PREREGISTRATION.md §3a.
"""
from __future__ import annotations

import os
import sys
import time

import numpy as np

_COSMO_SRC = os.path.join(os.path.dirname(__file__), "..", "..", "MTP-Cosmology", "src")
sys.path.insert(0, _COSMO_SRC)

from mtp_cosmology import models as M                       # noqa: E402
from mtp_cosmology import compare as C                      # noqa: E402

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from scorecard.schema import ApproachScore, DomainScore     # noqa: E402
from scorecard import assumptions                           # noqa: E402

TOL = 2.0                       # chi2/N per-block tolerance (pre-registered)
MODELS = ["lcdm", "cpl_w0wa", "standard_ide", "sign_switching_ide",
          "mtp_3p", "mtp_4p", "hde", "rvm"]
_Z = np.linspace(0.01, 2.5, 200)


def _blocks():
    """Single-block datasets + their point counts, for per-block chi2."""
    bao = C.desi_dr1_dataset()
    rsd = C.rsd_dataset()
    cmb = C.Dataset("CMB", cmb=C.cmb_block())
    return {"BAO": (bao, bao.n_points), "RSD": (rsd, rsd.n_points),
            "CMB": (cmb, cmb.n_points)}


def _h_eval_cost(model, theta, repeats=5):
    t = time.perf_counter()
    for _ in range(repeats):
        model.H(_Z, theta)
    return (time.perf_counter() - t) / repeats


def score() -> DomainScore:
    full = C.full_dataset()
    blocks = _blocks()

    scores = {}
    costs = {}
    for name in MODELS:
        mdl = M.get(name)
        fit = C.fit_model(mdl, full, n_starts=6)
        theta = [fit.best[p] for p in mdl.param_names]
        # per-block chi2/N at the joint best fit -> phenomena_covered
        covered = 0
        for _bname, (ds, n) in blocks.items():
            if ds.chi2(mdl, theta) / n <= TOL:
                covered += 1
        cost = _h_eval_cost(mdl, theta)
        costs[name] = cost
        scores[name] = ApproachScore(
            name=name, phenomena=covered, free_params=mdl.k,
            assumptions=assumptions.COSMOLOGY[name], compute_cost=cost,
        )

    base_cost = costs["lcdm"]
    for s in scores.values():
        s.compute_norm = s.compute_cost / base_cost if base_cost > 0 else 1.0

    refs = [scores[n] for n in MODELS if n not in ("lcdm", "mtp_3p")]
    return DomainScore(
        domain="cosmology",
        baseline=scores["lcdm"],
        mtp=scores["mtp_3p"],
        references=refs,
        construction_flag="none",
        notes="Joint Planck(R,lA)+DESI+RSD fit; phenomena = blocks at chi2/N<=2.",
    )


if __name__ == "__main__":
    ds = score()
    print(ds.summary())
    for a in [ds.baseline, ds.mtp] + ds.references:
        print(ds.row(a))
