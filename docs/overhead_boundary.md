# The overhead boundary — the un-flagged test of MTP-as-stopping

This is the test the RH and control domains could not be: one where the
non-refutation stopping rule has a **ground truth it can get wrong**, so a "win"
is not true by construction. It also answers the philosophical worry directly:
*if MTP is only a cost/compression principle, does "keep searching but stop at a
floor" collapse into nihilism, or is it a real methodology?*

## Setup (see `adapters/sequential.py`, pre-registered in PREREGISTRATION §3d)

A population of conjectures. Each is TRUE (no counterexample in the horizon
`[0, M)`) or FALSE (a counterexample at `x ~ Geometric(r)`). Checking candidate
`t` reveals whether it refutes; each check costs one unit (+ Landauer entropy).

- **baseline** — exhaustive scan to `M`; always correct within the horizon.
- **mtp** — the *non-refutation floor*: after surviving `[0, t)` with no
  counterexample, the posterior that one still remains is
  `q(t) = π0·S(t) / [(1−π0) + π0·S(t)]`. Stop at the smallest `t` with `q(t) ≤ ε`.
  `ε` is set by the Landauer marginal-cost / stake ratio — principled, not tuned.

The **overhead boundary** is `t_floor(ε)`: the point past which the posterior
chance of a surviving counterexample is below `ε`, so further checking buys
(almost) no refutation power but keeps spending entropy.

## Result 1 — the risk is provably bounded (non-nihilism)

There is a theorem: under a correct prior, the miss rate (a FALSE conjecture
whose counterexample sits beyond the floor) obeys
`miss_rate = π0·S(t_floor) ≤ ε(1−π0)`. The experiment confirms it to the digit:

| ε | t_floor | miss rate | bound ε(1−π0) | compute saved |
|------|--------:|----------:|--------------:|--------------:|
| 0.05 | 146 | 0.0269 | 0.0250 | 96.2% |
| 0.01 | 228 | 0.0052 | 0.0050 | 94.5% |
| 0.005| 263 | 0.0027 | 0.0025 | 93.8% |
| 0.001| 342 | 0.0008 | 0.0005 | 92.2% |

So "stop at the floor" is **not** a surrender: it saves >90% of the work while
keeping the missed-refutation probability *quantitatively bounded by a knob you
choose*. The act of continuing to search up to — and only up to — the floor is a
legitimate, risk-controlled methodology. That is the concrete reason this does
not collapse into nihilism. (Left panel of
`results/sequential_overhead_boundary.png`: empirical miss rate hugs the bound.)

## Result 2 — but the saving is bought with an assumption, and the ratio is only neutral

The scorecard's efficiency ratio for this domain is **0.98 (neutral)**, *despite*
the 94% compute saving. The reason is the honest core of the whole project: the
floor buys its savings with an **extra modeling assumption** (the generative
prior `π0, r`). In `efficiency = phenomena / (params + assumptions + compute_norm)`
the added assumption and the tiny coverage loss almost exactly cancel the compute
gain. MTP here is an **assumption-for-compute trade**, not a free compression.

## Result 3 — and the assumption is exactly what breaks (the failure mode)

Under distribution shift — the true counterexample tail 4× heavier than the prior
expects — the floor becomes over-confident: at ε = 0.01 the miss rate jumps to
**0.156**, ~31× its bound, while still "saving" 93% of compute (red point, left
panel). The bound is only as good as the prior, and prior misspecification is the
precise way the method fails.

## What this establishes

- MTP-as-stopping is a **real, risk-bounded methodology**, not nihilism: the
  overhead boundary exists and is locatable, with a provable risk knob (Result 1).
- It is a **conditional compression**, not a universal one: it trades a modeling
  assumption for compute (Result 2), a net win only when compute is the
  bottleneck *and* the prior holds.
- Its failure mode is **prior misspecification** (Result 3) — which is also why
  the cosmology instantiation failed: windowed-IDE added structural assumptions
  the data did not reward.

This is consistent across the scorecard: MTP earns its keep as a **verification /
stopping** principle with bounded risk, and loses whenever the task requires
*adding* believed structure rather than *cutting* wasteful accumulation.
