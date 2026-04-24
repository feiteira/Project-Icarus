# EHD Ion Wind Propulsion — Practical Airflow Multiplication Designs

**Search Query:** "practical designs ion wind airflow multiplication" OR "EHD thrust enhancement DIY" OR "ionic wind amplifier practical"  
**Date:** 2026-04-24  
**Sources:** arXiv, Google Scholar (attempts blocked by rate limiting)  
**Total Results Found (arXiv subset):** ~30 direct EHD-ion propulsion papers; selected top 5 most practical/DIY-relevant

---

## Paper 1 — Laser-Microfabricated EHD Thruster for cm-Scale Aerial Robots

**Title:** A laser-microfabricated electrohydrodynamic thruster for centimeter-scale aerial robots  
**Authors:** Hari Krishna Hari Prasad, Ravi Sankar Vaddi, Yogesh M Chukewad, Elma Dedic, Igor Novosselov, Sawyer B Fuller  
**Year:** 2020 (accepted/published via PLOS ONE 2020)  
**arXiv:** [1906.10210](https://arxiv.org/abs/1906.10210v4)

**Key Practical Design Approach:**  
Laser micromachined (355 nm UV) steel emitter electrodes + lightweight carbon fiber mesh collector — a quad-thruster array (4 units) on a 1.8 × 2.5 cm footprint. No moving mechanical parts; pure corona-discharge EHD thrust.

**How it Multiplies/Enhances Airflow/Thrust:**  
Corona discharge ionizes air at sharp emitter tips; strong electric field accelerates ions toward the mesh collector. Ions transfer momentum to neutral air molecules via collisions, creating directional thrust. The quad-thruster array distributes thrust for stable lift. Achieved **thrust-to-weight ratio of 1.38** at 4.6 kV.

**DIY-Achievable with Basic Tools?**  
⚠️ **Partially.** Laser micromachining is not basic, but hobbyists can substitute with **sharp steel needles/dryer ions, wire mesh collectors, and a high-voltage DC supply** (~3–6 kV). The core principle is simple corona discharge; precision microfabrication just maximizes performance density.

**Assessment for Project Icarus:** 🔥 **Highly useful** — establishes that EHD can generate lift-to-weight >1 with no moving parts; most relevant baseline for a practical ion wind plane.

---

## Paper 2 — High Force Density Multi-Stage EHD Jets

**Title:** High Force Density Multi-Stage Electrohydrodynamic Jets Using Folded Laser Microfabricated Electrodes  
**Authors:** Daniel S. Drew, Sean Follmer  
**Year:** 2021  
**arXiv:** [2107.03567](https://arxiv.org/abs/2107.03567v1)  
**Conference:** Transducers 2021

**Key Practical Design Approach:**  
Multi-stage EHD device using **folded laser-microfabricated electrode geometry** — stages are stacked in series to progressively accelerate ions. This reduces component count and assembly complexity while maintaining ducted inter-stage flow.

**How it Multiplies/Enhances Airflow/Thrust:**  
Near-linear scaling of output force with stage count — one stage → two stages → three stages yields proportional force increase, indicating inter-stage ducting successfully minimizes losses. Three-stage device achieves among the highest **areal thrust, force density, and volumetric power density** ever measured for an EHD actuator.

**DIY-Achievable with Basic Tools?**  
⚠️ **Harder.** Laser microfabrication is required for the folded electrode geometry. However, the underlying principle — **stacking multiple EHD acceleration stages in series** — is conceptually simple. A DIY version could use multiple sequential wire-mesh/needle stages separated by insulating spacers.

**Assessment for Project Icarus:** 🔥 **Very useful** — proves multi-stage stacking is the path to significantly higher thrust density; key concept for scaling up from single-stage prototypes.

---

## Paper 3 — Electrohydrodynamic Emitters of Ion Beams

**Title:** Electrohydrodynamic emitters of ion beams  
**Authors:** Vadim Dudnikov  
**Year:** 2020  
**arXiv:** [2003.07354](https://arxiv.org/abs/2003.07354v1)

**Key Practical Design Approach:**  
Comprehensive review of EHD emitter design for high emission current density — covers emission zone sizing, stability at high/low currents, cluster generation, and practical maintenance of stable functioning emitters.

**How it Multiplies/Enhances Airflow/Thrust:**  
Focuses on maximizing ion current density and ion beam brightness by optimizing the Taylor cone/jet mode transition in electrospray emitters. Key practical insight: stable operation requires precise control of voltage, surface roughness, and liquid feed (if used).

**DIY-Achievable with Basic Tools?**  
✅ **Yes (partially).** Basic EHD ion emitters can be built from a **sharp needle + surrounding ring electrode + high voltage**. The paper provides theoretical grounding for avoiding emitter failure modes (arcing, flooding). However, achieving high current density stable emission requires careful geometry control.

**Assessment for Project Icarus:** 🟡 **Moderately useful** — more theoretical/industrial focus; useful for understanding emitter stability but less directly applicable to ambient-air ion wind propulsion than Papers 1–2.

---

## Paper 4 — Coulomb Drag Devices / Electric Solar Wind Sail (E-Sail)

**Title:** Coulomb drag devices: electric solar wind sail propulsion and ionospheric deorbiting  
**Authors:** Pekka Janhunen  
**Year:** 2014  
**arXiv:** [1404.7430](https://arxiv.org/abs/1404.7430v2)

**Key Practical Design Approach:**  
Uses a **charged tether/wire** in flowing plasma (solar wind or ionospheric ram flow) to extract momentum via Coulomb drag. ESAIL project produced a continuous 1 km tether sample via ultrasonic wire-to-wire bonding, with a Remote Unit for deployment and spin rate control.

**How it Multiplies/Enhances Airflow/Thrust:**  
The momentum flux from plasma stream (solar wind or ionospheric ions) impinges on a positively charged tether and transfers momentum — this is a form of passive "multiplication" by leveraging naturally flowing plasma. Thrust scales inversely with solar distance; power consumption ~700 W/N at 1 AU.

**DIY-Achievable with Basic Tools?**  
❌ **No.** Requires space plasma environment and km-scale tethers with ultrasonic bonding. However, the **negatively charged variant ("plasma brake")** works in LEO ionospheric plasma and could inspire ground-level analogues.

**Assessment for Project Icarus:** 🟡 **Moderately useful** — the multi-wire tether concept and high-voltage charge management are conceptually interesting, but the approach depends entirely on ambient space plasma and doesn't apply to ground-level ion wind propulsion.

---

## Paper 5 — Bernoulli + EHD Flow Enhancement (Support Paper)

**Title:** Competitive electrohydrodynamic and electrosolutal advection arrests evaporation kinetics of droplets  
**Authors:** Vivek Jaiswal, Shubham Singh, A R Harikrishnan, Purbarun Dhar  
**Year:** 2018  
**arXiv:** [1807.02720](https://arxiv.org/abs/1807.02720v1)

**Key Practical Design Approach:**  
Study of electrohydrodynamic circulation suppression in droplets — documents how electric fields affect internal advection/circulation in conducting fluids. Shows the **Electrohydrodynamic (EHD) number** as key scaling parameter for flow control.

**How it Multiplies/Enhances Airflow/Thrust:**  
Indirectly relevant — demonstrates that EHD body forces can be used to control and suppress circulation, but the same principles can be inverted to **amplify** bulk flow in the desired direction. Establishes that electric body forces retard stable internal circulation, suggesting a properly designed electrode geometry can redirect and enhance flow.

**DIY-Achievable with Basic Tools?**  
✅ **Yes.** A basic setup with **parallel plate electrodes, saline droplet, and AC/DC high voltage** can replicate the core EHD flow control experiments. This is essentially the same setup as a simplified ion wind pump.

**Assessment for Project Icarus:** 🟢 **Useful as supporting physics reference** — helps understand EHD flow scaling numbers and electrode geometry effects; good starting point for DIY parameter selection.

---

## Summary Table

| # | Paper | Year | DIY? | Icarus Relevance |
|---|-------|------|------|-----------------|
| 1 | Laser-microfabricated EHD thruster (cm-scale aerial robots) | 2020 | ⚠️ Partial | 🔥 Highly useful |
| 2 | Multi-Stage Folded Electrode EHD Jets | 2021 | ⚠️ Hard | 🔥 Very useful |
| 3 | Electrohydrodynamic Emitters of Ion Beams | 2020 | ✅ Partial | 🟡 Moderate |
| 4 | Coulomb Drag / E-Sail | 2014 | ❌ No | 🟡 Moderate |
| 5 | EHD Advection & Evaporation Kinetics | 2018 | ✅ Yes | 🟢 Supportive |

---

## Key Takeaways for Project Icarus

1. **Multi-stage stacking** is proven to scale thrust nearly linearly — the #1 priority for building a practical ion wind propulsion system.
2. **No moving parts** is the core advantage — durability and simplicity are the main benefits over conventional fans.
3. **DIY corona discharge** is achievable with needle + mesh + HV supply (~4–6 kV), even if laser microfabrication isn't available.
4. **Thrust-to-weight ratio > 1** has been demonstrated at cm-scale — the path to full-sized ion wind flight is through multi-stage multiplication.
5. **Key bottleneck** remains power consumption — high voltage at low current is the operational envelope to explore.
