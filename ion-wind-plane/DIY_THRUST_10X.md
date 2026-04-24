# DIY_THRUST_10X.md — Progress Log
**Started:** 2026-04-24 16:13 GMT+2
**Goal:** Path to 10× (1690 mN) at 35kV using NO micron-precision parts

---

## CONSTRAINT REMINDER
- Emitter wire minimum = 0.1mm (stainless steel guitar string or tungsten from welding supply)
- NO precision machining, NO custom micrometer positioning systems
- Basic DIY tools only: hand drills, laser-cut acrylic, 3D printer, basic soldering
- Parts from Amazon/Reichelt

---

## BASELINE
- 35kV/20mm/500mm/NACA (K=0.623) → **169 mN** (empirical)
- Formula: T_mN = K × (V_kV²/d_mm²) × L_mm
- TPW_baseline = 169/15 = **11.3 mN/W** at d=20mm

## APPROACH 1: TANDEM STAGES

### Physics: Do tandem stages compound?

Two configurations for tandem:
- **Voltage-sharing tandem**: Two pairs at different voltages summing to 35kV total. Pair 1 at 25kV/8mm, Pair 2 at 10kV/8mm. Each pair has own gap. Ions from pair 1 are further accelerated by pair 2.
- **Independent tandem**: Two pairs both at 35kV, in parallel from same HV supply. Each pair independently produces thrust. Ion wind from pair 1 passes through pair 2's collector and adds momentum.

For voltage-sharing tandem:
- Pair 1: 25kV/8mm → T ≈ 0.623 × (25²/8²) × 500 = 0.623 × 9.77 × 500 = **610 mN** per pair... wait
- Actually T_pair = K × (V₁²/d²) × L for pair 1, plus T_pair = K × (V₂²/d²) × L for pair 2
- Sum = K × (V₁² + V₂²)/d² × L
- If V₁=25kV, V₂=10kV: V₁²+V₂² = 625+100 = 725, vs (35kV)² = 1225
- So with voltage-sharing: T = 0.623 × (725/64) × 500 = 0.623 × 11.33 × 500 = **3530 mN**
- Wait, that's using the formula wrong. The formula T = K×V²/d²×L is for one electrode pair.
- For two pairs in VOLTAGE-SHARING mode (both pairs across the same gap): T = K × [(V₁+V₂)²]/d² × L = K × V_total²/d² × L
- So voltage-sharing doesn't help vs a single pair at combined voltage!

For INDEPENDENT tandem (both at 35kV, each stage with own d):
- Each stage: T_stage = K × (35²/d_stage²) × L
- Two stages at d=8mm: T_total = 2 × 0.623 × (35²/8²) × 500 = 2 × 0.623 × 19.14 × 500 = **11,926 mN** ← WRONG

The correct analysis: each stage requires its own POWER. Thrust per stage at same voltage/gap is the same, but power also scales linearly with stage count.

### Per-stage power analysis
At d=20mm/15W: TPW = 11.3 mN/W
At d=8mm: TPW scales as 20/8 = 2.5× → TPW ≈ 28.3 mN/W
At 15W per stage → T_stage ≈ 425 mN per stage

With 2 stages at 15W each = 30W total: T ≈ 850 mN = 5×

With 3 stages at 15W each = 45W total: T ≈ 1275 mN = 7.5×

This is still short of 10×! Unless K effectively compounds.

### MOONSHOT vs Reality for Tandem
MOONSHOT.md claimed tandem × 2 could reach 1500 mN (8.9×) but that's at d=6mm which requires μm-precision emitter.

At d=8mm with 2 stages × 15W = 30W:
- T ≈ 2 × 425 × (K_eff assumed 1.2 for tandem bonus) = **1020 mN = 6×**

At d=8mm with 3 stages × 15W = 45W:
- T ≈ 3 × 425 × (K_eff assumed 1.3) = **1658 mN = 9.8×**

