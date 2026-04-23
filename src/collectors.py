"""
Collector Plate Mounts for Ion Wind Aircraft
Large smooth surfaces that collect ions — flat plates or foil arrays.
Parametric design for Bambu Lab 3D printing.
"""

from stl_utils import *
import os

P = dict(
    plate_w=30.0,
    plate_h=50.0,
    plate_t=1.5,
    gap=25.0,
    frame_W=80.0,
    frame_H=60.0,
    frame_D=10.0,
    fin_count=8,
    fin_spacing=5.0,
    fin_t=0.5,
    adj_outer_r=8.0,
    adj_inner_r=6.0,
    adj_h=40.0,
    tab_w=12.0,
    tab_h=3.0,
    tab_t=2.0,
)


def collector_plate():
    """Single flat collector plate with chamfered edges."""
    w, h, t = P["plate_w"], P["plate_h"], P["plate_t"]
    tris = []
    tris.extend(cube(0, -w/2, -h/2, t, w, h))
    bev = 1.0
    tris.extend(cube(0, -w/2, -h/2, t + bev, bev, bev))
    tris.extend(cube(0, w/2 - bev, -h/2, t + bev, bev, bev))
    tris.extend(cube(0, -w/2, h/2 - bev, t + bev, bev, bev))
    tris.extend(cube(0, w/2 - bev, h/2 - bev, t + bev, bev, bev))
    return np.array(tris, dtype=np.float32)


def collector_foil_array():
    """Multiple thin foil collectors in parallel."""
    n, sp, w, h = P["fin_count"], P["fin_spacing"], P["plate_w"], P["plate_h"]
    t = P["fin_t"]
    total = n * sp
    start = -total / 2
    tris = []
    for i in range(n):
        y = start + i * sp + sp / 2
        tris.extend(cube(0, y - sp/2 + t/2, -h/2, P["plate_t"], sp - t, h))
    return np.array(tris, dtype=np.float32)


def collector_mount_frame():
    """Rectangular frame holding collector plates."""
    W, H, D = P["frame_W"], P["frame_H"], P["frame_D"]
    strut = 5.0
    tw, th, tt = P["tab_w"], P["tab_h"], P["tab_t"]

    tris = []
    tris.extend(cube(0, 0, 0, D, strut, strut))
    tris.extend(cube(0, 0, H - strut, D, strut, strut))
    tris.extend(cube(0, 0, 0, strut, W, strut))
    tris.extend(cube(0, W - strut, 0, strut, strut, H))

    # Mounting tabs
    corners = [
        (0, 0, strut), (D - tt, 0, strut),
        (0, W - tw, strut), (D - tt, W - tw, strut),
        (0, 0, H - strut - th), (D - tt, 0, H - strut - th),
        (0, W - tw, H - strut - th), (D - tt, W - tw, H - strut - th),
    ]
    for tx, ty, tz in corners:
        tris.extend(cube(tx, ty, tz, tt, tw, th))

    # Screw holes
    for hx, hy in [(D/3, 5), (2*D/3, 5), (D/3, W-5), (2*D/3, W-5)]:
        tris.extend(cylinder(hx, hy, H/2, 1.5, 15, axis='z', segments=12))

    return np.array(tris, dtype=np.float32)


def collector_with_frame():
    """Collector plate inside its mount frame."""
    plate = collector_plate()
    plate = translate(plate, x=P["plate_t"] + 2)
    frame = collector_mount_frame()
    return merge(plate, frame)


def adjustable_collector_mount():
    """Height-adjustable sliding tube mount for gap tuning."""
    or_, ir_, h = P["adj_outer_r"], P["adj_inner_r"], P["adj_h"]

    tris = []
    tris.extend(tube(0, 0, 0, r_inner=ir_, r_outer=or_, h=h*0.6, axis='z', segments=24))
    tris.extend(cylinder(0, 0, h*0.5, ir_ - 1.0, h*0.6, axis='z', segments=16))
    tris.extend(cylinder(0, 0, h*0.4, or_ + 2.0, 5.0, axis='z', segments=24))  # lock ring
    tris.extend(cube(-12.5, -12.5, h + 15, 25, 25, 3.0))  # mount plate
    tris.extend(cylinder(0, 0, h*0.5, 2.0, h*0.3, axis='z', segments=12))  # lock screw
    return np.array(tris, dtype=np.float32)


def streamer_suppressor():
    """Corona suppressor fins between emitter and collector."""
    gap, w = P["gap"], P["plate_w"]
    fin_t, fin_count = 0.8, 4

    tris = []
    for i in range(fin_count):
        z = gap + 3 + i * 3.0
        tris.extend(cube(0, -w/2, z, fin_t, w, 3.0))
    return np.array(tris, dtype=np.float32)


def generate_all(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    print("Collector parts:")
    write_stl(os.path.join(out_dir, "collector_plate.stl"), collector_plate())
    write_stl(os.path.join(out_dir, "collector_foil_array.stl"), collector_foil_array())
    write_stl(os.path.join(out_dir, "collector_mount_frame.stl"), collector_mount_frame())
    write_stl(os.path.join(out_dir, "collector_with_frame.stl"), collector_with_frame())
    write_stl(os.path.join(out_dir, "adjustable_mount.stl"), adjustable_collector_mount())
    write_stl(os.path.join(out_dir, "streamer_suppressor.stl"), streamer_suppressor())


if __name__ == "__main__":
    generate_all(os.path.dirname(__file__))