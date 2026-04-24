# Thrust Stand Construction Guide — English Summary

## What is this guide?

A step-by-step manual for building a minimum viable DIY ion wind thrust stand for ~€64. Designed for beginners with basic electronics knowledge — no prior experience with high voltage or corona discharge required.

## What you'll need (minimum viable)

- ZVS Flyback Module (5-12V input, 20-50kV output) — €10
- Arduino Nano Every — €10
- Thin wire (0.1mm stainless steel or tungsten) for emitter — €6
- Copper or aluminum foil for collector — €5
- Acrylic sheet for structure — €10
- M3 threaded rods and nuts — €5
- 18650 battery holder + 2× batteries — €8
- HV resistive divider (10MΩ + 1MΩ resistors) — €1
- Multimeter (you already have one)

Total: ~€64 without load cell.

## What the guide covers

**Safety first** — HV at 20-50kV is dangerous. The guide explains risks and precautions in plain language.

**Component identification** — Each component is explained with photos descriptions (what it looks like, what it does, typical wire colors).

**Assembly in 4 phases:**
1. HV Generator (ZVS Flyback) — wiring, testing, troubleshooting
2. Electrode assembly — emitter wire tensioning, collector foil mounting, gap setting to 25mm
3. Thrust measurement (pendulum method) — calibration with known weights, deflection-to-thrust conversion
4. Arduino data logging — basic voltage readout, optional load cell integration

**First test procedure** — How to distinguish good corona (purple glow, ozone smell) from bad arcing (sparks, crackling).

**Troubleshooting table** — 10 common problems with causes and solutions.

## Key design choices explained

- **25mm gap** — safe zone between arcing (too small) and weak thrust (too large)
- **Pendulum method** — no load cell needed, just string + pivot + known calibration weights
- **Stainless steel 0.1mm wire** — cheap and effective emitter material
- **Smooth collector** — must be LISE with no sharp edges, or arcing occurs

## What you'll learn

The thrust stand validates whether our ion wind electrode design actually produces thrust — and in what amount (mN). This calibrates the simulator (the K constant mystery) and tells us whether Project Icarus is physically viable before we spend months designing the airframe.

---

*Full guide in European Portuguese at: THRUST_STAND_GUIDE_PT.md*
*Project Icarus — Clawdia01 — April 2026*