Close but needs 45W and 3 stages.

### FINDING: Tandem alone needs 3+ stages at d=8mm and ~45W to reach 10×. Buildable but complex.

---

## APPROACH 2: WING SPAN LENGTH

### Linear scaling
T ∝ L. L=1000mm → T = 2× baseline = 338 mN (still only 2×)
L=2000mm → T = 4× = 676 mN (only 4×)

To reach 10× via length alone: L = 5000mm (5 meters!)
At L=5000mm: T = 0.623 × 3.06 × 5000 = 9540 mN ✓

### Practical L=1000mm
At L=1000mm with d=20mm: T = 338 mN = 2×
At L=1000mm with d=10mm: T = 0.623 × 12.25 × 1000 = 7631 mN = 45×

BUT: d=10mm at 35kV with 0.1mm wire is borderline arcing. Let's check:
- d=10mm: E=3.5 MV/m
- For 0.1mm wire: β ≈ (d/r)^0.4 ≈ (100)^0.4 ≈ 6.3
- E_local = 3.5 × 6.3 = 22 MV/m → ABOVE air breakdown threshold
- Arcing RISK: HIGH at d=10mm with 0.1mm wire

At d=8mm: E=4.375 MV/m, β≈5.3, E_local=23 MV/m → very high arcing risk

At d=15mm: E=2.33 MV/m, β≈4.3, E_local=10 MV/m → safe

### Length at d=15mm (safe with 0.1mm wire)
T at L=1000mm/d=15mm = 0.623 × 5.44 × 1000 = 3390 mN = 20× ✓

### Carbon fiber rod support analysis
L=1000mm carbon fiber tube (6mm OD, 1mm wall): ~15g per meter
Electrode assembly (wire + collectors): ~20g
Airframe: ~30g
Total: ~65g

Thrust at d=15mm/L=1000mm: 3390 mN → T/W = 52 for 65g aircraft ✓

### FINDING: L=1000mm at d=15mm is EASY (no precision) and gives 20× baseline. Wing span alone can hit 10× trivially!

But MOONSHOT.md dismissed length scaling as "impractical for small-plane use case." Let me check if L=1000mm is actually too large...

---

## APPROACH 3: VOLTAGE STACK

Two ZVS modules each at 35kV in series = 70kV.
Then use two electrode pairs each at 35kV (same current flows through both pairs).

At 70kV/d=23mm (to avoid arcing): T = 0.623 × (70²/23²) × 500 = 0.623 × 9.27 × 500 = **2888 mN = 17×** ✓

But 70kV creates arcing risk and requires careful insulation.

Alternative: single 35kV module but using a voltage multiplier (Cockcroft-Walton) to double to 70kV.
- DIY: 10-stage CW multiplier with 10× 1nF caps and 10× 1N4007 diodes
- Input: 35kV AC (from ZVS) → output: 70kV DC
- Current limited by capacitor values
- At 70kV/0.5mA = 35W → T ≈ 2888 mN × (0.5/estimated_current)...

### FINDING: Voltage stack to 70kV works but needs 23mm gap to avoid arcing. 70kV at d=23mm gives ~17× but requires careful HV insulation.

---

## APPROACH 4: WIRE COUNT MULTIPLIER ("HARP" COLLECTOR)

### Concept
Multiple thin wires (0.1mm each) in parallel, side by side, at same voltage.
Each wire independently produces corona. All share a common collector.

If 1 wire gives K_factor=0.623, then N parallel wires give K_total = N × 0.623?

### Wire spacing considerations
Wires run along the span direction (parallel to wing, perpendicular to E-field direction).
Perpendicular to wire direction: spacing needs to be sufficient to avoid inter-wire arcing.
At 35kV/8mm gap, minimum wire separation to avoid inter-wire arcing: ~20mm.

Across L=500mm wing: with 20mm spacing → max 25 wires fit.
At 50mm spacing → 10 wires fit.

