"""
Emitter designs for Ion Wind Aircraft — REDESIGNED based on Integza/Plasma Channel research.

KEY INSIGHTS from Plasma Channel & Integza transcripts:
1. Emitter (positive electrode) = POINTY — razor blades create corona discharge → generates wind
2. Collector (negative/ground) = SMOOTH and ROUNDED — avoids sparks, doesn't generate wind alone
3. Gap: 11mm better than 9mm (Plasma Channel data)
4. Weight is critical — every gram counts at this scale
5. Razor blades work well as positive electrode
6. NEW: Peripheral acceleration design (hollow tube) — convergent approach

IMPORTANT SAFETY: 20-40 kV is lethal. Never power while handling exposed electrodes.
"""

from stl_utils import *
import os

# ── Design Parameters ────────────────────────────────────────────────────────
P = dict(
    # Collector (ground/negative) — SMOOTH rounded tube
    collector_outer_d=50.0,   # Outer diameter of collector tube (mm)
    collector_wall_t=0.5,      # Wall thickness for electroplating base
    collector_length=80.0,     # Total length of collector tube
    
    # Emitter (positive/HV) — POINTY sharp edges
    emitter_ring_d=46.0,      # Diameter of emitter ring (inside collector)
    blade_count=8,             # Number of razor blade points
    blade_thickness=0.3,       # Blade material thickness
    blade_projection=1.5,     # How far blade tip projects from ring
    
    # Gap (critical for corona discharge)
    gap=11.0,                 # Gap between emitter tip and collector wall (mm) — 11mm optimal
    
    # Frame / Housing
    housing_d=58.0,           # Outer housing diameter
    housing_length=90.0,      # Housing length
    wall_t=2.0,               # Housing wall thickness
    
    # Mounting
    flange_d=54.0,
    flange_t=3.0,
    mount_hole_d=3.0,
    mount_screw_d=2.5,
)


def collector_smooth_ring():
    """
    NEGATIVE electrode (ground) — smooth rounded metal surface.
    Based on Integza findings: round ring doesn't spark but doesn't produce wind alone.
    This is the OUTER tube in the peripheral acceleration design.
    We print in resin then electroplate with copper.
    """
    ro = P["collector_outer_d"] / 2
    wt = P["collector_wall_t"]
    L = P["collector_length"]
    
    tris = []
    # Outer smooth tube (collector)
    tris.extend(tube(0, 0, 0,
                    r_inner=ro - wt,
                    r_outer=ro,
                    h=L, axis='x', segments=48))
    
    # End caps with rounded edges (no sharp corners)
    # Front cap
    tris.extend(ring(ro - wt, ro, L, axis='x'))
    # Back cap
    tris.extend(ring(ro - wt, ro, 0, axis='x'))
    
    # Mounting flanges at each end
    fd = P["flange_d"] / 2
    ft = P["flange_t"]
    tris.extend(disc(0, 0, L, fd, ro, axis='x', segments=48))
    tris.extend(disc(0, 0, -ft, fd, ro, axis='x', segments=48))
    
    # Mounting holes in flanges
    for angle in [0, 90, 180, 270]:
        rad = np.radians(angle)
        for r_frac in [0.3, 0.7]:
            rr = r_frac * fd
            y = rr * np.cos(rad)
            z = rr * np.sin(rad)
            tris.extend(cylinder(L + ft/2, y, z, P["mount_screw_d"]/2, ft + 2, axis='x', segments=12))
    
    return np.array(tris, dtype=np.float32)


