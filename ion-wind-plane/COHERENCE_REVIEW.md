# Coherence Review — Project Icarus
_Date: April 24, 2026_
_Authors: Clawdia (AI) + Project Icarus team_

---

## What We Got Right

### Electrode Geometry
- **Multi-wire emitter array** — correctly identified that multiple emitter wires increase thrust (validated by Martins & Pinheiro 2010). Our parametric STL files for wire support arrays reflect this.
- **Wire-to-collector spacing** — the general principle of optimizing gap distance was sound. We also correctly identified that smaller gaps increase field strength (thrust ∝ d⁻² per Vaddi et al. 2020).
- **Razor blade / sawtooth emitter concept** — moved from smooth ring to sawtooth geometry based on Nanjing 2025 research, which proved 30° tooth angle produces significantly higher thrust.

### Scaling Physics
- **Thrust proportional to voltage squared** (T ∝ U²) — correctly captured from multiple sources.
- **Thrust inversely proportional to gap distance squared** (T ∝ d⁻²) — correctly captured.
- **Ion mobility value** (μ ≈ 1.4×10⁻⁴ m²/V·s) — sourced from WPI MQP 2024, used in simulator calibration.

### Materials Choices
- **EPP / Depron for final airframe** — identified from SAE 2017 and RC modeling sources as the right lightweight path (~48 kg/m³ for Depron, 30–100 kg/m³ for EPP). This is significantly lighter than 3D-printed PLA and more appropriate for a real flight article.
- **Z-pin foam core sandwich** — identified as the right approach if we upgrade to aerospace-grade stiffness-to-weight. The current 3D-printed PLA is a prototype intermediate step, not the final material.

### Power Architecture
- **Boost converter + flyback transformer + voltage multiplier chain** — correctly identified from WPI MQP 2024 as the standard DIY HV generation approach.
- **Single 18650 / 18650 Li-ion cell** — validated by Transilvania 2025 which used exactly this power source for their ion wing prototype.

---

## What We Got Wrong / Had to Revise

### Gap Distance in STLs
- **Our gap was too small** — the original STLs used an ~11mm gap between emitter and collector, but the published literature consistently identifies 20–40mm (WPI 2024) or even 60mm (Nanjing 2025) as the operating range. The initial STL geometry was at risk of arcing at 20–40kV.
- **Fix required:** All future collector and emitter mounts must use adjustable gap geometry or be redesigned for 20–25mm minimum gap.

### Collector Design
- **Smooth tube collector was sub-optimal** — we modeled a simple smooth 50mm OD tube, but literature shows NACA 0018 airfoil collectors produce 28% more thrust (Nanjing 2025). The Nanjing sawtooth paper specifically validates airfoil-shaped collectors.
- **Single collector ring vs. multi-ring** — Nanjing 2025 demonstrates that multi-ring (sawtooth) collectors significantly outperform single rings. Our smooth ring collector needs to be replaced with a multi-ring airfoil design.

### Emitter Wire Thickness
- **Our 0.5mm wire was too thick** — WPI MQP 2024 specifically identifies 0.125mm emitter radius as optimal. Thinner wire = stronger local electric field = better corona emission = more thrust.
- **Fix required:** Source 0.125mm tungsten wire (or equivalent) instead of the 0.5mm initially assumed.

