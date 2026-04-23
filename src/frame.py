"""
Main Frame / Spine for Ion Wind Aircraft
Lightweight structural spine connecting fuselage, wings, and ion array.
Honeycomb topology for minimal weight. Fits 256mm build volume.
"""

from stl_utils import *
import os

P = dict(
    spine_L=240.0,
    spine_W=30.0,
    spine_H=18.0,
    wall_t=2.0,
    node_spacing=30.0,
    node_r=7.0,
    wing_mount_w=20.0,
    wing_mount_t=3.0,
    fin_mount_h=12.0,
    fin_mount_t=3.0,
    snap_w=4.0, snap_h=2.0, snap_d=3.0,
)


def spine_segment(length=None):
    """Single spine segment with semi-hollow interior and cable channel."""
    sp = P["node_spacing"]
    L = length or sp
    W, H, T = P["spine_W"], P["spine_H"], P["wall_t"]

    tris = []
    tris.extend(cube(0, 0, 0, L, W, H))

    rd = T * 3
    tris.extend(cube(0, 0, 0, rd, W, H))          # left end cap
    tris.extend(cube(L - rd, 0, 0, rd, W, H))    # right end cap
    tris.extend(cube(rd, T, 0, L - 2*rd, W - 2*T, T))      # bottom skin
    tris.extend(cube(rd, T, H - T, L - 2*rd, W - 2*T, T))  # top skin
    tris.extend(cube(rd, 0, T, L - 2*rd, T, H - 2*T))     # front wall
    tris.extend(cube(rd, W - T, T, L - 2*rd, T, H - 2*T)) # back wall

    ch_h = H * 0.3
    tris.extend(cube(rd, T, (H - ch_h)/2, L - 2*rd, W - 2*T, T))  # cable channel floor

    for bx in [L*0.2, L*0.5, L*0.8]:
        tris.extend(cylinder(bx, W/2, H/2, 4.0, H*0.4, axis='y', segments=12))

    return np.array(tris, dtype=np.float32)


def node_junction():
    """Junction node connecting spine segments and wing mounts."""
    r, W, H = P["node_r"], P["spine_W"], P["spine_H"]

    tris = []
    tris.extend(cylinder(0, W/2, H/2, r, H*0.6, axis='x', segments=24))

    fw, ft = 15.0, 2.5
    for dy in [-fw/2, W/2 - fw/2]:
        tris.extend(cube(-ft, dy, H/2 - fw/2, ft*2, fw, fw))

    for angle in [0, 90, 180, 270]:
        rad = np.radians(angle)
        hy = W/2 + (W/2 - 5) * np.sin(rad)
        hz = H/2 + (H/2 - 5) * np.cos(rad)
        tris.extend(cylinder(r * 0.8, hy, hz, 1.5, 10, axis='x', segments=8))

    tris.extend(cylinder(-2, W/2, H*0.6, 3.0, 5.0, axis='x', segments=12))
    return np.array(tris, dtype=np.float32)


def wing_mount_plate():
    """Wing mounting plate that bolts to the spine."""
    W, H, mw, mt = P["spine_W"], P["spine_H"], P["wing_mount_w"], P["wing_mount_t"]
    sw, sh, sd = P["snap_w"], P["snap_h"], P["snap_d"]

    tris = []
    tris.extend(cube(0, -5, 0, mt, mw + 10, H))
    tris.extend(cube(0, 0, H*0.7, mt + 3, 3, H - H*0.7))
    for yo in [-mw/2, mw/2]:
        tris.extend(cube(mt, yo - sw/2, H - sh, sd, sw, sh))
    for sx, sy in [(3, -8), (3, 0), (3, 8), (mt+3, -8), (mt+3, 0), (mt+3, 8)]:
        tris.extend(cylinder(sx, sy, H, 1.5, 8, axis='z', segments=8))
    tris.extend(cube(0, -5, 0, mt + 2, 3, 5))
    return np.array(tris, dtype=np.float32)


def tail_fin_mount():
    """Rear stabilizer fin mount."""
    W, fmh = P["spine_W"], P["fin_mount_h"]

    tris = []
    tris.extend(cube(0, W/2 - 7, 0, P["fin_mount_t"], 14, fmh))
    tris.extend(cube(0, W/2 - 10, fmh, P["fin_mount_t"] + 5, 20, fmh * 0.3))
    for sz in [fmh*0.3, fmh*0.6, fmh*0.9]:
        tris.extend(cylinder(0, W/2 - 7, sz, 1.5, 10, axis='x', segments=8))
    return np.array(tris, dtype=np.float32)


def spine_assembly():
    """Full-length spine with segments and junction nodes."""
    total_L = P["spine_L"]
    spacing = P["node_spacing"]
    n = int(total_L / spacing)

    parts = []
    for i in range(n):
        parts.append(translate(spine_segment(), x=i * spacing))

    for i in range(1, n):
        node = translate(node_junction(), x=i * spacing - P["node_r"], y=0, z=0)
        parts.append(node)

    return merge(*parts) if parts else np.zeros((0, 3, 3), dtype=np.float32)


def spine_end_cap():
    """Cap at the end of the spine — encloses cable channel."""
    W, H, T = P["spine_W"], P["spine_H"], P["wall_t"]
    tris = []
    tris.extend(cube(0, T, T, T, W - 2*T, H - 2*T))
    tris.extend(cube(-T, W/2 - 5, H/2 - 4, T + 2, 10, 8))  # wire exit notch
    tris.extend(cylinder(T/2, W/2, H/2, 2.0, 15, axis='x', segments=12))
    return np.array(tris, dtype=np.float32)


def generate_all(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    print("Frame parts:")
    write_stl(os.path.join(out_dir, "spine_segment.stl"), spine_segment())
    write_stl(os.path.join(out_dir, "node_junction.stl"), node_junction())
    write_stl(os.path.join(out_dir, "wing_mount_plate.stl"), wing_mount_plate())
    write_stl(os.path.join(out_dir, "tail_fin_mount.stl"), tail_fin_mount())
    write_stl(os.path.join(out_dir, "spine_assembly.stl"), spine_assembly())
    write_stl(os.path.join(out_dir, "spine_end_cap.stl"), spine_end_cap())


if __name__ == "__main__":
    generate_all(os.path.dirname(__file__))