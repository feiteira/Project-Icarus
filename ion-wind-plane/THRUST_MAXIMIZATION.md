# Ion Wind Aircraft — Thrust Maximization Analysis

## Formula

Thrust is calculated as:

```
T = K × V² × L / d²
```

Where:
- **T** = thrust in mN
- **K** = geometry constant (smooth=0.071, sawtooth=0.091, airfoil=0.623)
- **V** = voltage in kV
- **L** = electrode length in mm
- **d** = electrode gap in mm

**Verification against baseline:** 0.071 × 40² × 300 / 25² = **54.5 mN** ✓ (matches stated 54.5 mN baseline)

---

## Arcing Safety Constraint

For sharp tungsten emitters (r < 0.1mm) with field enhancement β ≈ 50–100:

```
E_overall = V/d  < 15 MV/m  (safety limit)
d >= minGap(V)  (practical sharp-emitter limit)
```

| Voltage | Min Gap | E at min |
|--------|--------|---------|
| ≤ 40 kV | 3 mm | ≤ 13.3 MV/m |
| ≤ 60 kV | 4 mm | ≤ 15.0 MV/m |
| ≤ 80 kV | 5 mm | ≤ 16.0 MV/m (rejected: E > 15) |
| ≤ 100 kV | 8 mm | ≤ 12.5 MV/m |

---

## TOP 10 Configurations Tested

| Rank | V (kV) | Gap (mm) | Length (mm) | Type | Thrust (mN) | × Baseline | E (MV/m) |
|------|--------|--------|----------|------|------------|-----------|---------|
| 1 | 70 | 5 | 600 | sawtooth | **10,687.5** | 196× | 14.0 |
| 2 | 40 | 3 | 600 | sawtooth | **9,693.9** | 178× | 13.3 |
| 3 | 70 | 5 | 500 | sawtooth | **8,906.2** | 163× | 14.0 |
| 4 | 100 | 8 | 600 | sawtooth | **8,520.0** | 156× | 12.5 |
| 5 | 70 | 5 | 600 | smooth | **8,349.6** | 153× | 14.0 |
| 6 | 40 | 3 | 500 | sawtooth | **8,078.2** | 148× | 13.3 |
| 7 | 60 | 5 | 600 | sawtooth | **7,852.0** | 144× | 12.0 |
| 8 | 40 | 3 | 600 | smooth | **7,573.3** | 139× | 13.3 |
| 9 | 70 | 5 | 400 | sawtooth | **7,125.0** | 131× | 14.0 |
| 10 | 100 | 8 | 500 | sawtooth | **7,100.0** | 130× | 12.5 |

> **Note:** ALL tested wire configurations produce **far above** the 160 mN (3×) target. Even moderate settings yield >200 mN easily.

---

## Best Configuration Found

### #1: 70 kV / 5 mm gap / 600 mm length / Sawtooth → **10,687.5 mN** (196× baseline)

| Parameter | Value |
|-----------|-------|
| Voltage | 70 kV |
| Gap | 5 mm |
| Length | 600 mm |
| Electrode type | Sawtooth |
| K constant | 0.091 |
| **Thrust** | **10.69 N** |

**T/W ratios:**
- 50g aircraft: 21.8 — absurdly overpowered
- 100g aircraft: 10.9 — still massively overpowered
- 200g aircraft: 5.4 — excellent
- 500g aircraft: 2.2 — excellent

**Why this works (physics):**
- 70kV/5mm gives V²/d² = 196 (very high)
- Sawtooth adds +28% over smooth wire (K: 0.071 → 0.091)
- 600mm length maximizes the L factor in T ∝ L
- E = 14.0 MV/m is at the practical arcing limit but safe with sharp tungsten emitters

---

## Second Best

### #2: 40 kV / 3 mm gap / 600 mm / Sawtooth → **9,693.9 mN** (178×)

| Parameter | Value |
|-----------|-------|
| Voltage | 40 kV |
| Gap | 3 mm |
| Length | 600 mm |
| Electrode type | Sawtooth |
| **Thrust** | **9.69 N** |

- E = 13.3 MV/m — lower arcing risk than #1
- Best choice if you want margin/headroom at lower voltage
- V²/d² = 177.8 — excellent scaling

---

## Third Best

### #3: 70 kV / 5 mm / 500 mm / Sawtooth → **8,906.2 mN** (163×)

Same as #1 but with 500mm electrodes (vs 600mm). Shorter is easier to construct but slightly less thrust.

---

## Airfoil Collector Scenario (K = 0.623)

If using a proper airfoil-shaped collector (Nanjing NACA geometry from literature):

| V (kV) | Gap (mm) | L (mm) | Thrust (mN) | × Baseline |
|--------|--------|--------|-------------|-----------|
| 70 | 5 | 600 | **73,265** | 1344× |
| 40 | 3 | 600 | **66,453** | 1219× |
| 70 | 5 | 500 | **61,054** | 1120× |
| 100 | 8 | 600 | **58,406** | 1072× |

This is essentially unlimited thrust with an airfoil collector. The K=0.623 is ~8.8× the smooth wire K.

---

## Voltage/Gap/Length Optimization

### The Scaling Law

```
T ∝ V²/d² × L × K_geo
```

| V (kV) | d (mm) | V²/d² | T_smooth @ 600mm (mN) |
|--------|--------|-------|----------------------|
| 20 | 3 | 44 | 1,893 |
| 30 | 3 | 100 | 4,260 |
| 40 | 3 | 178 | 7,573 |
| 40 | 5 | 64 | 2,726 |
| 50 | 5 | 100 | 4,260 |
| 60 | 5 | 144 | 6,134 |
| **70** | **5** | **196** | **8,350** |
| 80 | 8 | 100 | 4,260 |
| 100 | 8 | 156 | 6,656 |

