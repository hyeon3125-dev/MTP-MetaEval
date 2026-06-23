"""
assumptions.py — frozen assumption counts (PREREGISTRATION.md §4).

Each entry is the number of independent explicit modeling commitments an
approach makes. Shared-substrate assumptions are counted for both approaches in
a domain (they cancel in the ratio but are recorded for transparency).
"""

# Cosmology: base = GR + FRW + CDM + fixed-Planck-early-universe = 4, plus the
# DE mechanism's own commitments.
_COSMO_BASE = 4
COSMOLOGY = {
    "lcdm": _COSMO_BASE + 1,                # + Lambda
    "cpl_w0wa": _COSMO_BASE + 1,            # + w(a)=w0+wa(1-a) form
    "standard_ide": _COSMO_BASE + 1,        # + constant coupling
    "sign_switching_ide": _COSMO_BASE + 2,  # + coupling + sign-switch
    "mtp_3p": _COSMO_BASE + 3,              # + coupling ansatz + F_hier + window
    "mtp_4p": _COSMO_BASE + 3,
    "hde": _COSMO_BASE + 1,                 # + holographic IR-cutoff postulate
    "rvm": _COSMO_BASE + 1,                 # + rho_Lambda(H) running law
}

# RH: shared "Z(t) sign-change => zero on line" + "theta bound valid" = 2.
# baseline adds the unjustified premise "more scanning => more confidence".
RH = {
    "baseline": 2 + 1,   # exhaustive accumulation premise
    "mtp": 2,            # non-refutation stop needs no extra premise
}

# Control: shared "CLT error ~ sigma/sqrt(N)" + "moving-average adequate" = 2.
# each adds its own safety premise.
CONTROL = {
    "baseline": 2 + 1,   # "fixed N is safe everywhere"
    "mtp": 2 + 1,        # "noise-floor stop is safe"
}

# Sequential refutation: shared "a check reveals refutation truthfully" = 1.
# baseline assumes the horizon M is sufficient; mtp assumes a generative prior
# (false-prob + counterexample-location law) — the very assumption that fails
# under distribution shift.
SEQUENTIAL = {
    "baseline": 1 + 1,   # + "horizon M sufficient"
    "mtp": 1 + 2,        # + prior(pi0) + CE-location law
}
