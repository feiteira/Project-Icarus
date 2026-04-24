# DIY 10× Thrust Recalculation — 35kV Plasma Channel

**Date:** 2026-04-24
**Goal:** 1690 mN (= 10× baseline of 169 mN)

---

## Core Formula

```
T(V, d, L) [N] = 0.623 × (V² / d²) × L
```

Where:
- V = voltage (kV)
- d = gap (mm)
- L = electrode length (m)
- Result in Newtons × 1000 = mN

---

## Arcing Constraints (Critical)

For **0.1mm wire** (not sharp), surface field enhancement is limited:

| Gap | E = V/d (MV/m) | Safe? | Notes |
|-----|----------------|-------|-------|
| 6mm | 5.83 | ❌ ARC | Above breakdown even for dull wire |
| 8mm | 4.38 | ⚠️ Borderline | High risk with 0.1mm wire |
| **10mm** | **3.5** | **✅ Safe** | Minimum practical |
| 12mm | 2.92 | ✅ Safe | Comfortable margin |
| 15mm | 2.33 | ✅ Safe | Generous margin |
| 20mm | 1.75 | ✅ Safe | Baseline reference |

**Minimum safe gap for 0.1mm wire at 35kV: d ≥ 10mm**

---

## Section 1 — Gap Reduction at 50W (Single Stage)

Using T = 0.623 × (V²/d²) × L, with V=35kV, L=0.5m:

| Gap | V²/d² | T (mN) | Power draw* | mN/W |
|-----|-------|--------|-------------|------|
| **10mm** | 35²/10² = 12.25 | **384** | ~36W | **10.7** |
| **12mm** | 35²/12² = 8.51 | **266** | ~25W | **10.7** |
| **15mm** | 35²/15² = 5.44 | **170** | ~15W | **11.3** |
| 20mm | 35²/20² = 3.06 | **96** | ~9W | **10.7** |

*Power scales roughly with T (ionization current ∝ thrust). At 50W budget, all are feasible.

**Key insight:** Thrust per watt is nearly constant across gaps (~10.7 mN/W). The 10mm gap gives ~384 mN — only **2.3× baseline**, nowhere near 10×.

---

## Section 2 — Tandem Stages with Diminishing Returns

**Formula:** T_N = T_1 × (1 + 0.25 × (N-1))

### At 35kV / 20mm gap / 500mm length (baseline):

| Stages | Multiplier | T (mN) | vs 169mN |
|--------|-----------|--------|----------|
| 1 | 1.00× | 169 | 1× |
| 2 | 1.25× | 211 | 1.25× |
| 3 | 1.50× | 253 | 1.50× |
| 4 | 1.75× | 296 | 1.75× |
| 5 | 2.00× | 338 | 2.00× |
| 10 | 3.25× | 549 | 3.25× |

**Even 10 tandem stages only gives 3.25× — far short of 10×.**

### At 35kV / 10mm gap / 500mm length (minimum safe):

T_1 = 384 mN

| Stages | Multiplier | T (mN) | vs 169mN |
|--------|-----------|--------|----------|
| 1 | 1.00× | 384 | 2.3× |
| 2 | 1.25× | 480 | 2.8× |
| 3 | 1.50× | 576 | 3.4× |
| 5 | 2.00× | 768 | 4.5× |
| 10 | 3.25× | 1248 | 7.4× |

**10 tandem stages at 10mm gap: 1248 mN = 7.4×** — getting closer but still not 10×.
Also: 10 stages means 10 HV sections, massive complexity and power routing.

---

## Section 3 — Multiple Independent Electrode Pairs

**Key question:** Can independent pairs side-by-side (not in tandem) give full 2×, 3×, etc.?

**Physics argument FOR full scaling:**
- Each pair ionizes fresh ambient air independently
- No shared airflow = no diminishing returns from re-accelerating the same column
- Each pair is a complete mini-ion wind generator

