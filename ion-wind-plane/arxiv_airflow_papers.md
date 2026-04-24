# ArXiv Papers: Practical EHD Ion Wind Airflow Multiplication & Thrust Enhancement

**Search date:** 2026-04-24  
**Total papers found:** Broad search returned thousands; narrowed to ~5 highly relevant for practical EHD airflow multiplication / thrust enhancement designs  
**Primary search query:** `"practical designs for ion wind airflow multiplication" OR "EHD thrust enhancement methods" OR "ionic wind multi-stage" OR "corona discharge airflow amplifier"`  
**Sources:** arXiv.org via API & browse

---

## Paper 1 — Wire-Cylinder-Plate Corona Discharge Ion Wind Generator

**Title:** Simulation of a wire-cylinder-plate positive corona discharge in nitrogen gas at atmospheric pressure  
**Authors:** Alexandre A. Martins  
**Year:** 2012  
**arXiv:** https://arxiv.org/abs/1202.4613

**Key practical design approach:**  
Wire-cylinder-plate geometry — a thin emitting wire inside a cylindrical shell that directs ions toward a plate electrode. This is a classic corona discharge actuator geometry. The wire corona ionizes air/nitrogen; ions are accelerated through the gap toward the plate/ground electrode, producing net thrust. Simulation validated against experimental data showing this specific geometry delivers very high thrust density.

**How it multiplies/enhances airflow/thrust:**  
The geometry concentrates the corona discharge at the wire tip for strong ionization, then uses the cylindrical shell to focus and direct the ion stream onto the plate, acting as an accelerator channel. Achieves **up to 0.35 N/m thrust per unit electrode length** and **8–9 m/s ion wind velocity** — among the highest reported for single-stage EHD devices at atmospheric pressure.

**DIY-achievable with basic tools?**  
**Yes, relatively accessible.** A thin high-voltage wire (e.g., tungsten or stainless steel sewing needle), a cylindrical metal shell (e.g., aluminum can), and a plate electrode can be assembled on a insulated frame. Requires a HV supply (Cockcroft-Walton multiplier or neon sign transformer) and current-limiting resistor. Wire spacing, cylinder diameter, and gap distance to plate are critical parameters — documented in the paper.

**Usefulness for Project Icarus:**  
⭐⭐⭐⭐⭐ — This is the **single most directly applicable paper**. The wire-cylinder-plate geometry is simple, scales well, and produces documented thrust densities useful for propulsion. Ideal starting point for a first stage ion wind thruster. The simulation framework also gives you design parameter guidance.

---

## Paper 2 — EHD Micropillar Electrode Geometry for Thrust Enhancement

**Title:** Development of EHD Ion-Drag Micropump for Microscale Electronics Cooling Systems  
**Authors:** C. K. Lee, A. J. Robinson, C. Y. Ching  
**Year:** 2008  
**arXiv:** https://arxiv.org/abs/0801.1001

**Key practical design approach:**  
3D micropillar electrode geometry etched/built on a microchannel floor — instead of flat planar electrodes, arrays of microscopic pillars are fabricated between the ion-drag electrodes. The micropillars perturb the electric field in 3D, creating a more intense field zone and enhancing ion-neutral momentum transfer per unit area.

**How it multiplies/enhances airflow/thrust:**  
The 3D micropillar geometry creates localized high-field regions at pillar tips, boosting ion production rate and charge density. At optimum pillar height (40 µm for 40 µm electrode spacing), the performance significantly exceeded equivalent planar geometry. Achieved a maximum mass flow rate of **0.18 g/min** in the micropump configuration. For macroscale EHD, the same principle applies: 3D structured electrodes multiply effective area and field non-uniformity, amplifying thrust.

**DIY-achievable with basic tools?**  
**Challenging at true micro-scale.** Micropillar fabrication requires photolithography or precision micro-milling. However, the **concept scales up** — large 3D bump arrays, pyramids, or fibrous textures on electrode surfaces can be made with basic materials (e.g., wire mesh, sandpaper-roughened plates, or 3D-printed conductive structures). The key insight is that rough/3D electrode surfaces enhance EHD thrust.

**Usefulness for Project Icarus:**  
⭐⭐⭐⭐ — The **electrode surface texturing concept** is highly practical for Project Icarus. Adding 3D texture to your corona wire or acceleration plate (e.g., using a roughened surface, mesh, or perforated plate) can amplify thrust without increasing voltage or electrode length.

