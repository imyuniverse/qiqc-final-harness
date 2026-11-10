# Net-zero CZ solver — what it does and what it measured

`cz_agent.py` is a measured-in-situ solver for the tunable-coupler CZ task. It talks
to the task's own MCP service (the URL the runner puts in `QIQC_MCP_SERVERS`) and
assumes nothing about the device: every value in the answer is measured on the
current cooldown, the same way a lab would.

Run the whole campaign:

```sh
python3 harness/cz_agent.py all
```

Stages can be re-run alone (`idle`, `cryo`, `chevron`, `rabi`, `tune`, `verify`,
`submit`); each writes its raw data to `$QIQC_CZ_STATE` (default `/tmp/qiqc-cz`),
so a later stage reuses earlier measurements instead of re-spending shots.

## Stage 1 — coupler decoupling null (`idle`)

Static-ZZ Ramsey: q1 in `|+>`, q2 in `|0>` or `|1>`, a 2 µs idle, four projections
per branch. Scan the coupler flux over [0.245, 0.290] and take the minimum of the
conditional phase, refined by a parabola. This is the bias where `J_eff` and
`zeta` both vanish, i.e. the idle parking spot.

## Stage 2 — flux-line settling (`cryo`)

Square-step cryoscope on the quadratic sweet-spot arc: q1 in `|+>`, N samples of
0.20 Φ₀, then `ry(±π/2)` / `rx(±π/2)`; N = 1…100 at 8192 shots per quadrature,
with the coupler parked at the decoupling null so the drive is single-qubit.
The two quadrature means fix the common readout offset, `atan2` gives θ(N), and a
separable non-linear least squares fits two discrete first-order poles

    s[n] = 1 - Σ_k A_k (1 - α_k)^n ,  α_k = Δt / (τ_k + Δt),  Δt = 0.4 ns

with the model weight pinned to one (the transient is linear in `A_k`, so a free
weight is degenerate with a common amplitude scale). The fit also rejects
pole banks whose inverse is not minimum-phase.

## Stage 3 — `|11>-|02>` crossing (`chevron`) and the gap (`rabi`)

A 2-D chevron: prepare `|11>`, hold a square flux pulse for 10…120 ns, read the
`q2 -> 2` population, over eleven fluxes spanning [0.264, 0.274]. Fitting
`P(t) = ½ - ½cos(2πΩt)` with `Ω(Φ) = sqrt((ω₁(Φ) - ω₂ - α₂)² + 2J²)` returns the
crossing (hence `α₂`, `Φ_cross`) and a cross-check on `J`. A smooth-ramp Rabi at
the crossing then measures the `|11>-|02>` rate directly, `J = f/√2`, at the
declared gate bias.

## Stage 4 — pulse design

Mirrored (net-zero by construction) fast-adiabatic trajectory: a raised-cosine
ramp to a hold at `ω_cross + δ_hold`, then the same half with the flux sign
flipped, 2 ns ramp / 22 ns hold per half, 52 ns total. The programmed DAC array
is the exact rational inverse of the recovered settling (same recursion with
numerator and denominator swapped), quantised on the 16-bit / 0.4 ns AWG and
kept inside its ±0.70 Φ₀ range.

## Stage 5 — conditional-phase loop (`tune`)

`φ₂Q` is measured, not predicted: q1 in `|+>`, q2 in `|0>` or `|1>`, four
projections per branch, and `φ₂Q = φ(q2=1) - φ(q2=0)`. The four-projection
estimator `atan2(B-D, C-A)` cancels the readout offset and visibility exactly,
so no separate readout calibration is needed. A coarse scan over `δ_hold`
unwraps the phase across the whole physical window, brackets `π`, and a secant
iteration lands on it; two further measurements confirm the operating point.

Because the hold frequency is measured through a fitted crossing, the phase is
*not* assumed to be a linear function of `δ_hold` — the loop closes on the shot
data itself, which is what makes it robust to a ±10 MHz error in `α₂`.

## Stage 6 — verification and submission (`verify`, `submit`)

Leakage from the four computational inputs (level 2 on either qubit), `φ₂Q`,
the two single-qubit phases (`φ₀₁`, `φ₁₀`) that become the virtual-Z corrections,
and the static ZZ at the idle bias. Then `stage_a` / `stage_b` / `stage_c` are
assembled and pushed through the task's own `submit_final_answer`.

## Changing the runtime

`harness.json` carries only `runtime`. It is set to `deepseek`; change the single
value to `codex` or `pi` to run the same solver on another native CLI. The solver
is plain Python 3 + numpy + scipy, so it runs under any of them.
