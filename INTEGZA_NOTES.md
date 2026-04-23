# Integza / Joel — Research Notes

## Channel Info
- **YouTube Channel:** Integza
- **Video 1 (reference):** "I built an IONIC PLASMA THRUSTER (Best Design)"
  - URL: https://www.youtube.com/watch?v=mnCmvxt2jn8
- **Video 2 (from Carlos):** "Designing A Self Propelling Ionic Thrust Wing"
  - URL: https://www.youtube.com/watch?v=5lDSSgHG4q0

## Key Technical Insights from Transcript (Video 1)

### Electrode Design
- **Cathode (emitter):** Pointy/spiky — creates corona discharge → generates wind
- **Anode (collector):** Smooth, round surface — avoids sparks, does NOT generate wind alone
- Best design = COMBINES both: tube with round edges but internal emitter wire

### Ion Wind Principle
- Electrons shoot from one place to another
- Electrons collide with air molecules, projecting them in one direction
- Corona discharge generates wind; spark/arc discharge does NOT

### Thruster Design
- Cable and tube: electrons push air into tube, generating focused airflow
- Problem: flyback transformer is heavy (epoxy resin protection)
- Lighter alternative: plasma lighter (but doesn't produce enough voltage)

### Electroplating Optimization
- 3D print lightweight resin part → electroplate with thin copper layer
- Makes conductive, light part for anode collector
- Electroplating: copper sulfate + 1 amp max current + swirl

### Test Results (Video 1)
- Single module: ~40cm thrust distance, powered candle easily
- Added to boat: "slowly but steadily" worked
- Multiple modules = more thrust

## Contact / Outreach
- **Status:** NOT contacted yet
- **Next step:** Carlos will provide more transcripts, then decide on outreach approach
- **Do NOT contact yet** — waiting for Carlos's instructions

## Relevance to Project Icarus
- Directly applicable electrode geometry (pointy cathode, smooth anode)
- Lightweight 3D-printed + electroplated collector design
- Demonstrates practical thrust from ion wind at small scale

---

## Plasma Channel Video (Transatlantic Collaboration with Joel) — Video ID: 5lDSSgHG4q0
**Channel:** Plasma Channel (Integza?)
**Collaboration:** Plasma Channel + American Joel (competitive iterative design)
**Goal:** Ionic thrust wing — both wing AND thruster in one

### Key Technical Data

**Test Setup:**
- 12 CM section of wing tested
- 4 mini airfoils on top
- Leading edges: aluminum foil tape (electrical ground/collector)
- Trailing edge: razor blades (high voltage positive/emitter)
- Stun gun modules: 30,000 volts
- Spacings tested: 9mm, 11mm, 13mm

**Velocity Results:**
- 9mm gap: 0.4 m/s (weak)
- 11mm gap: 0.5 m/s (better)
- Parallel vs series wiring tested

**Weight Reduction Journey:**
- Initial airfoil: 100g
- After plastic removal + thin sheeting: 45g (55% reduction)
- Ionic segment (razor blades): 15g → 10g with thinner serrated blades
- Total prototype: 100g (50% total weight reduction)

**Dry Ice Test Results:**
- Wing glows eerie Corona purple when powered
- Air clearly drawn over leading edge (fog display)
- Time exposures show complete corona effect

**Rotating Test Rig:**
- Balance point armature with power source + HV modules
- Freely moving from ground for testing
- Result: just under 60 RPM = 2 m/s (circumference 2m)
- **"Not quite fast enough to fly but only a 12 CM section"**

### Key Design Insights

1. **Glider wings are ideal platform:** huge, designed for slow speed lift, low wing loading, high aspect ratio
2. **Integrate thrusters INTO wings** — minimize weight and components
3. **Weight is critical** — ionic thrust is weak, so every gram matters
4. **Closer spacing better for power** — 11mm > 9mm in their tests
5. **Glider-format:** slow moving, big airfoil, very low wing loading, very large wings, high aspect ratio

### Expert Input: Peter SLE (Glider Expert)
- Has built and flown planes for a decade
- Met at Open Sauce in San Francisco
- Advice: glider format, very low wing loading, huge aspect ratio, very large slender wings

### Joel (American Collaborator)
- Friend and fellow creator
- Designed his own ionic thruster that outperformed Plasma Channel's first design
- Joel's second design: "brilliantly simple and compact"
- This is a TRANSATLANTIC collaboration — Portugal ←→ USA

### Scaling Up
- A 12 CM section gave 2 m/s
- Full wing would need significant more thrust
- MIT paper used 5m wingspan at 2.5kg and ~600W for ~1N thrust
- At 300mm, we need to be much more efficient

---

## Raw Transcript Snippets (Video 1 - Plasma Channel)

### Joel's involvement
"my friend and fellow Creator Joel designed his own ionic Thruster one which worked really well and quite frankly outperformed mine"

"American Joel responded with a second design of his own one that was brilliantly simple and compact"

### Key quote on approach
"for the better part of a year I've been trying to optimize an ionic Thruster for flight"

"we need to minimize weight and components not the other way around"

"maybe the best way to do that is to incorporate ionic thrusters into the wings themselves"

### Design specs tested
- 12 CM wing section
- 4 mini airfoils
- Aluminum foil tape (ground/collector) on leading edges
- Razor blades (HV positive/emitter) on trailing edge  
- Stun gun modules: 30,000 volts
- Gap distances: 9mm, 11mm, 13mm

### Weight data
- Initial airfoil: 100g
- After optimization: 45g (55% reduction)
- Ionic segment: 10g
- Total prototype: 100g (50% total reduction)

### Results
- 9mm gap: 0.4 m/s
- 11mm gap: 0.5 m/s
- Full rotating test: 60 RPM = 2 m/s
- "Not quite fast enough to fly but this is only a 12 CM section"

### Peter SLE (glider expert) advice
"it has to be a glider format right like it has to be a slow moving Big Air foil very slow moving air foil but it's also going to be very low Wing loading but it's going to have a huge aspect ratio so very very large wings large slender wings"

---

## Transcript Part 3 (Open Sauce, Mark I, Diminishing Returns)

### Key Quote
"ionic thrust is quickly emerging as a viable form of propulsion"
"MIT launched an ionic thrust airplane in 2018"
"We're all rushing towards an ionic thrust airplane of commercial design"

### Plasma Channel's Journey
- BSI Thruster (rough prototype): 2.3 m/s max output
- Mark I: 4x the volume of air at just under 4 m/s
- Sequential design limitation: same column of air accelerated over and over → diminishing returns

### Diminishing Returns Problem (Mark I)
- Stage 1: 40W → 2.1 m/s
- Stage 2: +40W → only 25% gain (3.2 m/s) 
- Stage 3: +40W → 4 m/s (only 25% more)

### Nature Inspiration
- Leaves use convergence with veins (sugar accumulation)
- Waves: constructive interference
- Key insight: CONVERGENT approach — no column of air accelerated twice
- Result: NEW type of ionic thruster — HOLLOW, relies on PERIPHERAL acceleration

### Open Sauce Connection
- Plasma Channel attended Open Sauce, brought his builds
- "Swamped with thousands of people wanting to see the Thruster in person"
- Going again this year (2026?)
- At Open Sauce met Peter SLE (glider expert)

### Previous Designs
- BSI Thruster: Max output 2.3 m/s
- Mark I: 4x volume, just under 4 m/s
- Both used sequential acceleration

### Problem Areas Identified
1. Method of acceleration (sequential = diminishing returns)
2. Structural integrity (positive electrode = super fragile wire)
3. Obstacle collision avoidance