---

## Paper 3 — Analytical Model for EHD Thrust (Design Tool)

**Title:** Analytical Model for Electrohydrodynamic Thrust  
**Authors:** Ravi Sankar Vaddi, Yifei Guan, Alexander Mamishev, Igor Novosselov  
**Year:** 2020  
**arXiv:** https://arxiv.org/abs/2002.11662

**Key practical design approach:**  
A first-principles analytical model coupling space charge, electric field, and momentum transfer to derive thrust force in 1D planar coordinates. The model uses the Mott-Gurney law for current density and adds drag force corrections, validated against multiple independent experimental datasets. Designed as a **direct propulsion system design tool**.

**How it multiplies/enhances airflow/thrust:**  
Not a device per se, but a **predictive modeling tool**. Knowing exactly how thrust scales with voltage, electrode spacing, gap distance, and current density allows you to **optimize geometry before building**. Proper use of this model prevents wasted iterations and identifies the sweet spots for multi-stage stacking — showing that thrust scales with the square of applied voltage and inversely with electrode gap.

**DIY-achievable with basic tools?**  
⭐⭐⭐ (model — moderate) | **Very DIY-achievable for someone who can code or use spreadsheets.** You can implement the equations in Python/MATLAB/spreadsheet to predict thrust for any geometry. No special equipment needed, just the parameter inputs (voltage, gap, electrode area). The model is specifically noted as "readily implemented in numerical simulations."

**Usefulness for Project Icarus:**  
⭐⭐⭐⭐⭐ — **Essential design tool for Project Icarus.** Use this to model and optimize your electrode geometry, voltage, and staging before fabricating. The scaling laws it reveals (thrust ∝ V²/d and increases with space charge) directly inform how to stack multiple stages for proportional thrust multiplication.

---

## Paper 4 — EHD Self-Boosted Rotary Propeller (Multi-Stage Concept)

**Title:** Electrohydrodynamic self-boosted propeller for in-atmosphere propulsion  
**Authors:** Adrian Ieta, Marius Chirita  
**Year:** 2019  
**arXiv:** https://arxiv.org/abs/1904.01395

**Key practical design approach:**  
Rotary EHD propeller — the propeller blade itself acts as one electrode (mounted on a high-voltage shaft), spinning within a ground electrode housing. The spinning motion is driven entirely by EHD ion wind impinging on blade surfaces, requiring no mechanical motor. Propellers up to **25.5 cm diameter, 27.8 g mass**, achieved liftoff with voltages from **−9.5 kV to 60 kV**, reaching rotational speeds up to **80 rot/s**. First reported self-powered EHD devices achieving independent liftoff and flight.

**How it multiplies/enhances airflow/thrust:**  
The rotary geometry provides **continuous blade regeneration** — each blade passage captures fresh ion wind, and the spin amplifies relative airflow velocity. The self-boosted propeller concept means the EHD thrust directly drives the propeller without an external motor, eliminating the mechanical transmission loss. This is a form of **mechanical amplification** of the ion wind effect — the same ion wind production is leveraged repeatedly through rotation.

**DIY-achievable with basic tools?**  
**Moderately difficult.** The spinning electrode requires a high-strength, high-voltage-compatible shaft with low friction support (ball bearings are typical). The ground electrode housing must be precisely concentric. The most challenging part is achieving the balance and mechanical tolerances while maintaining HV isolation. A skilled hobbyist could attempt this with nylon bushings, a careful lathe for concentric parts, and a HV supply of at least 20–30 kV. HV safety is critical (corona can be ozone-producing).

**Usefulness for Project Icarus:**  
⭐⭐⭐⭐ — The **self-boosted rotary concept is innovative and directly relevant** for Project Icarus, especially if a ducted fan or propeller configuration is planned. However, the mechanical complexity may be higher than a simple multi-stage linear stack. Could be explored as a second-generation design.

---

## Paper 5 — AC-Dielectric Barrier Discharge (DBD) Actuators — Streamer Ionic Wind Control