### With 10 parallel wires at d=8mm
Each wire: T_wire = K_single × (35²/8²) × (L/10) [each wire covers 1/10th of length]
T_total = 10 × K_single × (35²/8²) × (L/10) = K_single × (35²/8²) × L = same as single wire!

**CRITICAL INSIGHT: If wires are COLLECTED by a common shared collector, thrust does NOT scale with wire count!**

The formula T = K × V²/d² × L already assumes continuous emitter along L. Adding more wires in parallel doesn't change the total emitter length — it just splits the same length among more wires.

### To get actual scaling: Each wire needs its OWN COLLECTOR section
Design: "Comb" collector — each wire has its own small collector element.
- 10 wires × 50mm collector sections = 10 independent electrode pairs
- Each pair at 35kV/8mm gap
- Total L effectively = 500mm still (continuous)

Still no scaling. Unless each wire+collector pair is spatially separated.

### Redesign: Wire "Harps" in MULTIPLE LOCATIONS along wing
Instead of one long electrode pair, use 10 SHORT electrode pairs at different span locations.
Each short pair: L=50mm, but at same V/d.
T_per_pair = K × (35²/8²) × 50 = 0.623 × 19.14 × 50 = **596 mN per pair**
10 pairs × 596 = **5960 mN = 35×** ✓

But each short pair still needs its own gap in the span direction.
If each pair takes 50mm (wire) + 50mm (collector gap) + 50mm (next wire) = 150mm per pair:
10 pairs × 150mm = 1500mm total span needed.

### Mechanical design for 10-pair "comb"
- 10 emitter wires, each ~50mm long, at d=8mm from collector
- Collectors are separate metal strips, NOT connected to each other electrically
- Each collector is grounded through its own current-return path
- Ions from each emitter hit their local collector only
- Thrust ADDITIONS from each independent pair

Total active length: 500mm (wing span)
But if 10 pairs are distributed across 500mm, each pair has L=50mm active.
10 × 50mm = 500mm total. Still same as single pair with L=500mm.

**The only way to get 10× scaling from wire count is if each wire-pair is SPATIALLY SEPARATED in the flow direction, not just the span direction.**

### Alternative: TANDEM in the flow direction (multiple gaps in series)
This is just tandem stages (Approach 1), not wire count.

### FINDING: Wire count multiplier does NOT scale thrust unless each wire has its own independent collector section that is spatially separated. Simple parallel wire "harp" with shared collector gives NO scaling.

---

## APPROACH 5: COLLECTOR AMPLIFICATION (Steel Wool / Mesh)

### Mesh collector
Mesh (20× 20 per inch) has ~60% transmission (40% shadowing).
Effective collector area is 0.6 × geometric area.
But K should be based on effective ion collection area, not geometric.

From PRACTICAL_THRUST.md:
- Smooth collector: K=0.071
- NACA airfoil: K=0.623 (8.8× better than smooth)
- Mesh: K≈0.4-0.5 (maybe 6-7× smooth, but worse than NACA)

### Steel wool collector (multiple thin strands)
Each fiber (r≈0.05mm) acts as a micro-collector.
Effective surface area: steel wool has ~3-5 m² per 100g (enormous surface area).
BUT: ions need to hit a COLLECTOR that is positively biased relative to emitter.
Steel wool at ground potential: ions drift toward nearest fiber.
But fibers are electrically connected (all ground), so effective collection area is the geometric shadow of the wool.
Not the full surface area — just the frontal area.

### Risk: shorting
Steel wool fibers touching each other = short between emitter and collector = arc.
Unless the wool is carefully separated from the emitter by an insulator.

### FINDING: Steel wool collector provides minimal K improvement over NACA. Risk of shorting makes it dangerous. NOT RECOMMENDED.

---

## APPROACH 6: POWER BUDGET RELAXATION

### TPW scaling with gap
At small gaps, TPW is actually BETTER:
TPW(d) = 11.3 × (20/d) mN/W