def emitter_razor_ring():
    """
    POSITIVE electrode (HV) — array of sharp points for corona discharge.
    Based on Plasma Channel: razor blades on trailing edge of airfoil.
    This is the INNER emitter in the peripheral acceleration design.
    Sharp points create the electric field concentration for ion generation.
    """
    outer_r = P["collector_outer_d"] / 2 - P["collector_wall_t"]
    inner_r = P["emitter_ring_d"] / 2
    L = P["collector_length"]
    blade_t = P["blade_thickness"]
    n_blades = P["blade_count"]
    blade_proj = P["blade_projection"]
    
    tris = []
    
    # Central support ring
    tris.extend(tube(0, 0, 0,
                    r_inner=inner_r - 2,
                    r_outer=inner_r,
                    h=L, axis='x', segments=32))
    
    # Emitter wire ring inside (thin wire for sharp corona)
    wire_r = inner_r - 1
    tris.extend(tube(0, 0, 0,
                    r_inner=wire_r - 0.3,
                    r_outer=wire_r,
                    h=L, axis='x', segments=32))
    
    # Razor blade tips projecting outward — these create corona
    # Each blade is a thin strip with a sharp outer edge
    gap = P["gap"]
    emitter_tip_r = outer_r - gap  # Where tips should end up
    
    for i in range(n_blades):
        angle = 2 * np.pi * i / n_blades
        # Each blade is a thin rectangular strip from inner ring to near outer ring
        y_center = emitter_tip_r * np.cos(angle)
        z_center = emitter_tip_r * np.sin(angle)
        
        # Blade body — thin strip
        blade_w = 2.0  # blade width
        blade_l = emitter_tip_r - inner_r + blade_proj
        
        tris.extend(cube(0, 
                         y_center - blade_w/2, 
                         z_center - blade_w/2,
                         blade_l, blade_w, blade_w))
    
    # End caps for emitter ring
    tris.extend(disc(0, 0, -1, inner_r + blade_proj, inner_r - 2, axis='x', segments=32))
    tris.extend(disc(0, 0, L + 1, inner_r + blade_proj, inner_r - 2, axis='x', segments=32))
    
    return np.array(tris, dtype=np.float32)


def peripheral_thruster_demo():
    """
    Complete peripheral acceleration thruster — DEMO VERSION.
    
    Design based on Plasma Channel's "hollow thruster with peripheral acceleration":
    - Ions are generated at pointy emitter tips (razor blades)
    - Air enters from SIDEs (periphery) not front
    - No sequential column acceleration — convergent approach
    - This avoids the diminishing returns problem seen in Mark I (40W → 2.1 → 3.2 → 4 m/s)
    
    Geometry:
    - Outer smooth tube = GROUND (collector) 
    - Inner sharp ring = HV positive (emitter)
    - Gap = 11mm (optimal from Plasma Channel's 9mm vs 11mm tests)
    """
    parts = []
    
    # Collector (outer, smooth, grounded)
    parts.append(collector_smooth_ring())
    
    # Emitter (inner, pointy, HV positive)
    emitter = emitter_razor_ring()
    parts.append(emitter)
    
    # Insulating spacers at ends (keep emitter centered)
    spacer_t = 2.0
    for x_pos in [-1, P["collector_length"] + 1]:
        tris = []
        outer_r = P["collector_outer_d"] / 2 - P["collector_wall_t"]
        inner_r = P["emitter_ring_d"] / 2
        tris.extend(tube(x_pos, 0, 0, r_inner=inner_r - 1, r_outer=inner_r + 2, h=4.0, axis='x', segments=32))
        parts.append(np.array(tris, dtype=np.float32))
    
    return merge(*parts) if parts else np.zeros((0,3,3), dtype=np.float32)