**Title:** The ElectroHydroDynamic force distribution in surface AC Dielectric Barrier Discharge actuators: do streamers dictate the ionic wind profiles?  
**Authors:** Konstantinos Kourtzanidis, Guillaume Dufour, François Rogier  
**Year:** 2020 (originally posted 2020, J. Phys. D: Appl. Phys. 2021)  
**arXiv:** https://arxiv.org/abs/2007.01614

**Key practical design approach:**  
AC-Dielectric Barrier Discharge (DBD) surface actuators — where the corona discharge occurs over a dielectric-coated electrode surface, producing a thin plasma "sheet" that drives ambient air as a wall jet. The paper specifically maps how **streamer regime** (pulse-based high-field ionization) vs. **micro-discharge regime** (lower-intensity glow) affect the spatio-temporal EHD force distribution. Demonstrates that maximum ionic wind is located at streamer elongation zones, several millimeters from the exposed electrode.

**How it multiplies/enhances airflow/thrust:**  
DBD actuators produce a **thin, high-velocity wall jet** along the dielectric surface — useful for flow control or as a thrust-generating surface. The key enhancement mechanism is that the **streamer regime dominates the positive phase EHD force production**, and optimizing for streamer formation (via voltage waveform, dielectric thickness, electrode geometry) maximizes the induced airflow velocity. AC operation allows continuous operation without spark transition.

**DIY-achievable with basic tools?**  
**Moderately accessible.** DBD requires a dielectric layer (e.g., adhesive tape, plexiglass, ceramic sheet) sandwiched between two electrodes, one exposed to air and one covered. AC voltage source needed (flyback transformer from a CRT monitor or TV, with a dielectric barrier in between). The main challenge is AC HV generation and preventing arc-through the dielectric. Careful electrode spacing is needed to avoid complete dielectric breakdown. Ozone production is a safety concern.

**Usefulness for Project Icarus:**  
⭐⭐⭐ — **Useful for surface thrust generation** — a DBD array could be applied to the wing/body surface of an ion wind plane to produce distributed thrust. However, DBD produces lower absolute thrust than wire-cylinder geometries at the same power. Best used as a **flow control / boundary layer management** complement to main thruster stages rather than the primary thrust source.

---

## Summary Table

| # | Paper | Year | Key Enhancement Mechanism | DIY? | Project Icarus Rating |
|---|-------|------|--------------------------|------|---------------------|
| 1 | Wire-cylinder-plate corona discharge (Martins) | 2012 | High-density ion acceleration geometry, 0.35 N/m, 8-9 m/s | ✅ Yes (basic HV) | ⭐⭐⭐⭐⭐ |
| 2 | EHD Micropillar electrodes (Lee et al.) | 2008 | 3D surface texturing amplifies field & thrust | ⚠️ Microfabrication hard, concept scalable up | ⭐⭐⭐⭐ |
| 3 | Analytical EHD thrust model (Vaddi et al.) | 2020 | Predictive design tool for optimization | ✅ Yes (spreadsheet/coding) | ⭐⭐⭐⭐⭐ |
| 4 | EHD self-boosted rotary propeller (Ieta & Chirita) | 2019 | Mechanical rotation amplifies ion wind continuously | ⚠️ Precision mechanical build | ⭐⭐⭐⭐ |
| 5 | AC-DBD actuators — streamers (Kourtzanidis et al.) | 2020 | AC surface plasma jet, streamer-dominated force | ⚠️ AC HV + barrier needed | ⭐⭐⭐ |

---

## Recommended Priority for Project Icarus

1. **Start with Paper 1 (Wire-cylinder-plate)** — simplest geometry, highest thrust density, most documented performance data. Build stage 1 as a proof-of-concept linear thruster.
2. **Use Paper 3 (Analytical model)** concurrently — simulate and optimize before building; understand scaling laws for multi-stage stacking.
3. **Apply Paper 2 (3D electrode texturing)** to your electrodes — increase thrust from each stage without increasing voltage.
4. **Consider Paper 4 (Rotary propeller)** for a second-generation configuration if the linear stack needs mechanical redesign.
5. **Explore Paper 5 (DBD surface actuation)** for distributed surface thrust or flow control across the wing surfaces.

---

*Generated for Project Icarus — ion wind propulsion research*  
*Search methodology: arXiv API with multiple query strategies targeting EHD ion wind thrust enhancement, multi-stage designs, and practical corona discharge amplifier configurations*
