# PubMed Search: EHD Ion Wind Propulsion — Practical Designs for Airflow/Thrust Multiplication

**Search query:** "electrohydrodynamic ion wind thrust multiplier" OR "ionic wind practical design" OR "EHD propulsion airflow enhancement"
**Date:** 2026-04-24
**Total papers found via PubMed:** 2
**Note:** PubMed is a biomedical database; EHD propulsion research is primarily published in physics/engineering journals (IEEE, AIAA, J. Phys. D, Scientific Reports). Many relevant papers appear in non-PubMed-indexed venues. The 2 results below are the only PubMed-indexed papers found across all attempted query variations.

---

## Paper 1

**Title:** Sawtooth multi-ring electrodes for ionic wind propulsion
**Authors:** Miaosen Hou, Haoyuan Li, Yuxiang Li, Zhaotan Yao, Zequn Cui, Cheng Wang, Qiang Chen
**Year:** 2025
**Source:** Scientific Reports

**Key practical design approach:**
Serrated (sawtooth) single-ring emitter electrode paired with a multi-ring collector. The emitter uses a sawtooth/serrated edge to concentrate the electric field and enhance corona discharge at multiple points, while the multi-ring collector provides successive ion collection stages.

**How it multiplies/enhances airflow/thrust:**
1. The sawtooth emitter increases ion generation by creating multiple high-field points along the ring circumference
2. The multi-ring collector improves ion drift efficiency by offering multiple collection surfaces along the flow path
3. Combined effect: **1–2× thrust increase** over single-ring designs, with **28.2% thrust density enhancement** at optimized parameters
4. Maximum thrust achieved: **164 mN/m** at 40 kV, 60 mm gap
5. The design is compact and lightweight (17 g) with good structural stability

**DIY-achievable with basic tools?**
Moderate difficulty. The electrode rings (copper/wire) and sawtooth fabrication are doable with basic workshop tools. The main requirement is a **high-voltage power supply (20–40 kV DC)** and precise gap control — this is the main DIY barrier.

**Usefulness for Project Icarus:** ⭐⭐⭐⭐⭐
— The sawtooth + multi-ring collector design is the most directly applicable paper found; it offers a clear 1–2× thrust multiplication path with a practical, lightweight 17 g unit that aligns well with an ion wind plane's mass constraints.

---

## Paper 2

**Title:** Successively accelerated ionic wind with integrated dielectric-barrier-discharge plasma actuator for low-voltage operation
**Authors:** Shintaro Sato, Kento Yoshida, Hiroshi Nishida, Takuya Hara, Seiichi Sudo
**Year:** 2019
**Source:** Scientific Reports

**Key practical design approach:**
Multi-electrode DBD (dielectric-barrier-discharge) plasma actuator using 3–9 electrodes in a carefully arranged configuration. Uses a hybrid DC + pulsed voltage waveform (8 kV DC + 25 kHz negative pulses) applied across exposed and covered electrodes separated by a dielectric layer. The key innovation is controlling surface charge on the dielectric to avoid "counter ionic wind" that normally degrades multi-electrode designs.

**How it multiplies/enhances airflow/thrust:**
1. Each additional electrode in the multi-electrode array **linearly increases** the integrated EHD force (thrust scales with electrode count)
2. The surface-charge absorption effect at the downstream exposed electrode **enhances the EHD force** beyond what single-stage designs produce
3. The mutually enhanced (rather than degraded) EHD force is achieved by proper voltage waveform and electrode arrangement timing
4. At 9 electrodes with 2000 Hz pulse repetition: significantly more thrust than a conventional AC DBD plasma actuator of similar power
5. Operates at **lower voltage than typical corona-discharge EHD devices**, avoiding the need for expensive high-voltage power supplies
6. **Thrust-to-power ratio is higher** than conventional AC DBD actuators when using 3+ electrodes

**DIY-achievable with basic tools?**
Moderate–high difficulty. DBD actuators require precise dielectric layering (Kapton, Mica, or similar), electrode placement with tight tolerances, and a **combined DC + pulse waveform generator** — more complex electronics than a simple corona setup.

**Usefulness for Project Icarus:** ⭐⭐⭐⭐
— The successive acceleration concept (multi-stage thrust multiplication via electrode staging) is excellent for scaling thrust output, though the DBD fabrication complexity and pulse electronics add build difficulty.

---

## Summary Table

| # | Paper | Year | Key Design | Thrust Multiplier | DIY Difficulty |
|---|-------|------|-----------|-------------------|----------------|
| 1 | Hou et al. — Sawtooth multi-ring electrodes | 2025 | Serrated emitter + multi-ring collector | **1–2× over baseline** + 28.2% density gain | Moderate (needs 20–40 kV supply) |
| 2 | Sato et al. — DBD multi-electrode acceleration | 2019 | 3–9 electrode DBD with controlled surface charge | **Linear scaling with electrode count** | High (DBD dielectric + pulse electronics) |

---

## Recommendation for Project Icarus

**Start with Paper 1 (Hou 2025):** The sawtooth multi-ring design offers the clearest DIY path to thrust multiplication. It has a known mass (17 g), proven thrust output (164 mN/m), and the electrode geometry can be replicated with copper wire rings and a sawtooth-shaped emitter formed from copper sheet or wire. The main DIY investment is a 20–40 kV power supply (e.g., flyback transformer from a CRT monitor or dedicated HV module).

**Scale up using Paper 2 (Sato 2019):** For a second-generation design, the multi-stage DBD approach can stack multiple actuator modules for additive thrust without adding proportional power consumption.
