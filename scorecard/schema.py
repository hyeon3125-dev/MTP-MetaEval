"""
schema.py — common scorecard types and the (frozen) efficiency metric.

efficiency = phenomena_covered / (free_params + assumptions + compute_norm)
ratio      = efficiency_mtp / efficiency_baseline

Only `ratio` is comparable across domains (PREREGISTRATION.md §1). Verdict
thresholds and the construction-flag discount are fixed by pre-registration.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict


@dataclass
class ApproachScore:
    name: str
    phenomena: float          # phenomena_covered
    free_params: int
    assumptions: int
    compute_cost: float       # raw, domain-specific units
    compute_norm: float = 1.0 # set by the domain (baseline = 1.0)

    @property
    def efficiency(self) -> float:
        denom = self.free_params + self.assumptions + self.compute_norm
        return self.phenomena / denom if denom > 0 else float("inf")


def verdict(ratio: float) -> str:
    if ratio > 1.10:
        return "improves"
    if ratio < 0.90:
        return "worse"
    return "neutral"


@dataclass
class DomainScore:
    domain: str
    baseline: ApproachScore
    mtp: ApproachScore
    references: list = field(default_factory=list)   # list[ApproachScore]
    construction_flag: str = "none"                  # none | partial | full
    notes: str = ""

    @property
    def ratio(self) -> float:
        eb = self.baseline.efficiency
        return self.mtp.efficiency / eb if eb > 0 else float("inf")

    @property
    def verdict(self) -> str:
        return verdict(self.ratio)

    def row(self, a: ApproachScore) -> dict:
        d = asdict(a)
        d["efficiency"] = round(a.efficiency, 4)
        return d

    def summary(self) -> dict:
        return {
            "domain": self.domain,
            "ratio": round(self.ratio, 4),
            "verdict": self.verdict,
            "construction_flag": self.construction_flag,
            "baseline_eff": round(self.baseline.efficiency, 4),
            "mtp_eff": round(self.mtp.efficiency, 4),
            "notes": self.notes,
        }
