# Academic Paper Research Notes — Project Icarus
# Date: 2026-04-23

## PDF 1: WPI MQP (2024) — "Design, Analysis and Testing of Ionic Wind Propulsion System"

### Key Data
- Thrust density: up to **321.74 mN/m at 25 kV**
- Electrode length: 250mm
- Emitter radius: **0.125mm** (very thin!)
- Collector radius: varied (0.225in, 0.4in, 0.6in = 5.7mm, 10.2mm, 15.2mm)
- Electrode gap: **20-40mm** (tested range)
- Applied voltage: **10-30 kV**
- Ion mobility: 1.4e-4 m²/(V·s)
- Max thrust: **5.0 grams at 25 kV** (Test #3)
- Thrust ∝ U² (quadratic with voltage)
- Thrust ∝ d⁻² (decreases with electrode gap)

### Findings
1. Larger collector diameter → more thrust
2. Smaller gap → higher electric field (without arcing)
3. More emitter-collector pairs → more ionization zones
4. Staggering electrodes → improves ion drift efficiency

### Power Circuit
- DC → Boost Converter → Flyback Transformer → ZVS Driver → Voltage Multiplier → HV DC
- 4V to 40V DC input
- Flyback driver with ZVS (Zero Voltage Switching)

---

## PDF 2: Nature Scientific Reports (2025) — "Sawtooth multi-ring electrodes for ionic wind propulsion"
### Nanjing University of Aeronautics and Astronautics

### Key Achievement
- **164 mN/m at 40 kV** with 60mm gap (28.2% enhancement vs single ring)
- With NACA 0018 airfoil collector: **200 mN/m at 34 kV**

### Optimal Geometry (30° sawtooth angle)
- Emitter ring diameter: **80mm**
- Collector ring diameters: **60mm, 80mm, 100mm**
- Ring width (k): **3mm** (optimal)
- Ring spacing (b): **7mm** (optimal)
- Electrode gap (d): **60mm**
- Number of teeth: **50** (optimal — fewer is better)
- Tooth angle: **30°** (best — 60° gives only 144 mN/m)

### Key Insights
1. **30° angle** produces highest thrust (172 mN/m vs 144 mN/m for 60°)
2. **Fewer teeth** = higher thrust (less space charge accumulation, less recombination)
3. **NACA 0018 airfoil collector** outperforms ring collector (200 vs 156 mN/m)
4. **Smaller spacing** b = higher thrust (larger intermediate rings = more ion generation)
5. **Smaller width** k = higher thrust (k=2mm: 164 mN/m vs k=5mm: 134 mN/m)
6. Thrust ∝ U², decreases ∝ d⁻²

### Efficiency
- Thrust-to-power ratio **decreases** as U⁻¹ at high voltages
- Power ∝ U³ while thrust ∝ U²
- Mitigation: limit current, optimize for lower operating voltages

---

## PDF 3: Transilvania University (2025) — "Design and Experimental Evaluation of an Ion Wing Prototype"

### Wing Dimensions
- Length: **24-25 cm**
- Width: **18-20 cm**
- Grid-based system (modular for directional control)

### First Iteration: 3×3 Grid
- Grid unit: 119mm × 40mm × 1mm
- Slots: 3 per unit (1mm wide, 15mm long)
- **Critical gap: 0.8-0.9mm** between aluminum foil edges (essential for ionization)
- Materials: cardboard 280g/m² + aluminum foil + PVA adhesive

### Second Iteration: 6×6 Grid
- PLA 3D printed
- Maintains optimal spacing to prevent arcing

### Power
- 18650 Li-ion cell (3.7V nominal)
- HV generator module: **1000 kV output** (from 3-6V input)

---

## Comparison: Our Current Design vs Papers

| Parameter | Our Design | Paper Optimal |
|-----------|-----------|---------------|
| Gap | 11mm | 20-40mm (PDF1), 60mm (PDF2) |
| Collector | Smooth tube 50mm OD | 60-100mm rings (PDF2) |
| Emitter | Razor blade ring | Sawtooth 30° (PDF2) |
| Voltage | 20-40kV | 25-40kV |
| Electrode length | ~80mm | 250mm (PDF1) |

---

## Recommended Improvements

### Immediate (before printing)
1. **Increase gap** from 11mm to **20-25mm** — our gap is too small, risk of arcing
2. **Increase collector diameter** to 60-80mm (from 50mm)
3. **Add collector rings** (multi-ring design like PDF2)
4. **Consider NACA 0018 airfoil** as collector shape
5. **Add more electrode pairs** — staggered arrangement
6. **Use thinner emitter wire** — 0.125mm (PDF1) vs our 0.5mm

### Medium-term
1. **Implement flyback + ZVS + voltage multiplier** circuit (from PDF1)
2. **Design modular grid system** (like PDF3's 3×3 / 6×6 approach)
3. **Add directional control** via selective voltage application to grid sections

### Scale Calculation
- Our wing: ~300mm span × 60mm chord = 0.018m²
- At 164 mN/m (PDF2): if electrode length = 80mm per side
- Total electrode length = 2 × 80mm = 0.16m
- Estimated thrust = 164 × 0.16 = **~26 mN = 2.6 grams**
- Aircraft weight target: <100g (need lighter than PDF3's cardboard approach)
- **Verdict: feasible but margins are tight — thrust stand critical**

---

## PDF 4: Solar HAPS Airfoil Optimization (2021)

**Title:** Optimal Airfoil Design and Wing Analysis for Solar-Powered High-Altitude Platform Station
**Authors:** Hasan et al., University of Belgrade
**Context:** Aircraft for 17-25 km altitude, 150 kg, 25 m/s cruise

### Key Data (NOT directly ion wind, but useful for wing design)

**Best airfoil (Airfoil-1) — optimized for glide ratio:**
- Relative thickness: **12.36%** at 34.5% chord
- Camber: **4.87%** at 47% chord
- Max glide ratio (2D): **~85**
- Max glide ratio (3D wing): **~32**
- Max CL: 1.45 (2D)

**Wing geometry:**
- Aspect ratio: ~11.8
- Taper ratio: 0.6
- Dihedral: 10.44°

**Solar system:**
- Panel coverage: 75% of suction surface
- Panel mass: 9 kg (for ~35m²)
- Battery: ~28-37% of total mass

### Relevance to Project Icarus
- **NOT directly applicable** — this is for 150kg aircraft at 20km altitude
- **However useful for:**
  1. Airfoil selection methodology (CST parameterization)
  2. Low-speed airfoil data (CLmax, glide ratios)
  3. Wing construction approach (untorsion, dihedral)
  
**Our constraint:** We have ~2.6g thrust vs aircraft weight ~100g. We need MUCH higher glide ratio than conventional aircraft because thrust is marginal.

**Recommendation:** For ion wind at small scale, focus on:
- Ultra-lightweight construction (film, carbon fiber rods)
- Very large wing area for maximum lift
- Minimum possible weight above all else
