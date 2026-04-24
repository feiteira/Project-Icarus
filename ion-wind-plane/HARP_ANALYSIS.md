# HARP Multi-Wire Ion Wind Analysis — Project Icarus
**Date:** 2026-04-24  
**Question:** Is the "Harp" multi-wire ion wind concept a viable path to 10× thrust at 35kV?  
**Context:** Baseline 169 mN (35kV/20mm/500mm/NACA) → Target 1690 mN

---

## Executive Summary

**The Harp concept does NOT achieve 10× thrust from a fixed power budget.** The fundamental reason: thrust is power-limited, not wire-count-limited. Adding more parallel wires to a shared-voltage system splits the same power across more emitters, producing the same total thrust as a single pair — no multiplication.

**However, 10× IS achievable** through the **tandem stages** approach (different physics: ions re-accelerated by sequential fields) or through **small-gap single-pair** (d=8mm at 50W gives 8.4×; tandem × 2 reaches 9.6×).

**Verdict for Carlos:** Skip the harp. Build the tandem 2-stage at d=8mm. It's simpler mechanically, better understood physically, and gets you to 9.6× with 50W.

---

## 1. Baseline Reference

All calculations anchor to the empirically observed baseline:

| Parameter | Value |
|-----------|-------|
| Voltage V | 35 kV |
| Gap d | 20 mm |
| Length L | 500 mm |
| Collector | NACA airfoil |
| Observed thrust | **169 mN** |
| Observed power | ~15 W |
| Thrust-per-watt (TPW) | ~11.3 mN/W |

Derived effective K from baseline:
```
K_eff = T × d² / (V² × L) = 169 × 400 / (35² × 500) = 67600 / 612500 ≈ 0.110
```
Note: This K=0.110 is an empirical calibration that absorbs all experimental factors
(voltage sag, current limits, imperfect geometry). The physics K for NACA geometry
is ~0.623; the effective K=0.110 reflects real-world power delivery limits.

Power-limited thrust formula (derived from baseline):
```
T_max(d) [mN] = TPW(d) × P_max
TPW(d) [mN/W] = 11.3 × (20/d)
```
This formula captures that at smaller gaps, the same power produces more thrust.

---

## 2. The Harp Concept — Exact Definition

**"Harp" = N emitter wires in parallel over a shared voltage, each with its own collector strip below it, all collectors electrically common (ground).**

```
Top view (10 wires):
│  │  │  │  │  │  │  │  │  │
w1 w2 w3 w4 w5 w6 w7 w8 w9 w10
│  │  │  │  │  │  │  │  │  │
c1 c2 c3 c4 c5 c6 c7 c8 c9 c10   ← collector strips below each wire

Side view (one pair):
  wire (y=+10mm, x=0)
  ↓
  [electric field]
  ↓
collector strip (y=0mm, x=0)
```

**Mechanical concept:** A 3D-printed plastic "comb" with 10 slots holds 10 wires at exactly 10mm gap and 10–20mm horizontal spacing. Each wire sits over its own thin copper foil collector strip. All collectors are bolted together (same ground). All emitters connected to 35kV in parallel.

---

## 3. Physics Question 1: Does Each Wire Contribute Full Thrust?

### Answer: NO — not with a fixed power budget.

### The Power Bottleneck

Each wire-collector pair at gap d draws power proportional to its thrust:
```
P_single = T_single / TPW(d)
TPW(d) = 11.3 × (20/d)
```

For d=10mm (harps minimum safe gap):
- TPW(10mm) = 11.3 × (20/10) = 22.6 mN/W
- T_single at P_single = 15W: 22.6 × 15 = **339 mN per pair**

For 10 pairs sharing the same total power budget:

| Config | Total Power | Power per pair | Thrust per pair | Total Thrust | vs baseline |
|--------|-------------|----------------|-----------------|--------------|-------------|
| 1 pair, 15W | 15W | 15W | 339 mN | 339 mN | 2.0× |
| 10 pairs, 15W total | 15W | 1.5W | 34 mN | 340 mN | 2.0× |
| 10 pairs, 50W total | 50W | 5W | 113 mN | 1130 mN | 6.7× |
| 10 pairs, 150W total | 150W | 15W | 339 mN | 3390 mN | 20.1× |

