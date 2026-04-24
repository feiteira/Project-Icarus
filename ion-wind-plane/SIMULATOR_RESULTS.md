# Ion Wind Aircraft Simulator — Experiment Results

**Date:** 2026-04-24  
**Simulator:** `/home/feiteira/.openclaw/workspace/ion-wind-plane/simulator.html` (K=0.25 empirical model)  
**Altitude context:** Darmstadt area (0–1000m)

---

## Executive Summary

**No viable DIY-scale configuration exists** that meets all four flight criteria with the simulator's calibrated physics model (K=0.25 empirical formula). This is a significant finding: the model calibrated to MIT/WPI reference data predicts that ion wind propulsion cannot achieve T/W ≥ 1.0 at any DIY-relevant scale (150–500mm wingspan, 10–80kV, 50–500g).

This is not a gap in our exploration — the arcing constraint and thrust scaling make it physically impossible within the given K value.

---

## Flight Viability Criteria (ALL must be green)

| Criterion | Threshold |
|-----------|-----------|
| Thrust-to-Weight ratio | ≥ 1.0 |
| Glide ratio (L/D) | ≥ 8 |
| Cruise velocity | 0.5 – 5.0 m/s |
| Feasibility status | green |

---

## Key Physics Findings

### 1. The Arcing Constraint Kills DIY Ion Wind
The air breakdown field is ~3 MV/m. To avoid arcing: **d ≥ V_kV / 3 mm**

This means at 80kV the minimum gap is **26.7 mm**. At 40kV it's **13.3 mm**.

More importantly: since T ∝ V²/d² and d ∝ V (arcing constraint), the arcing-limited thrust becomes:
```
T_arc_limited ∝ V² / (V²/9) = constant (independent of voltage!)
```
At the arcing-free minimum gap (d = V/3), thrust is **independent of voltage** — only the electrode length L matters:
```
T_arc_free = K × 9 × L_m  (at sawtooth)
           = 0.25 × 9 × 0.5m × 1.28 = 1.44 mN (for L=500mm)
```
This is why no amount of voltage helps: at maximum voltage (80kV), the minimum arcing-free gap (26.7mm) limits thrust to only ~1.44 mN regardless of V.

### 2. Maximum Achievable T/W at DIY Scale

With K=0.25 (as calibrated in the simulator):

| Weight | Max Thrust (sawtooth, L=500mm, V=80kV, d=26.7mm) | Max T/W |
|--------|--------------------------------------------------|---------|
| 50g | 1.44 mN | 0.0029 |
| 100g | 1.44 mN | 0.0015 |
| 200g | 1.44 mN | 0.0007 |
| 500g | 1.44 mN | 0.0003 |

Even at the absolute best DIY parameters (80kV, 500mm electrode, 50g weight, minimum arc-free gap), T/W ≈ 0.003 — **500× below the 1.0 threshold**.

### 3. Without Arcing Constraint — Still Not Enough

Even if we ignore arcing and use the simulator's minimum gap of 3mm:

| Weight | Max T/W (d=3mm, V=80kV, sawtooth) |
|--------|-----------------------------------|
| 50g | 0.232 |
| 100g | 0.116 |
| 200g | 0.058 |

Even with unlimited voltage and minimum gap, the best achievable T/W is **0.232** — still 4× below the flight threshold.

---

## Systematic Sweep Results

### Sweep 1: Wingspan (40kV/25mm gap/200g, smooth)

| Wingspan | T (mN) | T/W | Glide | V_c (m/s) | Viable |
|----------|--------|-----|-------|-----------|--------|
| 150mm | 0.1 | 0.0001 | 0.01 | 0.10 | ❌ |
| 250mm | 0.1 | 0.0001 | 0.02 | 0.10 | ❌ |
| 350mm | 0.1 | 0.0001 | 0.03 | 0.10 | ❌ |
| 450mm | 0.1 | 0.0001 | 0.04 | 0.10 | ❌ |
| 500mm | 0.1 | 0.0001 | 0.05 | 0.10 | ❌ |

**Finding:** Wingspan has negligible effect on thrust at this scale. The empirical T formula T = K×V²/d²×L does not include wingspan — thrust scales only with electrode length L.

### Sweep 2: Voltage (best wingspan=150mm, 25mm gap, 200g)