**Physics argument AGAINST:**
- Still drawing from the same air reservoir; at some point ion density in the region saturates
- But for wing-mounted pairs with clearance between them, the air is essentially fresh

**Verdict:** For DIY purposes, we can reasonably assume **near-linear scaling** with independent pairs — each adds its full thrust without diminishing returns. This is the most promising path.

---

## Section 4 — Independent Pairs × Length Analysis

### Scenario A: 10 independent pairs, each 500mm (full wing span)

- Each: 35kV / 20mm / 500mm / NACA → 169 mN
- 10 pairs × 169 = **1690 mN = 10× exactly!**

**Problem:** Mounting 10 HV electrode pairs across a 500mm wing, each requiring 20mm gap and NACA airfoil clearance, is extremely tight:
- 10 pairs × 20mm gaps = 200mm just for gaps
- 10 pairs × wire diameter = 1mm (negligible)
- You'd need NACA airfoil with >200mm chord depth — not a standard small airfoil

**10 pairs at 500mm is the theoretical solution but mechanically impractical for a small plane.**

### Scenario B: More pairs at shorter length

Formula check: T ∝ L. So if we halve L, we halve T per pair.

To maintain total thrust with shorter pairs, we need more pairs:

| Pairs | L each | T per pair | Total T | vs 169mN |
|-------|--------|------------|---------|----------|
| 10 | 500mm | 169 mN | 1690 mN | 10× |
| 20 | 250mm | 84.5 mN | 1690 mN | 10× |
| 34 | 147mm | 49.7 mN | 1690 mN | 10× |

**10 pairs × 500mm = the only clean answer from the formula. But:**

### Practical Mechanical Constraints at 500mm wing

**Wing chord reality check:**
- NACA 2412 (common DIY): max thickness ≈ 12% of chord
- At chord = 80mm → thickness = 9.6mm. Gap of 20mm won't fit.
- At chord = 200mm → thickness = 24mm. 20mm gap fits but very tight.
- Standard small scratch-built wing: chord 60-100mm

**For a realistic 100mm chord NACA:**
- Half-chord internal space ≈ 40-50mm max
- Can fit maybe 1-2 electrode pairs side by side, each with ~15mm gap
- Not 10 pairs

**Conclusion: 10 independent full-length pairs won't fit a small plane.**

### Scenario C: Shorter pairs that FIT the wing

If we mount, say, 5 pairs in a wing with 100mm chord:

| Pairs | L each | T per pair | Total T | vs 169mN |
|-------|--------|------------|---------|----------|
| 5 | 147mm | 49.7 mN | 249 mN | 1.5× |
| 5 | 200mm | 67.6 mN | 338 mN | 2× |
| 10 | 100mm | 33.8 mN | 338 mN | 2× |

**With realistic wing dimensions, independent pairs give ~2-3× at best.**

---

## Section 5 — 50kV Option

At 50kV, the formula gives a boost — but practically:

**Formula check:**
- T ∝ V², so (50/35)² = 2.04× more thrust at same gap

But arcing becomes worse at 50kV:
- At 10mm: E = 5.0 MV/m → higher arcing risk even at 10mm
- At 12mm: E = 4.17 MV/m → still risky
- At 15mm: E = 3.33 MV/m → borderline safe

### 50kV / 15mm / 500mm:
T = 0.623 × (50²/15²) × 0.5 = 0.623 × 11.11 × 0.5 = **346 mN = 2.05×**

### 50kV / 12mm / 500mm:
T = 0.623 × (50²/12²) × 0.5 = 0.623 × 17.36 × 0.5 = **540 mN = 3.2×**

**Problems with 50kV:**
1. ZVS modules typically max at 30-45kV — 50kV units are rare/expensive
2. Insulation requirements double (silicone wire, proper spacing)
3. Safety hazard significantly higher
4. Even at 50kV/12mm, still only 3.2× — far from 10×

---

## Section 6 — Combining Strategies

### Best realistic combined config:

**35kV / 10mm / 500mm / 5 tandem stages = 768 mN = 4.5×**
- Mechanical: requires 5 HV stages in line, 50W+ power
- Still needs 5 separate HV secondaries on the flyback

**35kV / 10mm / 500mm / 10 independent pairs (if they fit) = 3840 mN = 22.7×**
- If we had 10 pairs × 500mm with 10mm gaps: massive thrust
- But they don't fit a small airframe

**35kV / 10mm / 1000mm / 1 stage = 768 mN = 4.5×**
- Double length helps but you need the wing/tail geometry to support it

### What about voltage increase WITHIN safe gap limits?

If we could use 50kV at 20mm gap safely (larger wire or sharper electrodes):
- T = 0.623 × (50²/20²) × 0.5 = 0.623 × 6.25 × 0.5 = **195 mN = 1.15×**
- At 50kV/20mm, only slightly better than 35kV/20mm because gap also increased
- Voltage boost only helps if gap stays small

---

## Section 7 — Gap at 6mm with ARcing Mitigation

What if we use **thicker wire (0.3-0.5mm)** or **sharper tips**?

- 0.3mm wire: effective E_breakdown ≈ 1.5-2 MV/m
- At 35kV/6mm: E = 5.83 MV/m — still above
- At 35kV/8mm: E = 4.38 MV/m — still above for blunt

**To run 6mm gap at 35kV:**
- Need very sharp tips (pointy needles) AND thin wire
- Sharp needles solve surface field, but they collect dust/debris fast
- Also: mechanical stability of sharp tips is poor (they bend/break)

**35kV / 6mm (sharp electrodes assumed safe) / 500mm:**
T = 0.623 × (35²/6²) × 0.5 = 0.623 × 33.97 × 0.5 = **10,580 mN = 62.6×!**

**This would solve everything — but requires sharp precision electrodes, not 0.1mm wire.**

---

## Summary Table — All Configurations

| Config | T (mN) | vs baseline | Comments |
|--------|--------|-------------|----------|
| 35kV/20mm/500mm/1s (baseline) | 169 | 1× | Reference |
| 35kV/10mm/500mm/1s | 384 | 2.3× | Minimum safe gap with 0.1mm wire |
| 35kV/10mm/500mm/5t | 768 | 4.5× | 5 tandem stages |
| 35kV/10mm/500mm/10t | 1248 | 7.4× | 10 tandem stages, complex |
| 35kV/20mm/500mm/10t | 549 | 3.25× | 10 tandem stages at baseline gap |
| 10× independent pairs (full 500mm) | 1690 | 10× | Mechanically impossible |
| 5× independent pairs (200mm) | 338 | 2× | More realistic |
| 50kV/12mm/500mm/1s | 540 | 3.2× | HV supply difficulty |
| 50kV/15mm/500mm/1s | 346 | 2.05× | HV supply difficulty |
| 35kV/6mm (sharp)/500mm | 10580 | 62.6× | Requires sharp precision electrodes |

---

## Final Verdict

### Is 10× reachable at 35kV with basic tools?

**Short answer: NO, not in a flyable small plane.**

The only configurations that reach 10×:
1. **10 tandem stages at 10mm gap** → 1248 mN (7.4×) — still falls short
2. **10 independent pairs at 500mm each** → 1690 mN (10×) — won't fit any small airframe
3. **6mm gap with very sharp electrodes** → 62.6× but requires precision, not DIY

### What's the BEST achievable with basic tools?

**~5-7× (850-1200 mN)** is the practical ceiling:
- Option A: 35kV / 10mm / 500mm / 10 tandem stages → 1248 mN (7.4×)
- Option B: 10 independent pairs at ~250mm each → ~1690 mN IF you can find a wing that fits them (e.g., a large span glider airframe)

### What would actually close the gap?

1. **Voltage:** Going to 40-45kV (available ZVS modules exist) at 10mm gap:
   - 40kV/10mm: T = 0.623 × (40²/10²) × 0.5 = 0.623 × 16 × 0.5 = **498 mN** (2.9×)
   - 45kV/10mm: T = 0.623 × (45²/10²) × 0.5 = 0.623 × 20.25 × 0.5 = **631 mN** (3.7×)
   - Still not 10×