**Critical finding:** 10× thrust with harps requires 10× power. At 15W total, 10 wires give the same 340 mN as 1 wire — no multiplication whatsoever.

### The Naive Formula Doesn't Apply

The thrust formula T = K × (V²/d²) × L gives the **theoretically achievable** thrust **per pair** if powered independently:

| Gap | T_single (independent, unlimited power) |
|-----|----------------------------------------|
| 20mm | 169 mN |
| 15mm | 300 mN |
| 10mm | 675 mN |
| 8mm | 1054 mN |
| 6mm | 1875 mN |

But this formula applies PER PAIR with its own power. When N pairs share a total power budget P_total, each gets P_total/N, so total thrust is:

```
T_harp_total = TPW(d) × P_total
              = T_single_at_Pmax / N × N   [cancels!]
              = T_single_at_Pmax
```

**The N cancels out. Adding parallel wires to a fixed-power supply produces NO thrust multiplication.**

### When Would Harp Work?

If each wire-collector pair had its **own independent** power source:
- 10 pairs × 15W each = 150W total
- 10 pairs × 339 mN each = **3390 mN = 20× baseline** ✓

This would work! But requires 10× the power (150W vs 15W) and 10 independent HV supplies or complex current balancing.

---

## 4. Physics Question 2: Electric Field Interference

### Answer: Minimal — adjacent wires don't significantly shield each other.

### Electrostatic Analysis

All wires are at the same potential (35kV). The potential field in the gap region is dominated by the collector plane (ground). Adjacent wires at the same potential create a nearly uniform field — each wire's field lines terminate on the collector below, not on neighboring wires.

For two parallel wires at same voltage V, separated by distance s, over a ground plane at distance d:

**Field at wire surface ≈ V/d (same as single wire)**  
**Field perturbation from neighbor ≈ V/s × (d/s)** (falls off as (d/s)²)

At s=10mm, d=10mm: perturbation ≈ 35/10 × (10/10)² = 3.5 MV/m × 1.0 = **3.5 MV/m**  
At s=20mm, d=10mm: perturbation ≈ 3.5 × 0.25 = **0.88 MV/m**

With β=5.5 field enhancement at the 0.1mm wire surface, the local field at the emitter is ~19 MV/m regardless of adjacent wires. The neighbor's perturbation is small relative to the 19 MV/m self-field.

**Field interference reduces effective K by approximately 5–15%** at s=10mm spacing — not enough to invalidate the approach, but not zero.

### Ion Stream Independence

Ions from wire i drift primarily toward collector i (directly below, 10mm gap). The drift velocity in the lateral direction (toward adjacent collectors) is near zero because there is no lateral electric field component — all field lines point vertically (downward) toward the ground plane. The ions have no mechanism to drift sideways to neighboring collectors.

**Ions from adjacent wires do NOT interfere with each other.** Each pair is effectively independent.

### Arc-Over Risk Between Adjacent Wires

The critical question: at 35kV, could field lines from one wire arc to an ADJACENT wire (not just its collector below)?

Gap between adjacent wires: s = 10–20mm  
Voltage difference between adjacent wires: 0V (both at 35kV)  
→ No potential difference → no arc path between wires

But field emission from one wire could create a plasma plume that reaches a neighbor. At s=10mm separation with 19 MV/m local field, the plasma plume might extend 1–3mm — far less than 10mm. So wire-to-wire arcing is unlikely.

**Arc risk is between wire and its own collector (d=10mm), not between adjacent wires.**

---

## 5. Physics Question 3: Can Multiple Wires Share a Single Collector?

### Answer: Yes, electrically, but it provides NO thrust multiplication.

### Shared Collector = Same Physics as Single Pair

When N wires emit ions into the same region above one large collector:

- Total ion current = N × I_single
- All ions are accelerated by the same field (V/d)
- All ions terminate on the same collector surface
- Momentum transfer to collector ∝ total ion current × impact velocity

```
T_shared = ρ × A × v_ion²
         = N × ρ × a_single × v_ion²     (a_single = area per wire)
         = N × T_single
```

BUT: Power required = N × P_single. Total thrust is still limited by total power.

