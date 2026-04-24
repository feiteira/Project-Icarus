"""
Collector designs for Ion Wind Aircraft — REDESIGNED based on Integza/Plasma Channel research.

KEY INSIGHTS:
1. Collector (ground/negative) = SMOOTH and ROUNDED — avoids sparks
2. NOT a flat plate — a smooth tube/ring that doesn't create corona
3. The CORONA (and thus wind) comes from the POINTY positive electrode only
4. Collector just needs to be conductive and smooth

This file is now simpler — the collector is the smooth outer tube (in emitters.py).
These parts are for MOUNTING and INTEGRATION.
"""

from stl_utils import *
import os

P = dict(
    # Wing integration
    wing_chord=60.0,           # Wing chord in mm (for our 300mm span test wing)
    wing_section_L=120.0,      # Length of test wing section
    frame_L=100.0,
    
    # Collector foil (for simple flat-plate version)
    foil_t=0.05,               # Aluminum foil thickness
    foil_h=40.0,               # Foil height
    foil_L=15.0,               # Foil length
    
    # Mounting
    mount_screw_d=2.5,
    tab_w=10.0,
    tab_t=2.0,
)


def collector_foil_mount():
    """
    Simple flat foil collector for basic bench tests.
    Aluminum foil tape on smooth 3D printed surface.
    This is the GROUND electrode — smooth, no points.
    """
    foil_h = P["foil_h"]
    foil_L = P["foil_L"]
    foil_t = P["foil_t"]
    
    tris = []
    # 3D printed base (smooth surface for foil)
    base_t = 1.5
    tris.extend(cube(0, 0, 0, foil_t + base_t, foil_h, foil_L))
    
    # Aluminum foil on top (conductive surface)
    tris.extend(cube(foil_t + base_t, 0, 0, foil_t, foil_h, foil_L))
    
    # Mounting tabs
    tab_w = P["tab_w"]
    tab_t = P["tab_t"]
    for z_pos in [5, foil_L - 5]:
        tris.extend(cube(-tab_t, foil_h/2 - tab_w/2, z_pos, tab_t, tab_w, tab_w))
        # Screw holes
        tris.extend(cylinder(-tab_t/2, foil_h/2, z_pos + tab_w/2, P["mount_screw_d"]/2, tab_t + 2, axis='x', segments=8))
    
    return np.array(tris, dtype=np.float32)


def wing_integration_frame():
    """
    Frame for integrating ionic thrust into a wing section.
    Based on Plasma Channel's approach: aluminum foil on leading edge (collector),
    razor blades on trailing edge (emitter).
    """
    chord = P["wing_chord"]
    L = P["wing_section_L"]
    
    tris = []
    
    # Main spar/frame
    spar_h = 8.0
    spar_t = 3.0
    tris.extend(cube(0, chord/2 - spar_h, 0, L, spar_h, spar_t))  # top spar
    tris.extend(cube(0, chord/2 - spar_h - 2, 0, L, spar_t, spar_t))  # bottom spar
    
    # Leading edge collector strip (smooth aluminum tape — ground)
    le_t = 0.1
    le_h = chord * 0.3  # 30% chord
    tris.extend(cube(0, chord/2 - le_h, 0, L, le_h, le_t))  # aluminum foil tape
    
    # Trailing edge emitter zone (razor blades — HV positive)
    te_t = 0.5
    te_h = chord * 0.2
    te_z_start = L - 15.0  # last 15mm is trailing edge
    tris.extend(cube(te_z_start, chord/2 - te_h, 0, 15, te_h, te_t))
    
    # Mounting rails for test
    rail_L = 20.0
    for x_pos in [L/4, 3*L/4]:
        tris.extend(cube(x_pos - rail_L/2, chord/2 - spar_h - 10, 0, rail_L, 3, 3))
    
    return np.array(tris, dtype=np.float32)


def test_rig_mount():
    """
    Mount for attaching thruster to a balance/measurement rig.
    Based on Plasma Channel's balance point armature.
    """
    tris = []
    
    # Central pivot block
    block_w = 30.0
    block_h = 20.0
    block_L = 40.0
    tris.extend(cube(0, -block_w/2, -block_h/2, block_L, block_w, block_h))
    
    # Pivot bearing hole
    tris.extend(cylinder(block_L/2, 0, 0, 5, block_L + 4, axis='x', segments=16))
    
    # Thruster mounting plate (top)
    mount_w = 40.0
    mount_h = 3.0
    tris.extend(cube(-mount_w/2, -mount_w/2, block_h/2, mount_w, mount_w, mount_h))
    
    # Screw holes for thruster
    for y_off in [-12, 12]:
        for z_off in [-12, 12]:
            tris.extend(cylinder(0, y_off, block_h/2 + z_off, P["mount_screw_d"]/2, mount_h + 2, axis='z', segments=8))
    
    return np.array(tris, dtype=np.float32)


def electroplate_base_collector():
    """
    Lightweight collector part designed for electroplating.
    3D print in resin, then electroplate with copper.
    Based on Integza's electroplating process (copper sulfate + 1 amp max).
    
    Design: Hollow tube with smooth inner surface.
    """
    outer_d = 48.0
    wall_t = 1.0
    L = 80.0
    
    outer_r = outer_d / 2
    inner_r = outer_r - wall_t
    
    tris = []
    # Outer tube
    tris.extend(tube(0, 0, 0, r_inner=inner_r, r_outer=outer_r, h=L, axis='x', segments=48))
    # End caps (smooth discs)
    tris.extend(disc(0, 0, 0, inner_r + 0.1, outer_r, axis='x', segments=48))
    tris.extend(disc(0, 0, L, inner_r + 0.1, outer_r, axis='x', segments=48))
    
    # Flanges for mounting
    flange_d = 54.0
    flange_t = 2.0
    tris.extend(disc(0, 0, -flange_t, flange_d/2, outer_r, axis='x', segments=48))
    tris.extend(disc(0, 0, L, flange_d/2, outer_r, axis='x', segments=48))
    
    return np.array(tris, dtype=np.float32)


def generate_all(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    print("Collector parts (REDESIGNED):")
    write_stl(os.path.join(out_dir, "collector_foil_mount.stl"), collector_foil_mount())
    write_stl(os.path.join(out_dir, "wing_integration_frame.stl"), wing_integration_frame())
    write_stl(os.path.join(out_dir, "test_rig_mount.stl"), test_rig_mount())
    write_stl(os.path.join(out_dir, "electroplated_collector.stl"), electroplate_base_collector())
    print(f"  collector_foil_mount.stl — simple bench test collector")
    print(f"  wing_integration_frame.stl — wing section with LE collector, TE emitter")
    print(f"  test_rig_mount.stl — balance rig attachment")
    print(f"  electroplated_collector.stl — light tube for copper electroplating")


if __name__ == "__main__":
    generate_all(os.path.dirname(__file__))