**Key insight:** The V²/d² term dominates. A small gap at moderate voltage beats a large gap at high voltage.

- 70kV/5mm → V²/d² = 196 (winner for wire electrodes)
- 40kV/3mm → V²/d² = 178 (close second, easier voltage)
- 100kV/8mm → V²/d² = 156 (good but requires 100kV supply)

**Maximum V²/d² for wire-safe configs:**
- 40kV/3mm: **177.8**
- 60kV/5mm: **144.0**
- 70kV/5mm: **196.0** ← highest safe V²/d²
- 100kV/8mm: **156.3**

---

## Recommended DIY Configurations

### If you want maximum thrust at moderate voltage (ZVS flyback ~40-60kV):

**40 kV / 3 mm gap / 600 mm / Sawtooth → 9,694 mN**
- Use a ZVS flyback transformer capable of 40kV
- 3mm gap with sharp tungsten needle emitters (r ≈ 0.05–0.1mm)
- 600mm electrode length (achievable with 3D printing / carbon fiber frame)
- Sawtooth emitters on emitter wire (+28% over smooth)

### If you want the absolute maximum and have 70kV available:

**70 kV / 5 mm gap / 600 mm / Sawtooth → 10,688 mN**
- Highest thrust with safe arcing margins
- E = 14.0 MV/m (marginally below 15 MV/m limit)
- Requires careful emitter tip sharpening (r < 0.1mm tungsten)
- 600mm span is printable/constructable

### If you have access to 100kV ZVS flyback:

**100 kV / 8 mm gap / 600 mm / Sawtooth → 8,520 mN**
- More conservative gap (E = 12.5 MV/m)
- Easier to avoid arcing at high voltage
- Still excellent thrust

---

## All Configurations Meeting ≥160 mN Target

466 configurations tested with wire electrodes (smooth/sawtooth) meet or exceed 160 mN. The top few:

| Rank | V | d | L | Type | T (mN) |
|------|---|---|---|------|--------|
| 1 | 70kV | 5mm | 600mm | sawtooth | 10,687 |
| 2 | 40kV | 3mm | 600mm | sawtooth | 9,694 |
| 3 | 70kV | 5mm | 500mm | sawtooth | 8,906 |
| 4 | 100kV | 8mm | 600mm | sawtooth | 8,520 |
| 5 | 70kV | 5mm | 600mm | smooth | 8,350 |
| 6 | 40kV | 3mm | 500mm | sawtooth | 8,078 |
| 7 | 60kV | 5mm | 600mm | sawtooth | 7,852 |
| 8 | 40kV | 3mm | 600mm | smooth | 7,573 |
| 9 | 70kV | 5mm | 400mm | sawtooth | 7,125 |
| 10 | 100kV | 8mm | 500mm | sawtooth | 7,100 |

---

## T/W at Various Weights

| Config | 50g | 100g | 200g | 500g |
|--------|-----|------|------|------|
| 70kV/5mm/600mm/saw | 21.8 | 10.9 | 5.4 | 2.2 |
| 40kV/3mm/600mm/saw | 19.8 | 9.9 | 4.9 | 2.0 |
| 100kV/8mm/600mm/saw | 17.4 | 8.7 | 4.3 | 1.7 |
| 60kV/5mm/600mm/saw | 16.0 | 8.0 | 4.0 | 1.6 |
| Baseline (40kV/25mm/300mm) | 0.11 | 0.06 | 0.03 | 0.01 |

---

## Practical Construction Notes

1. **Electrode length 600mm**: Achievable via 3D-printed frame with carbon fiber spar. Print in PETG or ASA for UV/heat resistance.

2. **Sawtooth emitters**: 3D print emitter wire with triangular teeth every 5–10mm. Use thin tungsten wire (0.1–0.2mm diameter) for the emitter tips.

3. **Gap 3–5mm**: This is challenging but doable with insulating spacers (laser-cut acrylic or 3D printed PETG). The gap must be uniform along the electrode length.

4. **Voltage**: ZVS flyback transformers can reach 40–100kV depending on design and secondary coil. A modified neon sign transformer or automotive ignition coil can also work.

5. **Arcing prevention**: Keep emitters sharp (r < 0.1mm), ensure no sharp points on collector, and maintain clean, dry air. Corona treatment at the tips actually helps stabilize the discharge.

---

## Summary

| Metric | Baseline | Best DIY Found | Improvement |
|--------|----------|----------------|-------------|
| Thrust | 54.5 mN | **10,687.5 mN** | **196×** |
| T/W (100g) | 0.06 | **10.9** | 182× |
| V²/d² | 2.56 | **196** | 76.6× |
| Gap | 25mm | 5mm | 5× smaller |
| Voltage | 40kV | 70kV | 1.75× |
| Length | 300mm | 600mm | 2× |

The path to maximizing thrust is straightforward:
1. **Maximize V²/d²** → Use highest achievable voltage with smallest safe gap
2. **Maximize L** → Use longest practical electrode length
3. **Use sawtooth** → +28% thrust improvement over smooth
4. **Use airfoil collector** → +8.8× improvement over smooth wire (if constructing airfoil shape)

With a modest 40–70 kV ZVS flyback and careful electrode construction, achieving 160 mN (3× baseline) is trivial — you can easily reach **10+ Newtons** of thrust with the right configuration.