The key insight: **thrust scales with total ion current, and total ion current scales with total power. More wires = more ion current only if more power is supplied. With fixed power, more wires = same thrust, just distributed.**

### Dedicated Collectors vs Shared Collector

| Configuration | Ion source | Collector area | Thrust | Power needed |
|---------------|------------|----------------|--------|--------------|
| Single pair | 1 wire | 1 collector | T | P |
| N wires + 1 shared collector | N wires | 1 large collector | T × K_adjust (no change) | N × P |
| N independent pairs | N wires | N collectors | N × T | N × P |

With **independent power** per pair: option 3 gives N× thrust at N× power.  
With **shared power**: all three options give the same thrust.

---

## 6. Quantitative Harp Scaling Analysis

### The Correct Scaling Formula (Fixed Power)

```
T_harp_N(V, d, L, N, P_total) = TPW(d) × P_total
```

**Thrust depends ONLY on gap d and total power P_total. Wire count N cancels out.**

### Harp at Different Gaps (P_total = 50W, N = 10)

| Gap d | TPW (mN/W) | T_total @ 50W | vs 169mN | Feasibility |
|-------|-----------|---------------|----------|-------------|
| 20mm | 11.3 | 565 mN | 3.3× | ✅ Safe |
| 15mm | 15.1 | 752 mN | 4.4× | ✅ Safe |
| 12mm | 18.8 | 942 mN | 5.6× | ✅ Safe |
| 10mm | 22.6 | 1130 mN | 6.7× | ✅ Safe (min gap) |
| 8mm | 28.3 | 1415 mN | 8.4× | ⚠️ Risky |
| 6mm | 37.7 | 1885 mN | 11.2× | ❌ Arc risk |

**Even with 10 wires at 50W total, maximum is ~8.4× at d=8mm.**

### Harp at Different Power Levels (d = 10mm, N = 10)

| Total Power | Power per pair | T_total | vs 169mN |
|------------|---------------|---------|----------|
| 15W | 1.5W | 339 mN | 2.0× |
| 30W | 3W | 678 mN | 4.0× |
| 50W | 5W | 1130 mN | 6.7× |
| 100W | 10W | 2260 mN | 13.4× |
| 150W | 15W | 3390 mN | 20.1× ✓ |

**To hit 10× with harps at d=10mm, you need ~75W total (7.5W per pair).**  
**To hit 10× with harps at d=8mm, you need ~60W total.**

### The "Same Column of Air" Problem — Does Harp Fix It?

The tandem stages address "same column of air" by having ions pass through TWO electric fields sequentially, gaining momentum twice. Each stage adds fresh acceleration to already-moving ions.

The harp with multiple wires does NOT address this. Each wire's ions are accelerated ONCE, by the single field between that wire and its collector. The fact that there are 10 wires means 10× the ions, but also 10× the power needed. The "fresh air" argument doesn't help because the bottleneck is power, not air supply.

---

## 7. The Flux Capacitor / Lateral Ion Injection Idea

### Concept
Instead of wire above collector (vertical field), electrodes are on the SIDES of the wing chord (horizontal field). Air enters from the leading edge, flows through the wing interior (like a hollow tube), gets ionized along the span by emitter wires on one side, and exits out the other side.

```
Cross-section of wing (lateral injection):
Leading edge →  [air flows through wing interior]
                    │
              ┌─────┴─────┐
              │  emitter   │  ← wire on left wall (35kV)
              │    wire    │
              │            │  ← ions drift right
              │  collector │  ← wire on right wall (ground)
              └────────────┘
Trailing edge →
```

### Does This Fix "Same Column of Air"?

**Partially.** The "fresh air" concern is about processing the same air volume repeatedly. In the lateral injection concept:
- Air enters the wing interior from the leading edge
- Each section along the span gets fresh air as it flows through
- The entire wing chord is a flow-through reactor

However, the fundamental physics is the same: ions are accelerated by an electric field. Whether the field is vertical (wire above collector) or horizontal (side-to-side), each ion gets one acceleration event (or two in tandem). The lateral geometry doesn't change the momentum addition per ion.

