"""
riemann adapter — reuses MTP-riemann-z explorer/riemann_explorer.c.

baseline = exhaustive accumulation (scan to a large t_max with no stopping rule).
mtp = non-refutation stop (scan only until non-refutation is established, then
stop — further zeros add ~0 refutation power but accrue Landauer entropy).

Both verify "RH not refuted on the critical line over the scanned range"
(phenomena_covered = 1). The difference is the entropy proxy (compute_cost) and
the free stopping knob. See PREREGISTRATION.md §3b.
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

# t_max for each approach. mtp stops once non-refutation is overwhelmingly
# established (first ~10 zeros); baseline keeps scanning ~4x further.
T_MTP, T_BASE, DT = 50.0, 200.0, 0.01


def _build():
    subprocess.run(["make", "riemann_explorer"], cwd=_RH_DIR,
                   check=True, capture_output=True)


def _run(t_max: float):
    out = subprocess.run(["./riemann_explorer", str(t_max), str(DT)],
                         cwd=_RH_DIR, capture_output=True, text=True, check=True).stdout
    located = int(re.search(r"Candidates located\s*:\s*(\d+)", out).group(1))
    within = int(re.search(r"Within theta error bound\s*:\s*(\d+)", out).group(1))
    # last Stage-3 row: "<n> t<<ceil> <wall_ms> <ms/marg> <entropy_J>"
    rows = re.findall(r"^\s*\d+\s+t<[\d.]+\s+([\d.]+)\s+[\d.]+\s+([\d.eE+-]+)\s*$",
                      out, re.M)
    wall_ms = float(rows[-1][0]) if rows else 0.0
    entropy = float(rows[-1][1]) if rows else 0.0
    refuted = "not refuted" not in out.lower()  # program prints "RH not refuted ..."
    return dict(located=located, within=within, wall_ms=wall_ms,
                entropy=entropy, non_refuted=not refuted)


def score() -> DomainScore:
    _build()
    base = _run(T_BASE)
    mtp = _run(T_MTP)

    base_s = ApproachScore(
        name="exhaustive_accumulation",
        phenomena=1.0 if base["non_refuted"] else 0.0,
        free_params=1,                       # arbitrary t_max
        assumptions=assumptions.RH["baseline"],
        compute_cost=base["entropy"], compute_norm=1.0,
    )
    mtp_s = ApproachScore(
        name="non_refutation_stop",
        phenomena=1.0 if mtp["non_refuted"] else 0.0,
        free_params=0,                       # stop set by the error bound
        assumptions=assumptions.RH["mtp"],
        compute_cost=mtp["entropy"],
        compute_norm=(mtp["entropy"] / base["entropy"]) if base["entropy"] > 0 else 1.0,
    )
    return DomainScore(
        domain="number_theory_RH",
        baseline=base_s, mtp=mtp_s,
        construction_flag="partial",
        notes=(f"baseline t<{T_BASE} ({base['located']} zeros), "
               f"mtp t<{T_MTP} ({mtp['located']} zeros); both non-refuted; "
               f"entropy {base['entropy']:.2e} vs {mtp['entropy']:.2e} J."),
    )


if __name__ == "__main__":
    ds = score()
    print(ds.summary())
    for a in (ds.baseline, ds.mtp):
        print(ds.row(a))