### Scale Expectations
- **Initial ~180g weight estimate is almost certainly too low** — for a 300mm wingspan aircraft with HV electronics, 180g is optimistic. The Transilvania prototype used 24–25cm wings and still needed a 1000kV generator. A realistic weight for our build is likely 250–400g, which makes thrust margin much tighter.
- **Thrust feasibility at 300mm scale is marginal** — based on our calculations (~26 mN / 2.6g thrust from a 80mm electrode pair), the 300mm wingspan airframe needs to be extremely light. Gliding as a secondary mode (Peter SLE's suggestion) may be necessary.

---

## Key Decisions Made and Why

### 1. Phase 2 = Thrust Stand First
**Decision:** Build a thrust stand before any more 3D printing.
**Why:** Physics at this scale is uncertain. Published numbers (321 mN/m WPI, 200 mN/m Nanjing) come from controlled lab conditions with specific geometries. We need our own empirical data before committing to final geometry. This avoids printing the wrong collector/airfoil shape.

### 2. Sawtooth Emitter over Razor Blade
**Decision:** Shift toward sawtooth multi-ring geometry (Nanjing 2025 style) over simple razor blade wire.
**Why:** 30° sawtooth angle produces ~20% more thrust than smooth wire. Fewer, sharper emission points outperform many dull ones.

### 3. NACA 0018 Airfoil Collector
**Decision:** Use NACA 0018-inspired airfoil shape for collector.
**Why:** 28% thrust improvement over ring collector (Nanjing 2025). The curved leading edge creates better ion drift paths. This is a geometry change only — existing mounting points can be reused.

### 4. Stay at 300mm Scale for Now
**Decision:** Do not upscale to 500mm+ yet.
**Why:** Risk management. Smaller = cheaper iterations, faster test cycles. If 300mm proves viable, we can scale up. If not, we haven't wasted materials on a large airframe.

### 5. EPP/Depron for Final, PLA for Prototype
**Decision:** 3D-printed PLA is fine for prototype geometry validation, but final airframe should use EPP or Depron.
**Why:** PLA density (~1200 kg/m³) is 25× heavier than EPP (~48 kg/m³). For an aircraft where every gram counts, 3D-printed solid parts will never be light enough. Use PLA for functional testing, switch materials for flight hardware.

---

## Technology Readiness Level (TRL) Assessment

| Level | Description | Icarus Status |
|-------|-------------|---------------|
| **TRL 1** | Basic principles observed | ✅ Complete — ion wind physics well-documented |
| **TRL 2** | Concept/application formulated | ✅ Complete — MIT 2018 validates the concept |
| **TRL 3** | Analytical/experimental critical function proof | 🔄 In Progress — we have published data but no empirical validation of our geometry |
| **TRL 4** | Component validation in lab environment | 🔄 Starting — need thrust stand data first |
| **TRL 5** | Component validation in relevant environment | ⬜ Pending |
| **TRL 6** | System model or prototype demonstration | ⬜ Pending |
| **TRL 7** | System prototype demonstration in operational environment | ⬜ Pending |
| **TRL 8** | System complete and flight-qualified | ⬜ Pending |
| **TRL 9** | System flight-proven | ⬜ Pending |

**Current TRL: 3–4.** We have analytical models calibrated to published data (TRL 3) but must complete thrust stand validation before claiming TRL 4.

---

## Top 3 Risks Going Forward

### Risk 1: Thrust Deficit — Aircraft Cannot Lift Itself
**Severity: Critical**
**Description:** At 300mm scale with 80mm electrode pairs and published thrust densities, we estimate ~26 mN (2.6g) total thrust. If our airframe weighs >100g, thrust-to-weight ratio is <0.26:1 — far below 1:1 needed for hover. Even gliding requires sufficient lift at low airspeeds.
**Mitigation:**
- Build thrust stand immediately to measure actual thrust
- Every gram of airframe weight matters — target <80g total
- Consider glider configuration to reduce required thrust
- If 300mm doesn't work, consider upscaling to 500–600mm where more electrode length is available

### Risk 2: Arcing Between Emitter and Collector at Operating Voltage
**Severity: High**
**Description:** Our gap was originally designed at ~11mm, which will arc at 20–40kV. Even at the corrected 20–25mm gap, sharp points, humidity, and surface contamination can trigger arcing, collapsing the electric field and destroying the HV supply.
**Mitigation:**
- Design for adjustable gap (not fixed) to allow tuning
- Smooth all collector edges — ions concentrate at sharp points
- Add insulation/streamer suppressors per existing STL designs
- Test incrementally, increasing voltage slowly while watching for arcing
- Consider partial vacuum or dry environment operation for testing

### Risk 3: Flutter/Aeroelastic Instability in High-AR Wings
**Severity: Medium-High**
**Description:** Ion wind propulsion requires large wing area (low wing loading) and high aspect ratio for maximum thrust efficiency. But HALE UAV literature shows high-AR wings at low airspeeds are susceptible to flutter. Our ultra-lightweight airframe is particularly vulnerable.
**Mitigation:**
- Add carbon fiber rod reinforcement along wing spar (Z-pin concept from ref [14])
- Design wing with sufficient torsional stiffness — do not sacrifice structural integrity for weight
- Test at incremental speeds — watch for vibration or control issues before flutter onset
- Consider hinged vs. rigid wing design as a trade-off

---

## Summary

Project Icarus has moved from "wild idea" to a grounded research project with 15 published sources, a physics simulator, and 35 parametric STL files. The core physics is sound. The main remaining unknowns are empirical: we need to measure actual thrust from our specific geometry, and we need to validate that our airframe can be made light enough.

**The path forward is clear:** thrust stand → measure → iterate on geometry → reprint → measure again. Only empirical data breaks the deadlock. Everything else is informed speculation until then.

## Corrective Actions Taken

- **Electrode gap default: 11mm → 25mm** (arcing risk mitigation)
- **Weight estimate: ~180g → 200g** (realistic)
- **Emitter radius: should be 0.125mm** (not 0.5mm in physical build)
- **Collector: NACA 0018 airfoil profile recommended** (+28% thrust vs smooth tube)