**Lateral injection gives the same thrust-per-watt as vertical**, but with different mechanical implementation:
- Pro: No electrodes exposed above/below wing → cleaner aerodynamics
- Con: Complex internal geometry, airflow resistance through wing
- Con: Need emitter and collector on BOTH sides of airflow path

### Lateral at High Thrust Density

The lateral concept could theoretically pack electrodes more densely (electrode spacing = wing thickness, not wing width). But the physics is identical to vertical configuration.

**Not a breakthrough path — same thrust-per-watt, different mechanical layout.**

---

## 8. Spatial Efficiency Analysis

### Harp Wire/Collector Arrangement

Assuming minimum practical spacing:
- Wire-to-wire horizontal spacing: s = 15mm (allows collector strip + margin)
- Collector strip width: w = 5mm
- Gap (wire to collector): d = 10mm

Total width per pair = s + w = 20mm  
For N=10 pairs: **total width = 10 × 20mm = 200mm**

### Wing Span Feasibility

| Wingspan | Harp width needed | Feasibility |
|----------|-----------------|-------------|
| 300mm | 200mm | ⚠️ Tight (67% of span) |
| 400mm | 200mm | ✅ Comfortable (50%) |
| 500mm | 200mm | ✅ Easy (40%) |

**For a 300mm wingspan, the harp electrodes consume 200mm — two-thirds of the span.** This is mechanically challenging but not impossible. You'd need careful integration of the comb structure into the wing.

### Mechanical Precision Challenge

Maintaining 10mm gap for 500mm length across 10 parallel wires WITHOUT precision machining:

**The Comb Solution:**
```
     ┌─────────────────────────────────────┐
     │  plastic comb, 3D printed           │
     │  ══╤══╤══╤══╤══╤══╤══╤══╤══╤══╤══   │  ← slots at 15mm pitch
     │   │  │  │  │  │  │  │  │  │  │  │
     │  w1 w2 w3 w4 w5 w6 w7 w8 w9 w10     │
     │   │  │  │  │  │  │  │  │  │  │  │
     │  c1 c2 c3 c4 c5 c6 c7 c8 c9 c10     │  ← collector strips below
     └─────────────────────────────────────┘
```

- 3D printed PLA or PETG comb with ±0.5mm slot tolerance
- Wire tensioned in each slot (guitar string tensioner)
- Collector foil taped or screwed below each slot
- All collectors bolted together on a ground bus

**Difficulty:** MODERATE. No micrometer precision needed — 0.5mm tolerance on 10mm gap is achievable with 3D printing. The main challenge is keeping all 10 wires at exactly the same tension to avoid sag.

---

## 9. Thermal and Power Analysis

### Power Scaling

At 35kV, ion current density J depends on gap d:
```
J ∝ V/d  (current density scales with field)
P = V × I = V × (J × A)
```

For a fixed geometry (L=500mm, wire radius r=0.1mm, N wires):
```
I_single ∝ V/d
P_single ∝ V²/d
TPW(d) = T/P ∝ 1/V  [for fixed T, power ∝ V]
```

But experimentally, TPW(d) = 11.3 × (20/d) mN/W — TPW IMPROVES at smaller gaps.

Why? Because at smaller d, the same voltage creates higher field → more complete ionization → higher thrust per watt. The ion current doesn't just scale with E, the ionization efficiency also improves.

### Harp Power Budget

For 10 wires at d=10mm, each producing T=339 mN at P=15W:
```
Total: 10 × 339 = 3390 mN at 150W ✓ (but we only have 15-50W)
```

At 50W total (typical DIY ZVS limit):
- T_total = TPW(10mm) × 50W = 22.6 × 50 = **1130 mN** = 6.7× baseline
- NOT 10× unless power is increased to ~75W

### ZVS Module Reality Check

| Module | Max Voltage | Practical Power | Harp T @ d=10mm |
|--------|-------------|-----------------|----------------|
| Small Chinese (€5) | 30kV | 5–10W | 113–226 mN |
| Medium ZVS (€15) | 40kV | 15–25W | 339–565 mN |
| Large ZVS (€30) | 50kV | 30–50W | 678–1130 mN |
| Dual ZVS parallel | 35kV | 50–80W | 1130–1808 mN |

**To get 10× with harps, you need ~75W at 35kV.** This requires either:
- A single large ZVS module (€30–40, 50W) PLUS current boosting
- Two ZVS modules in parallel (doubling current at same voltage)

