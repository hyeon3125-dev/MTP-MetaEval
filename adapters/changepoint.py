"""
changepoint — a second 'add-structure' domain on real data (generalizing cosmology).

Cosmology asked: does adding a *localized* structural term (the windowed-IDE
activation) earn its keep? It did not — because at viable couplings the localized
signal was not in the data. This domain asks the same question on a different real
dataset where the localized structure IS known to be present, plus a null control
where it is destroyed.

Data: the classic Nile annual minimum-flow series (1871-1970, n=100), which has a
well-documented regime shift ~1898 (construction of the Aswan low dam upstream).

- baseline  = constant mean (no localized structure).        k=2  (mu, sigma)
- mtp/local = single changepoint: mean1, mean2, location tau. k=4  (mu1,mu2,sigma,tau)
  -- this is the windowed/localized 'activation' analog.

Verdict by AIC/BIC + a permutation null (shuffle destroys the regime shift but
keeps the marginal distribution). Expectation: the localized model wins on the
REAL series and loses on the shuffled null -> 'add-structure' pays only when the
structure is genuinely in the data.
"""
from __future__ import annotations

import math
import os

import numpy as np

NILE = np.array([
    1120, 1160, 963, 1210, 1160, 1160, 813, 1230, 1370, 1140, 995, 935, 1110,
    994, 1020, 960, 1180, 799, 958, 1140, 1100, 1210, 1150, 1250, 1260, 1220,
    1030, 1100, 774, 840, 874, 694, 940, 833, 701, 916, 692, 1020, 1050, 969,
    831, 726, 456, 824, 702, 1120, 1100, 832, 764, 821, 768, 845, 864, 862,
    698, 845, 744, 796, 1040, 759, 781, 865, 845, 944, 984, 897, 822, 1010,
    771, 676, 649, 846, 812, 742, 801, 1040, 860, 874, 848, 890, 744, 749, 838,
    1050, 918, 986, 797, 923, 975, 815, 1020, 906, 901, 1170, 912, 746, 919,
    718, 714, 740], dtype=float)


def _gauss_loglik(x, mu, sigma):
    sigma = max(sigma, 1e-9)
    return -0.5 * len(x) * math.log(2 * math.pi * sigma ** 2) \
        - 0.5 * np.sum((x - mu) ** 2) / sigma ** 2


def fit_constant(x):
    mu, sigma = x.mean(), x.std(ddof=0)
    return _gauss_loglik(x, mu, sigma), 2


def fit_changepoint(x, lo=5, hi=None):
    n = len(x)
    hi = hi or n - 5
    best_ll, best_tau = -np.inf, None
    for tau in range(lo, hi):
        left, right = x[:tau], x[tau:]
        # pooled sigma (shared scale), separate means
        resid = np.concatenate([left - left.mean(), right - right.mean()])
        sigma = resid.std(ddof=0)
        ll = _gauss_loglik(left, left.mean(), sigma) + _gauss_loglik(right, right.mean(), sigma)
        if ll > best_ll:
            best_ll, best_tau = ll, tau
    return best_ll, 4, best_tau


def aic_bic(ll, k, n):
    return -2 * ll + 2 * k, -2 * ll + k * math.log(n)


def evaluate(x):
    n = len(x)
    ll0, k0 = fit_constant(x)
    ll1, k1, tau = fit_changepoint(x)
    a0, b0 = aic_bic(ll0, k0, n)
    a1, b1 = aic_bic(ll1, k1, n)
    return dict(dAIC=a1 - a0, dBIC=b1 - b0, tau=tau, ll0=ll0, ll1=ll1)


def permutation_null(x, n_perm=2000, seed=42):
    rng = np.random.default_rng(seed)
    obs = evaluate(x)["dAIC"]
    null = np.empty(n_perm)
    for i in range(n_perm):
        null[i] = evaluate(rng.permutation(x))["dAIC"]
    p = float(np.mean(null <= obs))   # P(null as changepoint-favorable as observed)
    return obs, null, p


def main():
    n = len(NILE)
    real = evaluate(NILE)
    obs, null, p = permutation_null(NILE)
    yr = 1871 + real["tau"]

    print("=" * 74)
    print("  Add-structure on real data: Nile regime shift vs null")
    print("=" * 74)
    print(f"  n={n}; changepoint model adds a localized step (mu1->mu2 at tau).")
    print(f"\n  REAL Nile series:")
    print(f"    best changepoint at index {real['tau']} (year ~{yr})")
    print(f"    dAIC = {real['dAIC']:.1f}   dBIC = {real['dBIC']:.1f}   "
          f"(negative => localized model wins)")
    print(f"\n  Permutation null (shuffle destroys the regime shift, {len(null)} perms):")
    print(f"    null dAIC: mean {null.mean():.1f}, 5th pct {np.percentile(null,5):.1f}")
    print(f"    observed {obs:.1f}  ->  p = {p:.4f}")
    print(f"\n  Verdict: on the REAL series the localized ('windowed') structure is")
    print(f"  strongly selected (dAIC {real['dAIC']:.0f}, p={p:.3f}); under the null it")
    print(f"  is not. So 'add-structure' MTP-localization pays ONLY when the structure")
    print(f"  is genuinely in the data — which is exactly why windowed-IDE LOST in")
    print(f"  cosmology (no real window signal at viable couplings). The cosmology loss")
    print(f"  generalizes as CONDITIONAL: assumed structure loses, earned structure wins.")

    res_dir = os.path.join(os.path.dirname(__file__), "..", "results")
    os.makedirs(res_dir, exist_ok=True)
    import csv
    with open(os.path.join(res_dir, "changepoint.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["series", "dAIC", "dBIC", "tau_year", "perm_p"])
        w.writerow(["nile_real", f"{real['dAIC']:.2f}", f"{real['dBIC']:.2f}", yr, f"{p:.4f}"])
        w.writerow(["null_mean", f"{null.mean():.2f}", "", "", ""])
    print("\nWrote: results/changepoint.csv")


if __name__ == "__main__":
    main()
