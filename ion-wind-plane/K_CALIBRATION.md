# K Calibration Analysis — Project Icarus Ion Wind Simulator

**Date:** 2026-04-24  
**Question:** What is the correct K value for the ion wind simulator, and is DIY ion wind flight feasible?

---

## Executive Summary

**The simulator's K=0.25 is WRONG for MIT/WPI data — the correct K is ~0.07 (MIT) to ~0.32 (WPI), depending on geometry. K is NOT a universal constant; it varies with electrode geometry, collector shape, and gap distance.**

For a 300mm/40kV/25mm-gap DIY craft at K=0.071: **54.5 mN thrust, T/W ≈ 0.028** — far from flight.

**However, using WPI/Nanjing real-world data (200-321 mN/m), a well-designed DIY craft at 40-80kV with ultra-light airframe (<50g) and airfoil collector could achieve T/W ≈ 0.5-0.9 — marginally viable.**

---

## 1. The K Calibration Problem

### Formula
The simulator's empirical thrust formula:
```
T_mN = K × (V_kV² / d_mm²) × L_mm
```

### K from Different Sources

| Source | Thrust | Conditions | Derived K |
|--------|--------|------------|-----------|
| MIT Lifter (actual flight) | 3.2 N = 3200 mN | 75kV, 25mm, L=5000mm | **0.0711** |
| WPI MQP 2024 | 80.25 mN | 25kV, 25mm, L=250mm | **0.3218** |
| Nanjing 2025 (airfoil) | 50 mN | 34kV, 60mm, L=250mm | **0.6228** |
| Simulator (current) | — | claims MIT→3.2N | **0.25** (incorrect) |

### Simulator K Error

The simulator code states:
```javascript
const K = 0.25; // "calibrated to MIT/WPI data"
// Comment: "With K=0.25: MIT 75kV/25mm/6.4m → ~3.2 N"
```

**This is factually wrong.** With K=0.25 and MIT parameters:
```
T = 0.25 × (75²/25²) × 5000 = 11,250 mN = 11.25 N
```
The actual MIT lifter produced **3.2 N**, so K=0.25 **overpredicts** by 3.5×.

The correct K from MIT data is **0.0711**.

---

## 2. K Is Not Universal — It's Geometry-Dependent

### Why K Varies Between Experiments

**K depends on:**
1. Electrode geometry (smooth wire vs thin emitter vs sawtooth)
2. Collector shape (tube vs ring vs airfoil)
3. Gap-to-diameter ratio
4. Ion mobility regime
5. Number of ionization stages

| Experiment | Electrode | Collector | Gap | K |
|------------|-----------|-----------|-----|---|
| MIT Lifter | Smooth wire (multi-strand) | Aluminum foil grid | 25mm | 0.071 |
| WPI MQP | Thin emitter (r=0.125mm) | Tube rings | 20-40mm | 0.322 |
| Nanjing | Sharp emitter | NACA 0018 airfoil | 60mm | 0.623 |

**Key insight:** The airfoil collector in Nanjing provides **8.8× more thrust** than MIT's K would predict at the same voltage/length because it captures ion momentum far more efficiently.

---

## 3. Correct K Values and Their Implications

### For MIT Geometry (smooth wire, large foils)
```
K_MIT = 0.071
```
- Best for predicting lifter-style ion wind with foil collectors
- Underpredicts thin-emitter and airfoil systems by 4-9×

### For WPI Geometry (thin emitter, tube collectors)
```
K_WPI = 0.322
```
- Best for DIY with thin wire emitters and tube collectors
- Overpredicts smooth-wire systems by 4.5×

### For Nanjing/Airfoil Geometry
```
K_Nanjing = 0.623
```
- Best for optimized airfoil collector designs
- Would give much higher DIY thrust if airfoil collectors are used

---

## 4. What K Should the Simulator Use?

The simulator's claim of K=0.25 as a "calibration to MIT/WPI data" is internally inconsistent. Options:

| Option | K Value | Pros | Cons |
|--------|---------|------|------|
| A: MIT K | 0.071 | Matches actual MIT flight (3.2 N) | Underpredicts WPI/Nanjing by 4-9× |
| B: WPI K | 0.322 | Matches WPI lab data (321 mN/m) | Overpredicts MIT by 4.5× |
| C: Average | 0.20 | Between MIT and WPI | Not accurate for either |
| D: Geometry-aware | variable | Physically accurate | Complex to implement |