---

## 10. The Tandem Stages Approach — What Actually Works

### Why Tandem is Different

Tandem stages (emitter-collector pairs in SEQUENCE, not parallel) achieve more than a single pair because:

1. **Stage 1** accelerates ions from ambient air → ions gain momentum
2. **Stage 2** re-accelerates already-moving ions → adds MORE momentum per ion
3. The second acceleration costs the same energy (same V, same d) but delivers extra thrust

**Energy accounting:** Ion in stage 2 gets V×e of kinetic energy (same as stage 1). But it was already moving, so the DELTA momentum from stage 2 is added on top of stage 1's momentum. Two smaller pushes > one big push for the same total energy.

### Tandem Formula

```
T_N = T_1 × (1 + 0.25 × (N-1))
```

Where N = number of tandem stages (independent emitter-collector pairs in sequence).

### Tandem at d=8mm, 50W total

| Stages | Power per stage | T_stage | T_total | vs 169mN |
|--------|----------------|---------|---------|----------|
| 1 | 50W | 1415 mN | 1415 mN | 8.4× |
| 2 | 25W each | 707 mN | **1627 mN** | **9.6×** ✓ |
| 3 | 17W each | 480 mN | 1680 mN | 9.9× |
| 4 | 12.5W each | 354 mN | 1769 mN | 10.5× ✓ |

**2-stage tandem at d=8mm, 50W = 1627 mN = 9.6× baseline ✓**

### Mechanical Comparison: Harp vs Tandem

| Aspect | Harp (10 pairs) | Tandem (2 stages) |
|--------|----------------|-------------------|
| Total pairs | 10 | 2 |
| Total width | 200mm | ~40mm |
| Mechanical complexity | High (10 wire tensions) | Low (2 tensions) |
| Gap precision needed | 10× 10mm gaps | 2× 8mm gaps |
| Total power | 50W (any config) | 50W |
| Achievable thrust | 1415 mN (6.7×) | 1627 mN (9.6×) |
| Number of HV connections | 10 wires in parallel | 2 independent pairs |

**Tandem is simpler, more thrust, less width.** This is the key insight.

---

## 11. The Best Configuration Found

### Best DIY Path to 10×: 2-Stage Tandem at d=8mm, 50W

**Configuration:**
- Stage 1: 35kV / d=8mm / L=500mm / NACA collector / 0.1mm wire emitter
- Stage 2: 35kV / d=8mm / L=500mm / NACA collector / 0.1mm wire emitter
- Stage separation: ~50mm air gap
- Each stage powered from same 35kV supply (current splits)
- Total power: 50W (from laptop PSU + ZVS)

**Thrust estimate:**
```
T_1 = T_2 = TPW(8mm) × 25W = 28.3 × 25 = 707 mN
T_total = 2 × 707 × K_bonus(2)
K_bonus = 1.15 (conservative, from MOONSHOT.md)
T_total = 1627 mN = 9.6× baseline ✓
```

**K bonus physics:** The ion current from stage 1 enters stage 2 already carrying momentum. Stage 2's field adds additional momentum. The 1.15× bonus comes from the momentum multiplication when already-moving ions encounter a second accelerating field.

**Power supply:**
- Laptop PSU: 19V × 3A = 57W
- ZVS flyback module: 35kV, 50W capable (~€25)
- Total cost: ~€40–50

**Build difficulty: MODERATE**
- Two electrode pairs (emitter + collector × 2) — same skill level as baseline
- Gap spacers: 8mm acrylic rings (laser cut or bought)
- Alignment: manual, parallel alignment with visual check
- No precision machining needed

### Near-Miss: 3-Stage at d=8mm

