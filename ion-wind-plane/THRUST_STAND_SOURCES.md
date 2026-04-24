# Thrust Stand — Sourcing List (Germany/Darmstadt)

> Budget: ~€200-300 | Compiled: 2026-04-24

---

## Required Components

### 1. HV Generator (DC-DC Step-Up)
Generates 20–50 kV from 5–12V input. Powers the corona discharge.

| Option | Shop | Product | Price |
|--------|------|---------|-------|
| **ZVS Flyback Module** (recommended — same as WPI 2024 used) | reichelt.de | ZVS Low Voltage Triggered Flyback Driver Module (search: "ZVS Flyback" or "ZVS Treiber") | ~€8–15 |
| Alternative: MW KM-10-12 | reichelt.de | HV generator module 10kV | ~€20–30 |
| DIY alternative: Flyback from old monitor + ZVS driver | Pollin.de | Gebrauchtes Flyback-Transformator (refurb) | ~€5–10 |

> **Carlos note:** The ZVS flyback approach is exactly what the WPI 2024 paper used. Most reliable.

---

### 2. Data Logger — Arduino Nano
Reads voltage, current, and load cell. Logs to serial.

| Shop | Product | Price |
|------|---------|-------|
| reichelt.de | Arduino Nano Every (ATmega4809) — ARD NANO EVERY | ~€8–12 |
| reichelt.de | Arduino Nano R4 (RA4M1, 32-bit) | ~€15–18 |

**Recommended:** Arduino Nano Every — sufficient, well-documented, 5V logic.

---

### 3. Load Cell + HX711 Amplifier
Measures thrust directly. 24-bit ADC, 80 Hz update rate.

| Shop | Product | Price |
|------|---------|-------|
| reichelt.de | FREI HX711 module (ARD SEN HX711) | ~€3–5 |
| reichelt.de | JOY-IT Balance 5 kg module (with HX711) | ~€8–12 |
| Amazon.de | HX711 + 1kg load cell combo (search: "HX711 Wägezelle 1kg") | ~€6–10 |

**Recommended for thrust stand:** JOY-IT 5 kg module — pre-calibrated, easy to mount.

---

### 4. Precision Scale (Manual Readout)
For calibrating the load cell and weighing components.

| Shop | Product | Price |
|------|---------|-------|
| Amazon.de | Kern PCB / Precision balance 200g × 0.01g | ~€40–80 |
| reichelt.de | JOY-IT Scale 40 kg (for larger measurements) | ~€15–25 |
| Conrad | Digital precision scale 200g/0.01g (Kern or similar) | ~€35–60 |

**Minimum viable:** A kitchen scale with 1g resolution + manual thrust measurement (pendulum method from Polk 2017) = €0

---

### 5. HV Voltage Probe / Meter
Measures output voltage to monitor arcing.

| Shop | Product | Price |
|------|---------|-------|
| Amazon.de | HV Probe 40kV DC (multimeter attachment) | ~€15–25 |
| Conrad | Digital Multimeter with HV probe capability | ~€30–60 |
| DIY | Resistive divider (10MΩ + 1MΩ) + multimeter | ~€5 (resistors) |

**Recommended:** Simple resistive divider + multimeter (most DIY approach, ~€5).

---

### 6. Electrode Materials

**Emitter wire (thin tungsten or stainless steel):**
| Shop | Product | Price |
|------|---------|-------|
| Amazon.de | Tungsten wire 0.1mm × 1m (WIG/Stick welding) | ~€8–15 |
| eBay.de | Stainless steel wire 0.1mm × 10m (kitchen/industrial) | ~€5–8 |
| Pollin.de | Copper wire various gauges | ~€2–5 |

**Collector foil:**
| Shop | Product | Price |
|------|---------|-------|
| Amazon.de | Copper foil 0.05mm × 100mm × 5m (self-adhesive) | ~€10–15 |
| Pollin.de | Aluminum foil (kitchen grade) | ~€3–5 |