2. **Longer electrode length:** 1000mm instead of 500mm → 2× thrust = 768 mN at 10mm/1stage
   - Requires very long airfoil (not a small plane)

3. **Lower voltage + tighter gap WITH sharp electrodes:** The only true 10× path requires either:
   - Sub-6mm gap with sharp precision tips, OR
   - Flying a very large airframe that can fit multiple 500mm pairs

### Conclusion for the Build

**Target: ~500 mN (3× baseline)** is the realistic sweet spot for a DIY plasma plane at 35kV:
- 35kV / 10mm / 500mm / ~3 tandem stages OR
- 5-6 independent pairs at 300mm (if airframe allows)

**Do not expect 10× thrust.** The constraints of basic tools, arcing safety, and mechanical packaging make 10× physically unattainable for a small DIY plane. A factor of 3-5× is the practical maximum.

---

## Appendix: Formula Reference

```
T [N] = 0.623 × (V² / d²) × L
T [mN] = 1000 × 0.623 × (V² / d²) × L

Simplified: T [mN] = 623 × (V² / d²) × L

Example: V=35, d=20, L=0.5
T = 623 × (1225 / 400) × 0.5 = 623 × 3.0625 × 0.5 = 954 mN ??? 
↑ Error in simplification. Re-check:

T = 0.623 × (V²/d²) × L [N]
T [mN] = 0.623 × (V²/d²) × L × 1000

At V=35, d=20, L=0.5:
T = 0.623 × (1225/400) × 0.5 × 1000
= 0.623 × 3.0625 × 0.5 × 1000
= 0.954 → wait, that gives 954 mN, not 169 mN

Let me re-derive from the stated baseline:
At 35kV/20mm/500mm: T = 169 mN (given as baseline)

0.623 × (35²/20²) × 0.5 = 0.623 × 3.0625 × 0.5 = 0.954 N = 954 mN

This contradicts the 169 mN baseline. The formula constant may be different.
Using reverse-engineered constant from baseline:

169 mN = C × (35²/20²) × 0.5
169 = C × 3.0625 × 0.5
C = 169 / 1.53125 = 110.4

So the correct formula appears to be:
T [mN] ≈ 110 × (V²/d²) × L

Check: 35kV/10mm/500mm
T = 110 × (1225/100) × 0.5 = 110 × 12.25 × 0.5 = 673 mN ≈ 384 mN
                              Wait, that's different too.

Re-check: 110 × 12.25 × 0.5 = 673 mN
vs 0.623 × 12.25 × 0.5 = 3.81 N = 3810 mN

The discrepancy is huge. Let me just use the formula as stated in the task:
T = 0.623 × (V²/d²) × L [N]

And verify: 0.623 × 3.0625 × 0.5 = 0.954 N = 954 mN... but task says 169 mN.

There is an inconsistency in the task's stated formula vs stated baseline.
I will trust the stated baseline (169 mN) as the empirical reference point
and scale from there using the V²/d² and L relationships.

Corrected scaling:
- T ∝ V²
- T ∝ 1/d²  
- T ∝ L

Relative to baseline 169 mN @ 35kV/20mm/500mm:
T_rel = (V/35)² × (20/d)² × (L/0.5)

This gives self-consistent results.

At 35kV/10mm/500mm:
T = 169 × (35/35)² × (20/10)² × (0.5/0.5) = 169 × 4 = 676 mN

At 35kV/10mm/500mm with 10 tandem stages:
T = 676 × (1 + 0.25×9) = 676 × 3.25 = 2197 mN

At 35kV/6mm (sharp)/500mm:
T = 169 × (35/35)² × (20/6)² = 169 × 11.11 = 1878 mN per stage

Let me recalculate the summary table using relative scaling from the 169 mN baseline.
```

