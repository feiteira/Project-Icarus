# Synthesis: Practical Designs to Multiply Airflow in Ion Wind EHD

**Date:** 2026-04-24
**Sources:** arXiv, Google Scholar, Crossref/ResearchGate, PubMed
**Note:** CNKI was inaccessible. All findings below are from open Western academic databases.

---

## What We Already Knew (from our research)
- Tandem stages: +25%/stage max (diminishing returns, Plasma Channel data)
- Harp multi-wire: power is the bottleneck, doesn't scale linearly
- Gap reduction: limited by arcing at d<10mm for 0.1mm wire at 35kV
- Best DIY path to 10×: tandem 2-stage at 8mm gap with 50W ≈ 1627 mN (9.6×)

---

## What the Papers Add (New Insights)

### 1. Wire-Cylinder-Plate Geometry ⭐⭐⭐⭐⭐
**Source:** arXiv Martins 2012 — "Simulation of wire-cylinder-plate positive corona discharge"

**The insight:** Instead of a flat collector plate, use a **cylindrical shell** (e.g., aluminum can) around the wire emitter. This channels ions through a focused gap onto the plate, acting as an accelerator tube.

- Thrust density: **0.35 N/m** (higher than flat plate)
- Ion velocity: **8-9 m/s**
- DIY: Very accessible — wire inside a can, plate at opening

**Why it matters for Icarus:** The cylindrical shell concentrates the electric field and directs ion flow more efficiently than a flat collector. This is a geometry we haven't tested — and it may boost thrust without increasing voltage or power.

---

### 2. Near-Linear Multi-Stage Scaling (with proper ducting) ⭐⭐⭐⭐⭐
**Source:** Drew & Follmer 2021 — "High Force Density Multi-Stage EHD Jets Using Folded Laser Microfabricated Electrodes"

**The insight:** The diminishing returns we found (+25%/stage) happen when stages are NOT properly ducted. When you properly channel the exhaust from stage N into stage N+1 (like a jet engine), thrust scales **near-linearly** with stage count.

- 1 stage → 2 stages = ~2× force
- 2 stages → 3 stages = ~3× force (with proper ducting)

**Why it matters for Icarus:** The Plasma Channel tandem failed because "same column of air was re-accelerated" — but that was an OPEN design. If we build a **ducted tandem** (like a tube-within-tube), each stage gets fresh air from the previous exhaust, and diminishing returns may be much less severe.

**This contradicts our earlier diminishing returns conclusion** — it applies only to open tandem, not ducted tandem.

---

### 3. Wire-to-Mesh is the Best DIY Geometry ⭐⭐⭐⭐⭐
**Source:** Tampouris & Moronis 2023 — "Two-Stage Wire-to-Mesh EHD Pump"

**The insight:** Wire-to-mesh is the simplest, most studied, most efficient EHD geometry for air moving. The mesh collector is easy to make (hardware store screen), the wire emitter is simple, and the two-stage version directly compares to mechanical fans.

- Wire: any thin conductive wire (0.1mm stainless works)
- Mesh: hardware store aluminum or steel screen
- Geometry scales predictably with voltage, gap, mesh aperture

**Why it matters for Icarus:** The NACA airfoil collector we use is complex to make and has not been empirically validated by us. Wire-to-mesh might perform nearly as well and is vastly easier to build and replicate.

---

### 4. 3D Electrode Surface Texturing ⭐⭐⭐⭐
**Source:** Lee et al. 2008 — "EHD Ion-Drag Micropump"

**The insight:** Flat electrodes produce less thrust than electrodes with **3D surface texture** (bumps, pyramids, fibrous surfaces). The rough/3D surface creates stronger local field gradients, boosting ion production and charge density.

- DIY texture options: steel wool on collector surface, sandpaper-roughened plates, wire mesh as collector, perforated metal sheet
- The principle scales: larger 3D textures = larger thrust amplification

**Why it matters for Icarus:** Instead of a smooth NACA collector foil, a **textured collector surface** (e.g., thin steel wool glued to a flat plate) may significantly amplify thrust. This is a simple modification we can test immediately on the thrust stand.

---

### 5. Vaddi Analytical Model (already in our simulator) ⭐⭐⭐⭐⭐
**Source:** Vaddi et al. 2020 — "Analytical Model for Electrohydrodynamic Thrust"

**The insight:** First-principles model we already incorporated into our simulator. Confirms our K calibration values and gives a theoretical basis for why NACA airfoil K=0.623 is reasonable.

**Status:** Already integrated into our simulator.

---

## Key Contradictions to Our Earlier Conclusions

### Contradiction 1: Diminishing Returns May Not Apply to Ducted Tandem
Our DIY_10X_RECALC concluded tandem gives only +25%/stage. But the Drew paper shows **near-linear scaling when stages are properly ducted**. The Plasma Channel "diminishing returns" data was from an OPEN design where the same air column was re-accelerated. A ducted design (tube-within-tube) gives each stage fresh, pre-accelerated air that still has momentum.

**This means our tandem 2-stage estimate of 211 mN (only 1.25×) may be pessimistic.** A ducted 2-stage could potentially give 2× or more.

**Action:** Revise tandem estimate upward. A ducted tandem at 35kV/8mm with 50W might give significantly more than the 1627 mN we calculated.

---

### Contradiction 2: Wire-to-Mesh May Rival NACA Collector
Our K calibration showed NACA airfoil (K=0.623) is 8.8× better than smooth tube (K=0.071). But the academic literature consistently shows wire-to-mesh as a top-performing geometry. The NACA airfoil has NOT been independently validated by any external source — it was from a Nanjing 2025 paper that may have used precision fabrication.

**Action:** On the thrust stand, test BOTH NACA foil and wire-to-mesh before committing to either.

---

## Actionable Findings for Carlos

**Highest priority (test on thrust stand first):**

1. **Wire-to-mesh collector** — easiest to build, well-documented performance
2. **Steel wool texture** on collector surface — may boost thrust significantly
3. **Ducted tandem design** — if we channel exhaust from stage 1 into stage 2, may get near-linear scaling instead of +25%/stage

**Design concept for a ducted tandem:**
- Stage 1: wire-to-mesh, 35kV/8mm, 500mm, in a 3D-printed duct
- Duct channels exhaust into Stage 2: second wire-to-mesh, same gap
- Each stage has its own HV feed-through (or tap from same supply)
- If Drew's near-linear scaling holds: 2 stages × T_single ≈ 2× thrust

---

## What to Upload to Site Later
Do NOT upload yet. First:
1. Validate ducted tandem thrust improvement on stand
2. Compare wire-to-mesh vs NACA foil experimentally
3. Validate steel wool texture boost

If these work, they represent genuine new findings that advance the project.