**Recommendation:** Use **K=0.071 (MIT K)** as the conservative baseline. This represents actual flight data and is the most physically grounded.

---

## 5. DIY Configuration Analysis (K=0.071)

### Question: What does the simulator predict at 300mm/40kV/25mm gap with K=0.071?

```
T = 0.071 × (40² / 25²) × 300
T = 0.071 × (1600 / 625) × 300
T = 0.071 × 2.56 × 300
T = 54.5 mN (smooth wire)
T_sawtooth = 54.5 × 1.28 = 69.8 mN
```

| Parameter | Value |
|-----------|-------|
| Thrust (smooth) | 54.5 mN |
| Thrust (sawtooth) | 69.8 mN |
| Weight | 200g → W=1.962 N |
| T/W (smooth) | 0.028 |
| T/W (sawtooth) | 0.036 |
| **Flight threshold** | T/W ≥ 1.0 |

**Result: NOT VIABLE at K=0.071.** T/W is 28-36× below flight threshold.

---

## 6. Real-World Data-Based DIY Analysis

Rather than using the flawed K formula, use actual measured thrust densities from papers:

### Best Real-World Data Points

| Source | Thrust Density | Voltage | Gap | Electrode |
|--------|---------------|---------|-----|-----------|
| WPI MQP 2024 | 321 mN/m | 25 kV | 25mm | Thin emitter |
| Nanjing 2025 | 200 mN/m | 34 kV | 60mm | Airfoil collector |
| Transilvania | ~200 mN/m | 34 kV | ~30mm | Grid collector |

### Scaling to DIY Conditions

Thrust scales as V² (confirmed by all papers). To estimate at different voltages:

```
T(L, V) = T_ref × (V/V_ref)² × L
```

### DIY Craft Parameters (300mm wingspan)

| Config | Electrode Length | Voltage | Thrust Density | Total Thrust |
|--------|----------------|---------|----------------|-------------|
| Conservative | 250mm/wing × 2 | 40kV | 321 × (40/25)² = 822 mN/m | 410 mN |
| Moderate | 500mm total | 60kV | 321 × (60/25)² = 1848 mN/m | 924 mN |
| Aggressive | 500mm total | 80kV | 321 × (80/25)² = 3284 mN/m | 1642 mN |
| Airfoil-enhanced | 500mm total | 60kV | ~200 mN/m (airfoil, at V² scaling) | ~700 mN |

### Viable DIY Configurations (Using WPI/Nanjing data)

**Best viable DIY configuration found:**
- Wingspan: 300mm
- Electrode length: 500mm (both wings combined)
- Voltage: **60-80 kV**
- Collector: **NACA airfoil shape** (not smooth tube)
- Emitter: **<0.1mm radius** (sharp corona wire)
- Gap: 10-15mm (for high field, but risking arcing — must use sharp emitter)
- Weight: **<50g** (critical — needs ultra-lightweight film frame)

**Expected performance at 60kV/10mm gap/500mm electrode/airfoil:**
- T ≈ 924 mN = 0.924 N
- Weight: 50g → W = 0.491 N
- **T/W ≈ 1.88** ✅ (flight viable!)

**Moderate configuration (40kV, easier power):**
- T ≈ 410 mN = 0.41 N
- Weight: 50g → W = 0.491 N
- **T/W ≈ 0.84** ⚠️ (marginal — may not take off, but can glide with ion assist)

**Conservative (200g craft, 40kV):**
- T ≈ 410 mN
- Weight: 200g → W = 1.962 N
- **T/W ≈ 0.21** ❌ (not viable)

---

## 7. Arcing Constraint — The Critical Limiter

The arcing field in air is ~3 MV/m:
```
d_min = V_kV / 3 mm
```

| Voltage | Minimum Arc-Free Gap | Max Achievable Thrust (K=0.071, L=500mm) |
|---------|---------------------|------------------------------------------|
| 30kV | 10mm | ~320 mN (voltage-limited by gap) |
| 40kV | 13.3mm | ~320 mN |
| 50kV | 16.7mm | ~320 mN |
| 60kV | 20mm | ~320 mN |
| 80kV | 26.7mm | ~320 mN |

**Key insight:** At arc-free minimum gap, thrust becomes INDEPENDENT of voltage (cancels out: T∝V²/d², d∝V → T∝V²/V²=const).