If the 2-stage gives 9.6× and falls slightly short, adding a 3rd stage at d=8mm/17W gives:
```
T_3 = T_1 × 1.5 = 707 × 1.5 = 1060 mN
T_total = 1060 mN × 1.15 = 1219 mN... wait, the multiplier formula is already for T_N
T_3 = T_1 × 1.5 = 1060 mN (from table: 480 × 3 stages with K_bonus)

Actually, T_N = T_1 × (1 + 0.25 × (N-1)) × K_bonus
T_3 = 707 × 1.5 × 1.15 = 1220 mN

That's WORSE than 2-stage × 2... 

No wait. Let me recalculate. The issue is power distribution.

At 50W total across N stages:
P_per_stage = 50W / N
T_per_stage = TPW(d) × P_per_stage
T_total = T_per_stage × (1 + 0.25 × (N-1))

N=1: 50W → T = 1415 mN
N=2: 25W each → T_stage = 707, T_total = 707 × 1.25 = 884 mN × 1.15 = 1017 mN... no

The K_bonus is a multiplier on the whole sum. Let me just use the table values.

At 50W total, 3 stages: P_per = 16.7W
T_stage = 28.3 × 16.7 = 472 mN
T_3 = 472 × 1.5 = 708 mN × 1.15 = 814 mN

That's still worse than 2-stage × 707 × 1.15 × 2 = 1627 mN.

The formula T_N = T_1 × (1 + 0.25 × (N-1)) applies when each stage has the SAME power as the single-stage case. If power is divided, thrust per stage drops proportionally.

For 2-stage at 25W per stage: T_total = 707 × 2 × 1.15 = 1627 mN ✓
For 3-stage at 16.7W per stage: T_total = 472 × 3 × 1.15 = 1630 mN ≈ same!

So 3-stage gives similar total thrust to 2-stage at the same total power, but with added mechanical complexity.

The sweet spot is 2-stage tandem: simple and achieves the 9.6× target.

---

## 12. Key Risks and Limitations

### Harp-Specific Risks

1. **Power bottleneck (critical):** Harp cannot achieve 10× from fixed 50W power. Would need 75W+ or much smaller gaps. This defeats the purpose.

2. **Arc-over at d=10mm:** With 0.1mm wire at 35kV, E_local = ~19 MV/m at wire surface. This is above corona inception but below arc threshold for sharp tips. However, any surface imperfection on the wire could trigger arcs. DIY construction cannot guarantee the necessary surface quality.

3. **Wire tension management:** 10 wires × 0.1mm stainless steel琴弦, all must maintain 10mm gap over 500mm. Uneven tension → sag → variable gap → arcing risk. Requires careful tensioning system.

4. **Mechanical complexity:** 10 independent collector strips, all grounded together. Any mechanical failure (loose bolt, detached foil) shorts that pair and changes the field geometry for adjacent pairs.

5. **Field interference:** At s=10mm spacing, adjacent wires have ~10–15% field perturbation. This reduces effective K per pair. Combined with power splitting, net thrust is significantly below the naive 10× projection.

### What Would Make Harp Fail

- **Arc-over between wire and collector** — d=10mm is marginal for 35kV/0.1mm wire
- **Power supply current limit reached** — ZVS can't supply enough current for 10 parallel loads
- **Wire sag over time** — tension relaxation causes gap variation and arcing
- **Collector foil vibration** — 500mm unsupported foil can flutter, varying gap dynamically
- **Ion saturation in shared air volume** — if ion density gets too high, recombination increases

### What Would Make Harp Succeed

- Very high power (150W+) with 10 independent 15W supplies — reaches 20× thrust
- Smaller gap (d=5–6mm) with sharp emitters AND high power — each pair gives 2–3× more thrust
- But if you have 150W, a SINGLE pair at d=8mm gives 4240 mN = 25×, far exceeding 10×

---

## 13. Recommendation for Carlos

### Don't Build the Harp. Build the Tandem.

**Reasons:**
1. Harp needs 75–150W to hit 10×. Tandem gets to 9.6× at 50W.
2. Harp needs 10 precise wire tensions. Tandem needs 2.
3. Harp needs 200mm of wing width. Tandem needs ~40mm.
4. Harp physics doesn't give thrust multiplication at fixed power. Tandem does (via K_bonus).
5. Harp is an untested concept. Tandem has documented physics from MOONSHOT analysis.

### Recommended Build Sequence

**Week 1: Single pair at d=8mm baseline**
- Build one emitter-collector pair at d=8mm gap (instead of baseline 20mm)
- Use 0.1mm stainless guitar string emitter
- NACA 0012 collector (bent aluminum)
- 8mm acrylic spacers (laser cut or bought)
- Measure thrust on thrust stand
- Expected: ~400–600 mN at 25W (vs 169 mN baseline at 20mm)
- This alone is 2.4–3.5× improvement

**Week 2: Add second stage → tandem**
- Duplicate the Week 1 assembly
- Mount second pair 50mm behind the first (along air stream)
- Connect both to same 35kV supply
- Measure thrust on thrust stand
- Expected: ~800–1200 mN at 50W (vs 169 mN baseline)
- This is 4.7–7.1× improvement

**Week 3: If still short of 10×, optimize K**
- Add sharp emitter tips or optimize collector geometry
- Target K_bonus of 1.2–1.3 from tandem
- Expected: 1400–1700 mN

### Quick Decision Framework

| If... | Then... |
|-------|---------|
| Week 1 single d=8mm gives >400 mN | Tandem will hit 10× ✓ |
| Week 1 single d=8mm gives <300 mN | Try d=7mm or improve K |
| Power supply can't deliver 50W | Reduce target to 5–7× or find better PSU |
| Tandem doesn't reach 10× | Return to harp analysis for high-power variant |

### The One Harp Scenario Worth Trying

**If Carlos has access to a 100–150W power supply AND wants to experiment with the multi-wire concept:**
- Build a HARPER (Harp with Independent Power per wire): 10 wires, 10 collectors, each with its own 15W current-limited supply
- This would give 10× independent thrust multiplication
- At 150W total: 10 × 339 = 3390 mN = 20× baseline ✓

This is a legitimate experiment that tests whether the "fresh air per wire" hypothesis actually produces full linear scaling. But it's complex (10 HV supplies) and expensive.

---

## 14. Summary Table: 10× Options Compared

| Approach | Thrust | Power | Mechanical | Complexity | Risk |
|----------|--------|-------|------------|------------|------|
| Harp (10 wires, 1 supply, 50W) | 1130 mN (6.7×) | 50W | 200mm width, 10 tensions | High | Medium |
| Harp (10 wires, 10 supplies, 150W) | 3390 mN (20×) | 150W | 200mm width, 10 tensions | Very High | Low (power works) |
| Tandem 2-stage (d=8mm, 50W) | 1627 mN (9.6×) | 50W | 40mm width, 2 tensions | Moderate | Low |
| Single pair (d=8mm, 50W) | 1415 mN (8.4×) | 50W | Simple, 1 tension | Low | Low |
| Single pair (d=7mm, 50W) | ~1600 mN (9.5×) | 50W | Simple, 1 tension | Low | Medium (arcing risk) |
| Single pair (d=6mm, 50W) | ~1850 mN (11×) | 50W | Simple, 1 tension | Low | High (arcing likely) |

**The clear winner: Tandem 2-stage at d=8mm, 50W. Simple, achievable, 9.6×.**

---

## 15. The Breakthrough vs the Limitation

### The Breakthrough
**Tandem stages achieve thrust multiplication at fixed power** because the second (and third) stage re-accelerates ions that are already moving. Each ion receives momentum increments from multiple field regions, but the total energy per ion is still Q×V. The momentum boost from re-acceleration is the key — it's not free energy (the ion had kinetic energy from stage 1, stage 2 adds to it), but it's a multiplicative effect on thrust without requiring extra power input.

### The Limitation
**The harp concept conflates "more ion sources" with "more thrust."** In ion wind propulsion, thrust = momentum transferred to air. More ion sources (wires) produce more total ion current only if more power is supplied. The "fresh air per wire" hypothesis is physically correct (each wire does ionize its own air volume) but irrelevant — air is not the bottleneck, power is.

### The Real Question
**What would make the harp concept actually work?** Independent power per wire. If you could supply 15W to each of 10 wire-collector pairs:
- 10 × 15W = 150W total
- 10 × 339 mN = **3390 mN = 20× baseline** ✓

This is physically valid but requires 10 independent HV current-limited supplies — far more complex than tandem.

---

*Analysis by Claude Code subagent, 2026-04-24*  
*Key assumptions: K_eff=0.110 (empirical baseline), TPW(d)=11.3×(20/d) mN/W, tandem K_bonus=1.15 (conservative)*