**Recommended:** Stainless steel emitter wire (0.1–0.2mm) + copper foil collector.

---

### 7. Insulating Materials
Mounts and spacers for electrode assembly.

| Shop | Product | Price |
|------|---------|-------|
| Amazon.de | Acrylic sheet 3mm, 200×300mm (Plexiglas) | ~€8–12 |
| OBI / Bauhaus | Polycarbonate sheet 3mm | ~€10–15 |
| Amazon.de | M3 threaded rods × 100mm (10pcs) | ~€5–8 |
| Amazon.de | M3 standoff set (nylon) | ~€6–10 |

---

### 8. Power Supply

| Shop | Product | Price |
|------|---------|-------|
| reichelt.de | Labornetzteil 5V/12V, 3A (e.g., Mean Well or similar) | ~€20–35 |
| Amazon.de | 18650 Battery holder + 2× 18650 + protection circuit | ~€10–15 |
| Mean Well RS-15-5 | 5V 3A from reichelt | ~€12–18 |

**Minimum viable:** 2× 18650 in series (7.4V) + holder = ~€8 (if you already have 18650 cells).

---

## Optional Components

| Component | Why Optional | Price |
|-----------|-------------|-------|
| ZVS driver upgrade | Basic flyback works but ZVS is more efficient | €8–15 |
| Current sensor (ACS712) | Can estimate power without direct measurement | €3–5 |
| OLED display (I2C) | For standalone display without PC | €5–8 |
| Additional load cells | For measuring different thrust ranges | €5–15 |

---

## Budget Summary

### Minimum Viable (pendulum method, no load cell):
| Item | Est. Cost |
|------|-----------|
| ZVS Flyback Module | €10 |
| Arduino Nano Every | €10 |
| HV resistive divider + multimeter (reuse) | €5 |
| Emitter wire (stainless steel) | €6 |
| Copper/aluminum foil | €5 |
| Acrylic sheet | €10 |
| M3 rods/standoffs | €8 |
| 18650 holder + batteries | €10 |
| **TOTAL** | **~€64** |

### Recommended Full Setup (with load cell):
| Item | Est. Cost |
|------|-----------|
| ZVS Flyback Module | €12 |
| Arduino Nano Every | €10 |
| HX711 + 5kg load cell | €12 |
| Precision scale (or use kitchen scale) | €0–40 |
| HV divider + resistors | €5 |
| Emitter wire | €8 |
| Copper foil | €12 |
| Acrylic sheet | €12 |
| M3 hardware | €10 |
| Lab power supply / 18650 | €15 |
| **TOTAL** | **~€96–140** |

### Full Featured (with all optionals):
| Item | Est. Cost |
|------|-----------|
| Everything above + | |
| ZVS driver upgrade | €15 |
| Current sensor | €5 |
| OLED display | €6 |
| **TOTAL** | **~€160–200** |

---

## Suppliers (that ship to Darmstadt)

1. **reichelt.de** — Best for Arduino, HX711, electronics components. Ships DE €5.90 shipping.
2. **Conrad.de** — Good for lab equipment, power supplies, precision scales. Ships DE €5.99.
3. **Pollin.de** — Cheap components, refurb items. Ships DE €4.95.
4. **Amazon.de** — Fast delivery, good for consumables (wire, foil). Prime = free shipping.
5. **eBay.de** — For wire, foil, used flyback transformers from German sellers.

---

## Key Notes for Carlos

1. **Start with minimum viable** — you can validate thrust with just the flyback + Arduino + pendulum (Polk 2017 method), before buying load cell.
2. **ZVS flyback is the same architecture** as the WPI 2024 project used — most documented DIY approach.
3. **Emitter wire diameter matters** — use 0.1–0.2mm tungsten or stainless steel. Thinner = lower arcing threshold.
4. **Collector should be smooth** (rounded) and copper or aluminum. The literature says no sharp edges on collector.
5. **Gap 25–40mm** between emitter and collector to avoid arcing at 20–40kV.
