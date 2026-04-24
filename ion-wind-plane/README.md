# Ion Wind Aircraft — 3D Model Files

Parametric STL generator for an electrohydrodynamic (ion wind) thrust aircraft,
designed for Bambu Lab X1C/P1P 3D printing.

## Quick Start

```bash
# Generate (or regenerate) all STL files
python3 generate_all.py

# Generate a specific subsystem
python3 generate_all.py --fuselage
python3 generate_all.py --emitters
python3 generate_all.py --collectors
python3 generate_all.py --frame
python3 generate_all.py --guards
```

## Project Structure

```
ion-wind-plane/
├── generate_all.py     # Master generator — run this to produce all STLs
├── stl_utils.py        # Shared mesh library (pure numpy, no CAD deps)
├── fuselage/           # Fuselage & electronics enclosure
├── emitters/           # Emitter wire supports & tensioners
├── collectors/          # Collector plate mounts & adjusters
├── frame/              # Main structural spine
└── guards/             # Propeller guard / duct
```

## Generated STL Files

| File | Description | Tris |
|------|-------------|------|
| **fuselage/fuselage_shell.stl** | Hollow box fuselage (180×80×50mm) | 72 |
| **fuselage/battery_bay.stl** | 4× 18650 cell holder tray | 624 |
| **fuselage/hv_module_bay.stl** | HV multiplier module mount bay | 276 |
| **fuselage/lid.stl** | Snap-fit removable lid | 60 |
| **fuselage/internal_ribs.stl** | Lightweight honeycomb ribs | 144 |
| **emitters/emitter_frame.stl** | Wire frame (80×60×10mm) | 352 |
| **emitters/wire_support_post.stl** | Single wire support post | 168 |
| **emitters/wire_support_array.stl** | All posts for 200mm span | 1512 |
| **emitters/tension_adjuster.stl** | Spring-loaded wire tensioner | 412 |
| **emitters/insulator_spacer.stl** | HV insulator plate | 60 |
| **emitters/emitter_assembly.stl** | Complete emitter row | 3040 |
| **collectors/collector_plate.stl** | Single flat collector plate | 60 |
| **collectors/collector_foil_array.stl** | 8-fin parallel foil array | 96 |
| **collectors/collector_mount_frame.stl** | Collector frame | 336 |
| **collectors/collector_with_frame.stl** | Plate + frame assembly | 396 |
| **collectors/adjustable_mount.stl** | Gap-tuning slide mount | 316 |
| **collectors/streamer_suppressor.stl** | Corona suppressor fins | 48 |
| **frame/spine_segment.stl** | Single spine node (30mm) | 240 |
| **frame/node_junction.stl** | Junction connector | 296 |
| **frame/wing_mount_plate.stl** | Wing attachment bracket | 252 |
| **frame/tail_fin_mount.stl** | Rear stabilizer mount | 120 |
| **frame/spine_assembly.stl** | Full 240mm spine | 3992 |
| **frame/spine_end_cap.stl** | Cable channel end cap | 72 |
| **guards/duct_ring.stl** | Hollow cylindrical duct | 624 |
| **guards/duct_with_struts.stl** | Duct with structural struts | 456 |
| **guards/wire_guard_mesh.stl** | Wire-frame prop guard | 576 |

## Design Parameters

All dimensions are in **mm**. Key physics values:

| Parameter | Value |
|-----------|-------|
| Emitter-collector gap | 25 mm (adjustable) |
| HV requirement | 20–40 kV |
| Emitter wire diameter | 0.5 mm (tungsten) |
| Collector plate width | 30 mm |
| Typical thrust | ~1–5 g/N (very low!) |

### Fuselage (180×80×50mm)
- 2mm wall thickness, hollow shell
- Battery bay: up to 4× 18650 cells (18×65mm)
- HV module bay in nose section

### Emitter Assembly
- Wire span: 200mm (fits in 256mm build volume)
- Support post spacing: 25mm (9 posts)
- Spring-loaded tension adjuster at each end
- Insulating spacer between HV and grounded parts

### Collector Assembly
- Flat plate collectors (30×50×1.5mm)
- 8-fin foil array option (5mm spacing)
- Height-adjustable mount for gap tuning
- Streamer suppressor fins to prevent arcing

### Frame Spine (240mm total)
- 8 spine segments × 30mm
- 7 junction nodes
- Low-profile (30×18mm cross-section) for minimal drag
- Internal cable routing channel
- Wing mount plates at intervals

## Slicer Settings for Bambu Lab

### PLA (recommended for prototype)
- Layer height: 0.2mm
- Infill: 15–20% (gyroid or honeycomb for weight reduction)
- Walls: 3 perimeters minimum
- Supports: tree supports for overhangs > 60°
- Nozzle temp: 210°C / Bed temp: 60°C

### PETG (for HV components)
- Layer height: 0.2mm
- Infill: 20%
- Walls: 4 perimeters
- Dry filament before printing!

### Key Print Considerations
- **emitter_assembly.stl** (3040 tris) — large assembly, may need 0.5mm layer
- **spine_assembly.stl** (3992 tris) — split if needed for older printers
- All parts fit within 256×256×256mm build volume
- Snap-fit joints: print with 0.2mm clearance
- Use variable layer height for faster printing of large flat parts

## Assembly Notes

### High Voltage Safety
⚠️ **DANGER**: This project involves 20–40 kV. Proper insulation and safety measures are essential:
- All plastic parts should be rated for HV use
- Minimum 25mm clearance between emitter and collector
- Use silicone oil or parylene coating for high-stress HV areas
- Never touch the apparatus while powered

### Mechanical Assembly
1. Print all parts in PLA or PETG
2. Insert battery holder into fuselage shell
3. Mount HV module in hv_module_bay
4. Snap lid onto fuselage
5. Attach spine to fuselage with M3 screws
6. Mount emitter and collector assemblies on spine
7. Thread tungsten wire through support posts
8. Adjust tension until wire is taut
9. Mount wing mount plates at desired positions

### Recommended Hardware
- M3×8mm socket head screws (for spine joints)
- M2×6mm screws (for electronics mounting)
- 18650 LiPo battery (3.7V × 4 in series for HV module)
- Cockcroft-Walton voltage multiplier (or ready-made HV module)
- Tungsten wire 0.5mm (emitter) / Copper foil 0.5mm (collector)

## Modifying Parameters

Edit the `P` dict in each `.py` file to change dimensions:

```python
# Example: change fuselage size
# Edit fuselage/fuselage.py:
P = dict(L=220.0, W=100.0, H=60.0, ...)

# Example: change wire span
# Edit emitters/emitters.py:
P = dict(wire_span=250.0, ...)
```

Then re-run `python3 generate_all.py` to regenerate all STLs.

## Physics Reference

Based on MIT ion wind aircraft research:
- Thrust ≈ 2.5 N / kW (iona thrust density ~4 N/m² at 30 kV/cm)
- Ionic wind velocity ~10 m/s for typical wire-to-plate geometries
- Electrode sharp radius → low onset voltage (~10 kV for 0.5mm wire)
- Collector roughness must be < 10µm to avoid corona suppression

## License

Open hardware — use for educational purposes. No warranty provided.