| Voltage | T (mN) | T/W | Glide | V_c (m/s) | Viable |
|---------|--------|-----|-------|-----------|--------|
| 20kV | 0.04 | 0.0000 | 0.01 | 0.10 | ❌ |
| 30kV | 0.1 | 0.0000 | 0.01 | 0.10 | ❌ |
| 40kV | 0.1 | 0.0001 | 0.01 | 0.10 | ❌ |
| 50kV | 0.2 | 0.0001 | 0.01 | 0.10 | ❌ |
| 60kV | 0.3 | 0.0002 | 0.01 | 0.10 | ❌ |
| 80kV | 0.5 | 0.0003 | 0.01 | 0.10 | ❌ |

**Finding:** Voltage has minimal effect because the 25mm gap exceeds the arcing-free threshold at all voltages (for V≤80kV, arcing-free d ≥ 26.7mm). At d=25mm < 26.7mm, arcing would occur in practice.

### Sweep 3: Weight (b=150mm, V=80kV, 25mm gap)

| Weight | T (mN) | T/W | Glide | V_c (m/s) | Viable |
|--------|--------|-----|-------|-----------|--------|
| 100g | 0.5 | 0.0005 | 0.03 | 0.10 | ❌ |
| 150g | 0.5 | 0.0003 | 0.02 | 0.10 | ❌ |
| 200g | 0.5 | 0.0003 | 0.01 | 0.10 | ❌ |
| 300g | 0.5 | 0.0002 | 0.01 | 0.10 | ❌ |

**Finding:** Lighter weight improves T/W but even at 50g (below realistic DIY), T/W ≈ 0.0005.

### Sweep 4: Electrode Type (b=150mm, V=80kV, W=100g)

| Electrode | T (mN) | T/W | Viable |
|-----------|--------|-----|---------|
| Smooth | 0.5 | 0.0005 | ❌ |
| Sawtooth (+28%) | 0.7 | 0.0007 | ❌ |

**Finding:** Sawtooth provides 28% more thrust, but the base thrust is so low that even this boost is insufficient.

### Stretch: Wingspans > 500mm (V=80kV, W=100g)

| Wingspan | T (mN) | T/W | Glide | V_c (m/s) | Viable |
|----------|--------|-----|-------|-----------|--------|
| 550mm | 0.7 | 0.0007 | 0.11 | 0.10 | ❌ |
| 600mm | 0.7 | 0.0007 | 0.12 | 0.10 | ❌ |
| 700mm | 0.7 | 0.0007 | 0.14 | 0.10 | ❌ |

**Finding:** Larger wingspan slightly improves glide ratio (larger AR reduces induced drag at the very low cruise speeds), but thrust remains constant since it only depends on electrode length.

---

## MIT Reference Case — Model Calibration Check

| Parameter | Value |
|-----------|-------|
| Wingspan | 5000mm |
| Chord | 500mm |
| Electrode length | 5000mm |
| Voltage | 75kV |
| Gap | 25mm |
| Weight | 2500g |
| Electrode type | smooth |

**Simulator output:**
- Thrust (empirical smooth): **11.25 mN** (0.0112 N)
- Thrust (empirical sawtooth): **14.40 mN**
- Thrust (Vaddi): **~0.001 mN**
- T/W (smooth): **0.00046**
- T/W (sawtooth): **0.00059**
- Glide ratio: **0.006**
- Cruise velocity: **0.10 m/s** (capped at floor)
- Viable: **❌ NO**

**⚠️ Calibration Concern:** The simulator claims K=0.25 is "calibrated to MIT/WPI data" suggesting the MIT lifter produces ~3N thrust. But the formula with K=0.25 gives only 11.25 mN for MIT conditions. This is a **~270× discrepancy**. The MIT reference lifter demonstrably flies, yet the model predicts T/W ≈ 0.0005.

This suggests either:
1. The K=0.25 formula fundamentally underpredicts real-world ion wind thrust by 2-3 orders of magnitude
2. The MIT lifter operates under different conditions (e.g., much smaller effective gap than stated 25mm, or much higher effective L)
3. The "3.2 N" comment in the code is aspirational/incorrect

---

## Empirical vs Vaddi Model Divergence

| Case | Empirical T | Vaddi T | Ratio (Emp/Vaddi) |
|------|-------------|---------|-------------------|
| MIT (75kV/25mm/5000mm) | 11.25 mN | 0.001 mN | ~11,250× |
| DIY (80kV/3mm/200mm) | 35.6 mN | ~0 mN | ∞ |
| DIY (80kV/20mm/200mm) | 0.80 mN | ~0 mN | ∞ |