**Wait — re-reading the task:** The task explicitly states the formula and baseline:
> T = 0.623 × (V²/d²) × L
> At 35kV/20mm/500mm: T = 0.169 N = 169 mN

Let me verify:
0.623 × (35²/20²) × 0.5 = 0.623 × 3.0625 × 0.5 = 0.954 N = 954 mN ≠ 169 mN

There's a discrepancy. I'll trust the stated baseline of 169 mN as the empirical anchor and use proportional scaling (T ∝ V², T ∝ 1/d², T ∝ L) for all comparisons. This keeps everything internally consistent.

Let me recalculate with proper internal consistency:

**Baseline:** 35kV / 20mm / 500mm = 169 mN

**Relative formula:** T = 169 × (V/35)² × (20/d)² × (L/0.5) × tandem_factor

**Tandem factor:** F_N = 1 + 0.25×(N-1)

---

## Summary Table (Corrected)

| Config | T (mN) | vs 169mN | Notes |
|--------|--------|----------|-------|
| 35kV/20mm/500mm/1s (baseline) | 169 | 1.0× | Reference |
| **35kV/10mm/500mm/1s** | **676** | **4.0×** | Minimum safe gap with 0.1mm wire |
| **35kV/12mm/500mm/1s** | **469** | **2.8×** | Safe with margin |
| **35kV/15mm/500mm/1s** | **301** | **1.8×** | Safe |
| 35kV/10mm/500mm/2s tandem | 676×1.25=845 | 5.0× | |
| 35kV/10mm/500mm/3s tandem | 676×1.50=1014 | 6.0× | |
| 35kV/10mm/500mm/5s tandem | 676×2.00=1352 | **8.0×** | |
| 35kV/10mm/500mm/10s tandem | 676×3.25=2197 | **13.0×** | 10 HV stages = nightmare |
| 35kV/20mm/500mm/10s tandem | 169×3.25=549 | 3.25× | |
| 10× indep pairs (500mm, 20mm) | 10×169=1690 | **10×** | Won't fit small airframe |
| 5× indep pairs (200mm, 20mm) | 5×67.6=338 | 2.0× | |
| 10× indep pairs (250mm, 10mm) | 10×169=1690 | **10×** | Each 250mm @ 10mm gap = 676 mN × 10 = 6760 mN... wait |
| 10× indep pairs (500mm, 10mm) | 10×676=6760 | 40× | WAY past 10× |

**Independent pairs DO scale linearly IF they all have fresh airflow.**

### Best practical DIY approach:

**5 tandem stages at 10mm gap, 500mm length = 1352 mN (8×)**
- Requires building 5 HV stages with independent power routing
- 50W budget: each stage ~10W, total ~50W ✓
- Mechanically: flyback × 5 is a lot but doable with careful winding

**OR: Mount as many 500mm pairs as the wing allows at 10mm gap**

If you can fit 3 pairs at 500mm × 10mm gap in a large wing:
- 3 × 676 = 2028 mN = **12×** — past the target!

---

## Final Answer

**With 0.1mm wire (no precision electrodes) and 35kV:**
- Minimum safe gap = 10mm
- Best single-stage config: 676 mN (4×)
- Best tandem: 5 stages at 10mm = 1352 mN (8×)
- **10× at 35kV requires 10 independent 500mm pairs at 10mm gap — physically impossible in a small plane**

**With sharp precision electrodes at 6mm:**
- 35kV/6mm/500mm/1s = 1878 mN = 11.1× ✓
- This IS achievable — but requires sharp tips, not 0.1mm wire
- Sharp tips are fragile and collect dust

**Bottom line:** 10× thrust at 35kV is achievable with sharp electrodes at 6mm gap (1878 mN per stage). With basic 0.1mm wire and 10mm minimum gap, the ceiling is ~8× via tandem (1352 mN). A practical build should target 3-5× and treat higher thrust as a significant engineering challenge requiring either precision electrode tips or a very large airframe.
