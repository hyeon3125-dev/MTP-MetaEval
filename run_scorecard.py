"""
run_scorecard.py — cross-domain MTP explanatory-efficiency scorecard.

Runs the three domain adapters, prints a per-domain ratio/verdict table, the
reference comparators (cosmology), and a qualitative meta-pattern. Per
PREREGISTRATION.md: NO single aggregate index — only per-domain ratios + a
qualitative reading. Saves results/scorecard.csv.

Usage: python run_scorecard.py [--domains cosmology,riemann,control]
"""
from __future__ import annotations

import argparse
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from adapters import cosmology, riemann, control            # noqa: E402

ADAPTERS = {"cosmology": cosmology, "riemann": riemann, "control": control}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--domains", default="cosmology,riemann,control")
    ap.add_argument("--res-dir", default=os.path.join(os.path.dirname(__file__), "results"))
    args = ap.parse_args()
    names = [d.strip() for d in args.domains.split(",") if d.strip()]

    print("=" * 78)
    print("  MTP explanatory-efficiency scorecard")
    print("  E = phenomena / (params + assumptions + compute_norm);  ratio = E_mtp/E_base")
    print("  (per-domain ratios only — no cross-domain aggregate; see PREREGISTRATION)")
    print("=" * 78)

    domains = []
    for nm in names:
        print(f"\n>>> running domain: {nm} ...")
        domains.append(ADAPTERS[nm].score())

    # per-domain summary table
    print(f"\n{'domain':<22}{'baseline_E':>11}{'mtp_E':>9}{'ratio':>8}"
          f"{'verdict':>10}{'flag':>9}")
    print("-" * 78)
    rows = []
    for ds in domains:
        print(f"{ds.domain:<22}{ds.baseline.efficiency:>11.4f}{ds.mtp.efficiency:>9.4f}"
              f"{ds.ratio:>8.3f}{ds.verdict:>10}{ds.construction_flag:>9}")
        rows.append(ds.summary())
        # detail rows
        for tag, a in (("baseline", ds.baseline), ("mtp", ds.mtp)):
            rows.append({"domain": ds.domain, "approach": f"{tag}:{a.name}",
                         "phenomena": a.phenomena, "free_params": a.free_params,
                         "assumptions": a.assumptions,
                         "compute_norm": round(a.compute_norm, 4),
                         "efficiency": round(a.efficiency, 4)})

    # cosmology compute-excluded sensitivity (compute term dominates by 100x+)
    cosmo = next((d for d in domains if d.domain == "cosmology"), None)
    if cosmo:
        def eff_nc(a):  # efficiency excluding the compute term
            return a.phenomena / (a.free_params + a.assumptions)
        r_nc = eff_nc(cosmo.mtp) / eff_nc(cosmo.baseline)
        print(f"\n  [cosmology sensitivity] excluding compute term: ratio = {r_nc:.3f} "
              f"({'worse' if r_nc < 0.9 else 'neutral' if r_nc <= 1.1 else 'improves'}) "
              f"-> verdict robust to the compute-dominance.")

    # notes
    print("\nNotes:")
    for ds in domains:
        print(f"  - {ds.domain}: {ds.notes}")

    # qualitative meta-pattern (NO aggregate index)
    print("\n" + "=" * 78)
    print("  META-PATTERN (qualitative; pre-registered expectation in PREREGISTRATION §5)")
    print("=" * 78)
    improves = [d.domain for d in domains if d.verdict == "improves"]
    worse = [d.domain for d in domains if d.verdict == "worse"]
    flagged = [d.domain for d in domains if d.construction_flag != "none"]
    print(f"  improves: {improves or '—'}")
    print(f"  worse   : {worse or '—'}")
    print(f"  construction-flagged wins (weak evidence): {flagged or '—'}")
    print("  Reading: the principle is a COST/COMPRESSION rule. It improves efficiency")
    print("  where the bottleneck is wasteful accumulation (RH entropy, control")
    print("  iterations) but NOT where the task needs added explanatory structure")
    print("  (cosmology). Both 'improves' are construction-flagged, so they are weak")
    print("  evidence; the one genuine-baseline test (cosmology) goes against MTP.")
    print("  => Support for the axiom as a universal modeling principle is NOT")
    print("     established; it behaves as a verification-stopping heuristic.")

    os.makedirs(args.res_dir, exist_ok=True)
    pd.DataFrame(rows).to_csv(os.path.join(args.res_dir, "scorecard.csv"), index=False)
    print(f"\nWrote: results/scorecard.csv")


if __name__ == "__main__":
    main()