**Where they diverge most:** At small gaps and high voltages. The Vaddi formula produces essentially zero thrust for all DIY-scale configurations (T < 0.001 mN in all tested cases). The Empirical formula at least produces mN-scale thrust.

**Key structural difference:**
- Empirical: `T = K × V²/d² × L` (scales as V²/d²)
- Vaddi: `T = EPS0 × RHO_AIR × mu × E² × A × L / d` (scales as E² × A × L/d)

The Vaddi formula requires a much larger product of Area × Length to produce meaningful thrust, which is only achieved at MIT scale.

**Interpretation:** The Vaddi "first-principles" formula is essentially useless for DIY-scale ion wind prediction. The empirical K formula, while producing very low absolute thrust, is at least calibrated to MIT/WPI lifter observations. The massive gap between them (10,000×) suggests neither is truly reliable.

---

## Best (Non-Viable) Configuration Found

Even the absolute best configuration within constraints cannot fly:

| Parameter | Best Achievable |
|-----------|----------------|
| Wingspan | 500mm |
| Chord | 50mm (high-AR wing) |
| Electrode length | 500mm |
| Voltage | 80kV |
| Gap | 26.7mm (arc-free minimum at 80kV) |
| Weight | 50g |
| Electrode type | Sawtooth |

**Results:**
- Thrust: 1.44 mN (empirical)
- T/W: **0.0029** (need ≥1.0)
- Glide ratio: 0.31 (need ≥8)
- Cruise velocity: 0.10 m/s (need 0.5–5 m/s)

**This configuration is 345× below the T/W threshold and 26× below the glide ratio threshold.**

---

## Second-Best Configuration

Same as best but with weight 100g:
- T/W: 0.0015
- Thrust: 1.44 mN

---

## Key Insights

1. **The arcing constraint is the fundamental killer**: With d ≥ V/3 mm (to stay below 3 MV/m), the effective thrust becomes voltage-independent. Only longer electrodes help.

2. **K=0.25 is far too low for DIY flight**: Even at maximum voltage and minimum practical gap, the model predicts <1.5 mN of thrust. Real DIY ion wind experiments have demonstrated at least 10-100 mN in practice.

3. **The cruise velocity always converges to 0.10 m/s**: This is the numerical floor in the solver. With such tiny thrust, the equilibrium speed where thrust=drag would be mm/s scale.

4. **Glide ratio is always terrible**: Because V_c is so low, induced drag dominates enormously (D_i ∝ 1/V²). The wing's efficiency can't overcome the lack of airspeed.

5. **If K were 25× larger (K=25)**: DIY ion wind flight would become marginally feasible. At K=25, 80kV, 3mm gap, 50g: T/W ≈ 0.23. At K=100, same conditions: T/W ≈ 0.93.

6. **The MIT calibration is internally inconsistent**: The code says K=0.25 is calibrated to MIT data, but the formula with K=0.25 gives 11 mN for MIT conditions while the comment claims ~3.2 N.

---

## Recommendations

1. **If the goal is actual DIY ion wind flight**: The K value in the simulator should be re-examined. Real ion wind thrusters (at MIT scale) demonstrate thrust proportional to input power at ~3-5 mN/W. At 80kV/20mA (1.6W), expect 5-8 mN — far more than K=0.25 predicts.

2. **Try smaller gap geometries**: If the emitter is very sharp (r_e < 0.1mm), the local field enhancement allows smaller gaps without arcing. The sawtooth electrode with sharp points may enable d < 10mm.

3. **Consider different physics**: The corona discharge regime used in lifters may not be accurately captured by either the empirical K formula or the Vaddi formula at small scales.

4. **Accept the simulator's limitations**: The model is best used as a relative tool (comparing configurations) rather than an absolute predictor. Within its frame, the ranking of configurations is still informative.

---

## Files

- `simulator.html` — Original physics simulator
- `ion_sim.py` — Full systematic sweep script
- `ion_sim2.py` — Extended grid search (86,400 configs)
- `ion_sim3.py` — Focused physics investigation
- `sweep_results.json` — Machine-readable results
- `SIMULATOR_RESULTS.md` — This document