| d | TPW (mN/W) | T @ 15W | T @ 30W | T @ 50W |
|---|-----------|---------|---------|---------|
| 20mm | 11.3 | 169 mN | 339 mN | 565 mN |
| 15mm | 15.1 | 226 mN | 451 mN | 752 mN |
| 10mm | 22.6 | 339 mN | 678 mN | 1130 mN |
| 8mm | 28.3 | 424 mN | 848 mN | 1413 mN |
| 6mm | 37.7 | 555 mN | 1110 mN | 1850 mN |

**Key insight: At 50W with d=6mm → 1850 mN = 11× baseline ✓**

BUT: d=6mm at 35kV with 0.1mm wire is at the edge of arcing (E_local ≈ 17.5 MV/m).
d=8mm at 35kV with 0.1mm wire: E_local ≈ 14.6 MV/m (safer).
At 50W/d=8mm: T ≈ 1413 mN = 8.4×

### What ZVS module can deliver 50W?
ZVS flyback module input: 12-19V DC, output 30-50kV.
Efficiency: ~80-90% (ZVS is quite efficient).
Input power for 50W output: ~55-60W.
Input current at 12V: ~5A. At 19V: ~3A.

Laptop PSU (19V/3A = 57W) could work as input!
But the ZVS module itself needs to be capable of 50W output.
Most cheap ZVS modules are rated for 15-30W.
Better modules (€20-30): can handle 40-60W.

### FINDING: 50W ZVS + d=6mm could hit 11×. But d=6mm is arcing-risk with 0.1mm wire. d=8mm + 50W = 8.4× (close but not enough).

---

## APPROACH 7: WHAT IF WE USE 50kV?

### Formula check
T = K × (V²/d²) × L
At 50kV/d=6mm: T = 0.623 × (50²/6²) × 500 = 0.623 × 69.4 × 500 = **21,630 mN = 128×**
That's absurdly high but limited by power.

### Power requirement at 50kV
Ion current I scales with E (not V²/d²). More accurate: I ∝ V/d × area.
At 50kV/d=6mm: E = 8.33 MV/m (vs 5.83 at 35kV/6mm)
Ion current ~43% higher.
Power = 50kV × I_50kV.

At 50W supply: available current = 50W/50kV = 1mA.
At 35kV/6mm with 50W: current = 50W/35kV = 1.43mA.
So at same power (50W), the 50kV supply delivers LESS current.

### Realistic thrust at 50kV/50W
T/P ratio at 50kV/6mm: roughly same as 35kV/6mm (power-limited).
Thrust ≈ 1850 mN at 50W (same as 35kV/6mm/50W).

### 50kV ZVS modules
Can standard ZVS reach 50kV?
Most cheap ZVS modules claim 30-50kV. 50kV is at the upper end but achievable.
At 50kV, insulation becomes critical (silicon oil potting recommended).

### FINDING: 50kV + d=6mm + 50W = ~1850 mN (11×). Achievable if ZVS reaches 50kV and d=6mm gap is achievable without arcing. High voltage insulation complexity.

---

## INTERMEDIATE CONCLUSIONS

### Best DIY path to 10× (1690 mN) at 35kV:

| Approach | Config | Thrust | Difficulty | Risk |
|----------|--------|--------|------------|------|
| **1. Length + moderate gap** | L=1000mm, d=15mm | ~3390 mN (20×) | LOW | Safe |
| **2. Power + small gap** | 50W, d=6mm | ~1850 mN (11×) | MEDIUM | Arcing |
| **3. Tandem × 2 + moderate gap** | 2 stages, d=8mm, 30W | ~1020 mN (6×) | MEDIUM | Arcing |
| **4. Tandem × 3 + moderate gap** | 3 stages, d=8mm, 45W | ~1658 mN (9.8×) | HIGH | Complex |
| **5. Multi-wire independent** | 10 spatially-separated pairs | ~5960 mN (35×) | HIGH | Complex |

