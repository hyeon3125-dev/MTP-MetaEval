"""
earned_threshold — the assumed/earned axis as ONE calibrated curve.

Cosmology (assumed structure, lost) and the Nile changepoint (earned structure,
won) are the two ends of a single quantity: the signal-to-noise ratio of the
localized structure. This sweeps SNR and measures the probability that AIC selects
the localized (changepoint) model over the constant baseline, turning the binary
"win/lose" into a detection curve with a threshold.

Noise is calibrated to the real Nile within-segment scatter, so SNR=0 is the
cosmology/null regime (no real structure) and the Nile anchor sits at its
empirical SNR. The localized-structure move pays exactly above the threshold.
"""
from __future__ import annotations

import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from adapters.changepoint import NILE, fit_constant, fit_changepoint, aic_bic, evaluate

N = 100                       # series length (match Nile)
SNRS = [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0]
N_REAL = 400                  # realizations per SNR
SEED = 11


def nile_noise_sigma() -> float:
    """Pooled within-segment std of the real Nile series (the realistic noise)."""
    tau = evaluate(NILE)["tau"]
    left, right = NILE[:tau], NILE[tau:]
    resid = np.concatenate([left - left.mean(), right - right.mean()])
    return float(resid.std(ddof=0))


def nile_snr(sigma: float) -> float:
    tau = evaluate(NILE)["tau"]
    step = abs(NILE[:tau].mean() - NILE[tau:].mean())
    return step / sigma


def _daics_at(snr: float, sigma: float, rng):
    step = snr * sigma
    d = np.empty(N_REAL)
    for i in range(N_REAL):
        x = rng.normal(0.0, sigma, N)
        x[N // 2:] += step                     # localized shift at the midpoint
        ll0, k0 = fit_constant(x)
        ll1, k1, _ = fit_changepoint(x)
        a0, _ = aic_bic(ll0, k0, N)
        a1, _ = aic_bic(ll1, k1, N)
        d[i] = a1 - a0
    return d


def detection_curve(sigma: float):
    """Two detectors: naive (AIC<0) and null-calibrated (beat the SNR=0 null at 5%)."""
    rng = np.random.default_rng(SEED)
    null = _daics_at(0.0, sigma, rng)          # SNR=0 distribution of best dAIC
    crit = float(np.percentile(null, 5))       # 5% false-positive critical value
    out = []
    for snr in SNRS:
        d = _daics_at(snr, sigma, rng)
        out.append(dict(snr=snr,
                        detect_naive=float(np.mean(d < 0)),
                        detect=float(np.mean(d <= crit)),   # null-calibrated power
                        median_dAIC=float(np.median(d))))
    return out, crit, float(np.mean(null < 0))


def threshold(curve, level):
    """Smallest SNR with detection >= level (linear interp)."""
    for a, b in zip(curve, curve[1:]):
        if a["detect"] < level <= b["detect"]:
            f = (level - a["detect"]) / (b["detect"] - a["detect"])
            return a["snr"] + f * (b["snr"] - a["snr"])
    return None


def make_plot(curve, sigma, path, naive_fp, crit):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    snr = [c["snr"] for c in curve]
    det = [c["detect"] for c in curve]
    naive = [c["detect_naive"] for c in curve]
    nile = nile_snr(sigma)
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    ax.plot(snr, det, "o-", label="null-calibrated power (5% FP)")
    ax.plot(snr, naive, "s--", color="orange", alpha=0.8,
            label=f"naive AIC<0 (FP@SNR0={naive_fp:.0%})")
    ax.axhline(0.95, color="gray", ls=":", lw=1)
    t95 = threshold(curve, 0.95)
    if t95: ax.axvline(t95, color="green", ls="--", lw=1, label=f"95% power SNR≈{t95:.2f}")
    ax.axvspan(0, 0.3, color="red", alpha=0.08)
    ax.annotate("cosmology regime\n(assumed, SNR≪1 → lose)", (0.04, 0.42), fontsize=8, color="darkred")
    ax.scatter([nile], [1.0], c="blue", zorder=5, label=f"Nile (earned, SNR≈{nile:.1f})")
    ax.set_xlabel("localized-structure SNR (step / noise)")
    ax.set_ylabel("detection probability")
    ax.set_title("Earned vs assumed structure is one curve in SNR")
    ax.legend(fontsize=8); ax.grid(alpha=0.3); ax.set_ylim(-0.03, 1.05)
    fig.tight_layout(); fig.savefig(path, dpi=130, bbox_inches="tight"); plt.close(fig)


def main():
    sigma = nile_noise_sigma()
    nile = nile_snr(sigma)
    curve, crit, naive_fp = detection_curve(sigma)
    t50, t95 = threshold(curve, 0.5), threshold(curve, 0.95)

    print("=" * 72)
    print("  Earned vs assumed structure — one calibrated curve in SNR")
    print("=" * 72)
    print(f"  Nile within-segment noise sigma = {sigma:.1f}; Nile step SNR = {nile:.2f}\n")
    print(f"  Naive AIC<0 false-positive rate at SNR=0: {naive_fp:.3f}  <- the location")
    print(f"  search overfits noise; naive AIC 'detects' structure ~{naive_fp:.0%} of the")
    print(f"  time from pure noise. Proper detector calibrates vs the null (crit dAIC")
    print(f"  = {crit:.1f}, 5% false-positive).\n")
    print(f"  {'SNR':>6}{'naive_AIC<0':>13}{'calibrated_power':>18}{'median_dAIC':>13}")
    for c in curve:
        print(f"  {c['snr']:>6.2f}{c['detect_naive']:>13.3f}{c['detect']:>18.3f}{c['median_dAIC']:>13.1f}")
    print(f"\n  Calibrated detection threshold: 50% at SNR≈{t50:.2f}, 95% at SNR≈"
          f"{(f'{t95:.2f}' if t95 else '>3')}")
    print(f"  Nile (real, earned) at SNR≈{nile:.1f} -> power ~1.0 (won).")
    print(f"  Cosmology (windowed-IDE, assumed): localized signal sub-percent vs data")
    print(f"  errors -> SNR << 1, below threshold -> lost.")
    print(f"\n  => Two lessons in one curve:")
    print(f"     (a) 'assumed vs earned' is position on this SNR curve, not a binary;")
    print(f"         the move pays iff SNR clears ~{t95:.1f} (95% power).")
    print(f"     (b) the DETECTOR must itself be earned: naive AIC claims structure")
    print(f"         {naive_fp:.0%} of the time from noise -> the same assumed-not-earned trap,")
    print(f"         fixed only by calibrating against the null.")

    res = os.path.join(os.path.dirname(__file__), "..", "results")
    os.makedirs(res, exist_ok=True)
    import csv
    with open(os.path.join(res, "earned_threshold.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["snr", "detect_naive", "detect", "median_dAIC"])
        w.writeheader(); w.writerows(curve)
    make_plot(curve, sigma, os.path.join(res, "earned_threshold.png"), naive_fp, crit)
    print("\nWrote: results/earned_threshold.csv, results/earned_threshold.png")


if __name__ == "__main__":
    main()
