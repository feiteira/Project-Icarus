"""
Emitter Wire Supports for Ion Wind Aircraft
Holds thin tungsten wire (~0.5mm) under tension between two frames.
Parametric design for Bambu Lab 3D printing.
"""

from stl_utils import *
import os

P = dict(
    wire_dia=0.5,
    wire_span=200.0,
    gap=25.0,
    frame_W=80.0,
    frame_H=60.0,
    frame_D=10.0,
    support_spacing=25.0,
    post_r=4.0,
    post_base_w=16.0,
    post_base_d=12.0,
    slot_w=2.0,
    slot_d=4.0,
    adj_body_r=8.0,
    adj_body_L=20.0,
    spring_pocket_r=7.0,
    flange_t=2.5,
    insulator_w=70.0,
    insulator_h=8.0,
    insulator_t=3.0,
    snap_w=4.0, snap_h=2.0, snap_d=3.0,
)


def emitter_frame():
    """Rectangular wire frame — hollow ring with mounting flanges."""
    W, H, D = P["frame_W"], P["frame_H"], P["frame_D"]
    strut = 5.0
    tris = []
    tris.extend(cube(0, 0, 0, D, strut, strut))                          # bottom
    tris.extend(cube(0, 0, H - strut, D, strut, strut))                    # top
    tris.extend(cube(0, 0, 0, strut, W, strut))                           # left
    tris.extend(cube(0, W - strut, 0, strut, strut, H))                 # right
    tris.extend(cube(0, -6, 0, strut, 6, H))                              # front gusset
    tris.extend(cube(0, W - strut, 0, strut, 6, H))                        # back gusset

    # Mounting flanges
    fw, fh = 12.0, 3.0
    tris.extend(cube(0, -fw/2, H, D, fw, fh))
    tris.extend(cube(0, -fw/2, -fh, D, fw, fh))

    # Screw holes
    for xh in [D/4, 3*D/4]:
        for yo in [-6, 6]:
            tris.extend(cylinder(xh, yo, H + 1.5, 1.5, 8, axis='z', segments=8))
            tris.extend(cylinder(xh, yo, -1.5, 1.5, 8, axis='z', segments=8))

    return np.array(tris, dtype=np.float32)


def wire_support_post():
    """Single wire support post with wire-guide notch at top."""
    r = P["post_r"]
    bw, bd = P["post_base_w"], P["post_base_d"]
    H = P["frame_H"]
    slot_w, slot_d = P["slot_w"], P["slot_d"]

    tris = []
    tris.extend(cube(-bd/2, -bw/2, 0, bd, bw, 2.0))   # base plate

    # Main post (12-sided approx)
    n = 12
    for i in range(n):
        t0 = 2*np.pi*i/n
        t1 = 2*np.pi*(i+1)/n
        dx = r * abs(np.cos(t1) - np.cos(t0)) + 1
        dy = r * abs(np.sin(t1) - np.sin(t0)) + 1
        tris.extend(cube(r*np.cos(t0) - dx/2, r*np.sin(t0) - dy/2, 2,
                          dx, dy, H - 10))

    # Wire guide notch
    nz = H - 3
    tris.extend(cube(-slot_d/2, -slot_w/2, nz, slot_d, slot_w, 4.0))

    return np.array(tris, dtype=np.float32)


def wire_support_array():
    """All wire support posts along the wire span."""
    spacing = P["support_spacing"]
    span = P["wire_span"]
    n = int(span / spacing) + 1
    parts = [wire_support_post() for _ in range(n)]
    if parts:
        return merge(*[translate(parts[i], x=i*spacing) for i in range(n)])
    return np.zeros((0, 3, 3), dtype=np.float32)


def tension_adjuster():
    """Spring-loaded tension adjuster at wire end."""
    br, bL = P["adj_body_r"], P["adj_body_L"]
    spr, fl = P["spring_pocket_r"], P["flange_t"]
    sw = P["slot_w"] + 0.5

    tris = []
    tris.extend(cylinder(0, 0, 0, br, bL, axis='x', segments=24))
    tris.extend(cylinder(bL/2, 0, br - 3, sw/2 + 1, bL/2 + 2, axis='z', segments=12))
    tris.extend(cube(-fl, -br*1.25, -br*1.25, fl, br*2.5, br*2.5))  # flange
    tris.extend(cylinder(bL - bL*0.5, 0, 0, spr, bL*0.5, axis='x', segments=24))
    tris.extend(cylinder(bL, 0, 0, br*0.7, 4.0, axis='x', segments=16))
    for yo in [-8, 0, 8]:
        tris.extend(cylinder(-0.5, yo, 0, 1.2, 8.0, axis='y', segments=8))

    return np.array(tris, dtype=np.float32)


def insulator_spacer():
    """Insulating spacer plate between HV emitter and grounded frame."""
    w, h, t = P["insulator_w"], P["insulator_h"], P["insulator_t"]
    nw, nh, nd = P["snap_w"], P["snap_h"], P["snap_d"]

    tris = []
    tris.extend(cube(0, 0, 0, t, w, h))

    # Snap-fit tabs
    for yy in [w*0.25, w*0.75]:
        tris.extend(cube(t, yy - nw/2, h - nh, nd, nw, nh))

    # Cable tie slots
    for zz in [h*0.3, h*0.7]:
        tris.extend(cube(0, w/2 - 2, zz, t + 5, 4, 1.5))

    return np.array(tris, dtype=np.float32)


def complete_emitter_assembly():
    """Full emitter assembly: frame + supports + tension adjusters."""
    span = P["wire_span"]
    FH = P["frame_H"]

    parts = []
    # Top frame
    parts.append(translate(emitter_frame(), x=0, y=0, z=FH))
    # Bottom frame
    parts.append(translate(emitter_frame(), x=0, y=0, z=0))
    # Wire supports
    parts.append(wire_support_array())
    # Left adjuster
    adj_l = translate(tension_adjuster(), x=-5, y=P["frame_W"]/2, z=FH/2)
    parts.append(rotate(adj_l, 90, axis='z'))
    # Right adjuster
    adj_r = translate(tension_adjuster(), x=span + 5, y=P["frame_W"]/2, z=FH/2)
    parts.append(rotate(adj_r, -90, axis='z'))

    return merge(*parts) if parts else np.zeros((0,3,3), dtype=np.float32)


def generate_all(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    print("Emitter parts:")
    write_stl(os.path.join(out_dir, "emitter_frame.stl"), emitter_frame())
    write_stl(os.path.join(out_dir, "wire_support_post.stl"), wire_support_post())
    write_stl(os.path.join(out_dir, "wire_support_array.stl"), wire_support_array())
    write_stl(os.path.join(out_dir, "tension_adjuster.stl"), tension_adjuster())
    write_stl(os.path.join(out_dir, "insulator_spacer.stl"), insulator_spacer())
    write_stl(os.path.join(out_dir, "emitter_assembly.stl"), complete_emitter_assembly())


if __name__ == "__main__":
    generate_all(os.path.dirname(__file__))