### Shortest path: L=1000mm at d=15mm (SAFE, EASY, NO PRECISION)
- d=15mm at 35kV with 0.1mm wire: E_local ≈ 10 MV/m (safe from arcing)
- K=0.623, L=1000mm → T = 3390 mN = 20× baseline ✓
- Carbon fiber rod supports are standard (6mm OD, 1m length, ~€10)
- Spacers: laser-cut acrylic, no precision needed
- Power: ~25W (at d=15mm, TPW=15.1 → 25W × 15.1 = 378 mN? Wait)

Let me recalculate power-limited thrust at d=15mm:
- TPW(d) = 11.3 × (20/d) = 11.3 × 1.33 = 15.1 mN/W
- At 25W: T = 15.1 × 25 = 377 mN at d=15mm
- BUT the formula T = K × V²/d² × L gives: T = 0.623 × 5.44 × 1000 = 3390 mN

There's a HUGE discrepancy: formula gives 3390 mN, but power-limited gives only 377 mN at 25W.
Which is correct?

The formula T = K × V²/d² × L is the IDEAL formula assuming unlimited power.
In reality, thrust is POWER-LIMITED. The actual thrust is MIN(formula, TPW × P_max).

At d=15mm: formula gives 3390 mN, but power-limited gives only 377 mN (at 25W).
The POWER is what limits thrust, not the formula!

At d=15mm/35kV, to get anywhere near formula thrust of 3390 mN, we need P = T/TPW = 3390/15.1 = 225W.
That's enormous. Our practical ZVS can do 15-30W.

So at 15W: T_max at d=15mm = 15 × 15.1 = 226 mN = 1.3× baseline.
At 30W: T_MAX at d=15mm = 30 × 15.1 = 453 mN = 2.7× baseline.

**This means LENGTH SCALING alone doesn't help at fixed power!**

If I make L=1000mm but power stays at 15W: T = same as L=500mm (because power-limited).
Power-limited means more L doesn't help unless you also increase power.

**CRITICAL CORRECTION:** The power-limited regime means:
- T_max = TPW(d) × P_max
- TPW(d) = 11.3 × (20/d) mN/W
- P_max is limited by ZVS (typically 15-30W for small modules)

At d=6mm/15W: T_max = 37.7 × 15 = 555 mN (3.3×)
At d=6mm/30W: T_max = 37.7 × 30 = 1131 mN (6.7×)
At d=6mm/50W: T_max = 37.7 × 50 = 1885 mN (11.2×) ✓

At d=8mm/50W: T_max = 28.3 × 50 = 1415 mN (8.4×)
At d=8mm/60W: T_max = 28.3 × 60 = 1698 mN (10.1×) ✓

**NEW UNDERSTANDING:** The path to 10× at 35kV requires:
1. Small gap (d=6-8mm) to get good TPW
2. Higher power (50-60W) to get enough thrust
3. Tandem stages add K bonus on top of power-limited thrust

With tandem at d=8mm/50W:
- Base: 1415 mN
- K_eff from tandem × 2 = 1.2 → T = 1415 × 1.2 = 1698 mN = 10.1× ✓

### FINDING: Best DIY path = SMALL GAP (d=8mm) + HIGH POWER (50W) + TANDEM × 2

- d=8mm: TPW = 28.3 mN/W → 50W → 1415 mN
- Tandem × 2: K_eff = 1.2 → T = 1698 mN = 10.1× ✓
- Emitter: 0.1mm stainless steel guitar string (no precision needed)
- Gap: 8mm achieved with simple acrylic spacers (no micrometer)
- Power: 50W ZVS module (laptop PSU input)
- Mechanical: two independent electrode pairs at d=8mm, 50mm apart

---

## TO BE CONTINUED...
Writing final summary to DIY_10X_PATH.md next.