def razor_blade_array_demo():
    """
    Simpler demo: razor blade array for testing on bench.
    Based on Plasma Channel's trailing edge design.
    Single row of razor blades, aluminum foil collector on other side.
    """
    parts = []
    
    # Mounting rail
    rail_L = 100.0
    rail_h = 5.0
    rail_w = 4.0
    tris = []
    tris.extend(cube(0, 0, 0, rail_L, rail_w, rail_h))
    # Rail mounting holes
    for x in [10, 30, 50, 70, 90]:
        tris.extend(cylinder(x, rail_w/2, -1, P["mount_screw_d"]/2, rail_h + 2, axis='z', segments=8))
    parts.append(np.array(tris, dtype=np.float32))
    
    # Razor blades (positive/HV emitter) — alternating orientation
    blade_L = 30.0
    blade_h = 0.5
    n = 3
    spacing = rail_L / (n + 1)
    for i in range(n):
        x = (i + 1) * spacing
        # Blade pointing forward (toward collector)
        tris = cube(x - blade_L/2, 0, rail_h, blade_L, blade_h, blade_h)
        parts.append(translate(np.array(tris, dtype=np.float32), x=0, y=rail_w, z=0))
    
    # Aluminum foil collector plate (smooth, grounded)
    collector_t = 0.05  # foil
    collector_h = 40.0
    collector_L = 10.0
    collector_x = rail_L + 5  # gap from last blade
    tris = []
    tris.extend(cube(collector_x, 0, 0, collector_t, collector_h, collector_L))
    parts.append(translate(np.array(tris, dtype=np.float32), x=0, y=-collector_h/2 + rail_w/2, z=0))
    
    return merge(*parts) if parts else np.zeros((0,3,3), dtype=np.float32)


def housing_demo():
    """
    3D printed housing for demo thruster.
    Light resin body — can be electroplated for collector surface.
    """
    Do = P["housing_d"] / 2
    Di = P["collector_outer_d"] / 2 + 1  # clearance for collector
    L = P["housing_length"]
    wt = P["wall_t"]
    
    tris = []
    # Outer housing tube
    tris.extend(tube(0, 0, 0,
                    r_inner=Di,
                    r_outer=Do,
                    h=L, axis='x', segments=48))
    
    # End caps with mounting
    tris.extend(disc(0, 0, -wt, Do, Di, axis='x', segments=48))
    tris.extend(disc(0, 0, L, Do, Di, axis='x', segments=48))
    
    # Mounting flange rings
    fd = P["flange_d"] / 2
    ft = P["flange_t"]
    tris.extend(disc(0, 0, -wt - ft, fd, Do, axis='x', segments=48))
    tris.extend(disc(0, 0, L + wt, fd, Do, axis='x', segments=48))
    
    # Mounting holes
    for angle in [0, 60, 120, 180, 240, 300]:
        rad = np.radians(angle)
        y = fd * 0.7 * np.cos(rad)
        z = fd * 0.7 * np.sin(rad)
        tris.extend(cylinder(-wt - ft/2, y, z, P["mount_screw_d"]/2, ft + 2, axis='x', segments=8))
        tris.extend(cylinder(L + wt + ft/2, y, z, P["mount_screw_d"]/2, ft + 2, axis='x', segments=8))
    
    return np.array(tris, dtype=np.float32)


def generate_all(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    print("Emitter/Thruster parts (REDESIGNED):")
    write_stl(os.path.join(out_dir, "collector_smooth_ring.stl"), collector_smooth_ring())
    write_stl(os.path.join(out_dir, "emitter_razor_ring.stl"), emitter_razor_ring())
    write_stl(os.path.join(out_dir, "peripheral_thruster_demo.stl"), peripheral_thruster_demo())
    write_stl(os.path.join(out_dir, "razor_blade_array_demo.stl"), razor_blade_array_demo())
    write_stl(os.path.join(out_dir, "thruster_housing_demo.stl"), housing_demo())
    print(f"  collector_smooth_ring.stl — smooth tube for electroplating")
    print(f"  emitter_razor_ring.stl — sharp points for corona discharge")
    print(f"  peripheral_thruster_demo.stl — complete demo unit")
    print(f"  razor_blade_array_demo.stl — simple bench test version")
    print(f"  thruster_housing_demo.stl — 3D printable housing")


if __name__ == "__main__":
    generate_all(os.path.dirname(__file__))