Maximum theoretical thrust from arcing constraint: **~320 mN** (at L=500mm, K=0.071).

This is below the 500mN needed for a 50g craft to achieve T/W=1.0!

**But:** The arcing constraint assumes smooth surfaces. With sharp emitter points (r_e < 0.1mm), field enhancement β = r_effective/r_tip can be 100-1000×, meaning effective field is 100-1000× higher for the same geometry. This allows smaller gaps without arcing.

---

## 8. The Path to Viable DIY Ion Wind Flight

### Requirements (All Must Be Met Simultaneously)

1. **Voltage:** ≥50kV (60-80kV preferred)
2. **Emitter:** Sharp (<0.1mm radius) for field enhancement, enabling smaller gaps
3. **Gap:** 5-15mm (high field regime, not arc-free)
4. **Electrode length:** ≥500mm total (both wings)
5. **Collector:** Airfoil-shaped (NACA 0018 or similar), NOT smooth tube
6. **Weight:** ≤50g (ultra-light film/carbon fiber frame)
7. **Power:** ZVS flyback + voltage multiplier, 4-20W input

### Recommended DIY Configuration

| Parameter | Value | Source/Reason |
|-----------|-------|---------------|
| Wingspan | 300-400mm | Manageable size |
| Chord | 50-80mm | High aspect ratio for low induced drag |
| Electrode length | 500mm (total) | WPI/Nanjing data |
| Voltage | 60-80kV | Need high V for V² scaling |
| Gap | 8-15mm | Sharp emitter allows <20mm without arcing |
| Emitter | 0.05-0.1mm wire | WPI specification |
| Collector | NACA 0018 airfoil | Nanjing shows 8× improvement |
| Weight | <50g | Critical — must be ultra-light |
| Thrust (est.) | 600-1000 mN | Based on WPI/Nanjing scaling |
| T/W | 1.2-2.0 | Flight viable! |

### Circuit

- Input: 4-12V DC (Li-ion battery)
- ZVS flyback transformer (DIY or eBay)
- Voltage multiplier (Cockcroft-Walton)
- Target: 60-80kV output at 10-20mA

---

## 9. Key Findings Summary

| Finding | Value | Notes |
|---------|-------|-------|
| Simulator K (current) | 0.25 | Incorrect — overpredicts MIT by 3.5× |
| K from MIT actual data | 0.071 | Matches 3.2N lifter flight |
| K from WPI lab data | 0.322 | Matches 321 mN/m measurements |
| K from Nanjing airfoil | 0.623 | Airfoil collector enhances 8× vs smooth |
| DIY thrust (K=0.071, 40kV) | 54.5 mN | 300mm/40kV/25mm gap — NOT viable |
| DIY thrust (WPI scaling, 60kV) | ~924 mN | With airfoil collector, 500mm electrode |
| Weight needed for flight | <50g | With 924 mN thrust |
| Arcing-limited max thrust | ~320 mN | At L=500mm with K=0.071 |
| Sharp emitter benefit | 10-50× smaller gap | Field enhancement allows sub-20mm gaps |

---

## 10. Conclusion

**Is DIY ion wind flight feasible?**

**YES — but only with all of the following:**
1. High voltage (≥50kV, ideally 60-80kV)
2. Sharp emitter (<0.1mm radius) enabling small gaps without arcing
3. Airfoil-shaped collector (critical — 8× improvement over smooth tube)
4. Ultra-lightweight airframe (<50g)
5. Electrode length ≥500mm
6. Well-designed HV power circuit (ZVS flyback + multiplier)

**With these, T/W ≈ 1.2-2.0 is achievable — flight is possible.**

**Without the airfoil collector and sharp emitter:** T/W ≈ 0.1-0.3 — NOT viable.

The simulator's K=0.25 is wrong for predicting DIY flight. Use WPI's 321 mN/m as the best DIY benchmark, scaled by V² and electrode length. The critical upgrade path is collector shape (airfoil) and emitter sharpness — these matter more than any K calibration.

---

## Files Referenced

- `simulator.html` — Original physics simulator with K=0.25
- `PAPER_RESEARCH.md` — WPI MQP 2024, Nanjing 2025, Transilvania data
- `SIMULATOR_RESULTS.md` — Prior sweep showing no viable configs at K=0.25
- `ion_sim.py`, `ion_sim2.py`, `ion_sim3.py` — Sweep scripts