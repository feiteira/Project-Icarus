"""
Fuselage & Electronics Enclosure for Ion Wind Aircraft
Parametric, designed for Bambu Lab X1C/P1P (256×256×256mm build volume)

Physical sizing:
  - Total length: 180mm  (fits in 256mm build volume with margin)
  - Width: 80mm / Height: 50mm
  - Battery: up to 4× 18650 cells side-by-side
  - HV multiplier module bay in nose section
"""

from stl_utils import *
import os

P = dict(
    L=180.0, W=80.0, H=50.0, wall=2.0,
    cells=4, cell_d=18.0, cell_L=65.0,
    hv_w=60.0, hv_h=28.0, hv_d=45.0,
    snap_w=4.0, snap_h=1.8, snap_d=3.0,
    lid_t=1.5,
    rib_t=1.2, rib_spacing=28.0,
)


def fuselage_shell():
    """Hollow box shell — outer hull with inner cavity removed."""
    L, W, H, T = P["L"], P["W"], P["H"], P["wall"]
    iL, iW, iH = L - 2*T, W - 2*T, H - 2*T
    tris = []

    def ov(i, j, k):
        return np.array([i*L, j*W, k*H], dtype=np.float32)
    def iv(i, j, k):
        return np.array([T + i*iL, T + j*iW, T + k*iH], dtype=np.float32)

    # Outer faces (+Z, -Z, +X, -X, +Y, -Y)
    add_quad(tris, ov(0,0,0), ov(1,0,0), ov(1,1,0), ov(0,1,0))
    add_quad(tris, ov(0,0,1), ov(1,0,1), ov(1,1,1), ov(0,1,1))
    add_quad(tris, ov(0,0,0), ov(1,0,0), ov(1,0,1), ov(0,0,1))
    add_quad(tris, ov(1,0,0), ov(1,1,0), ov(1,1,1), ov(1,0,1))
    add_quad(tris, ov(0,1,0), ov(1,1,0), ov(1,1,1), ov(0,1,1))
    add_quad(tris, ov(0,0,0), ov(1,0,0), ov(0,1,0), ov(0,1,1))

    # Inner faces (winding reversed — normals point inward)
    add_quad(tris, iv(1,0,0), iv(0,0,0), iv(0,1,0), iv(1,1,0))
    add_quad(tris, iv(0,0,1), iv(1,0,1), iv(1,1,1), iv(0,1,1))
    add_quad(tris, iv(0,0,0), iv(0,0,1), iv(1,0,1), iv(1,0,0))
    add_quad(tris, iv(1,0,0), iv(1,0,1), iv(1,1,1), iv(1,1,0))
    add_quad(tris, iv(0,1,0), iv(0,1,1), iv(1,1,1), iv(1,0,0))
    add_quad(tris, iv(0,0,0), iv(1,0,0), iv(0,1,0), iv(0,1,1))

    # Side walls: connect outer face to corresponding inner face
    # Front wall (+X)
    add_quad(tris, ov(1,0,0), ov(1,0,1), iv(1,0,1), iv(1,0,0))
    add_quad(tris, ov(1,1,0), iv(1,1,0), iv(1,1,1), ov(1,1,1))
    add_quad(tris, ov(1,0,0), iv(1,0,0), iv(1,1,0), ov(1,1,0))
    add_quad(tris, ov(1,0,1), iv(1,0,1), iv(1,1,1), ov(1,1,1))
    # Back wall (-X)
    add_quad(tris, ov(0,0,0), iv(0,0,0), iv(0,0,1), ov(0,0,1))
    add_quad(tris, ov(0,1,0), ov(0,1,1), iv(0,1,1), iv(0,1,0))
    add_quad(tris, ov(0,0,0), ov(0,1,0), iv(0,1,0), iv(0,0,0))
    add_quad(tris, ov(0,0,1), iv(0,0,1), iv(0,1,1), ov(0,1,1))
    # Right wall (+Y)
    add_quad(tris, ov(0,1,0), ov(0,1,1), iv(0,1,1), iv(0,1,0))
    add_quad(tris, ov(1,1,0), iv(1,1,0), iv(1,1,1), ov(1,1,1))
    add_quad(tris, ov(0,1,0), iv(0,1,0), iv(1,1,0), ov(1,1,0))
    add_quad(tris, ov(0,1,1), iv(0,1,1), iv(1,1,1), ov(1,1,1))
    # Left wall (-Y)
    add_quad(tris, ov(0,0,0), iv(0,0,0), iv(0,0,1), ov(0,0,1))
    add_quad(tris, ov(1,0,0), ov(1,0,1), iv(1,0,1), iv(1,0,0))
    add_quad(tris, ov(0,0,0), ov(1,0,0), iv(1,0,0), iv(0,0,0))
    add_quad(tris, ov(0,0,1), iv(0,0,1), iv(1,0,1), ov(1,0,1))
    # Top wall (+Z)
    add_quad(tris, ov(0,0,1), iv(0,0,1), iv(0,1,1), ov(0,1,1))
    add_quad(tris, ov(1,0,1), ov(1,1,1), iv(1,1,1), iv(1,0,1))
    add_quad(tris, ov(0,0,1), ov(1,0,1), iv(1,0,1), iv(0,0,1))
    add_quad(tris, ov(0,1,1), iv(0,1,1), iv(1,1,1), ov(1,1,1))
    # Bottom wall (-Z)
    add_quad(tris, ov(0,0,0), ov(0,1,0), iv(0,1,0), iv(0,0,0))
    add_quad(tris, ov(1,0,0), iv(1,0,0), iv(1,1,0), ov(1,1,0))
    add_quad(tris, ov(0,0,0), iv(0,0,0), iv(1,0,0), ov(1,0,0))
    add_quad(tris, ov(0,1,0), iv(0,1,0), iv(1,1,0), ov(1,1,0))

    return np.array(tris, dtype=np.float32)


def battery_bay():
    """Battery holder tray for 4× 18650 cells."""
    L, W, H, T = P["L"], P["W"], P["H"], P["wall"]
    cell_d, cell_L, cells = P["cell_d"], P["cell_L"], P["cells"]
    spacing = cell_d + 4.0
    total_w = cells * spacing
    start_x = T + (L - total_w) / 2
    start_y = (W - cell_d) / 2

    tris = []
    for i in range(cells):
        cx = start_x + i * spacing + cell_d / 2
        cy = start_y + cell_d / 2
        cz = T + 4.0
        hw = cell_d + 4.0
        hh = cell_d + 4.0
        hL = cell_L + 6.0
        hx, hy, hz = cx - hL/2, cy - hw/2, cz

        tris.extend(cube(hx, hy, hz, hL, hw, 1.5))                           # bottom
        tris.extend(cube(hx, hy, hz, hL, 1.5, hh))                            # front wall
        tris.extend(cube(hx, hy + hw - 1.5, hz, hL, 1.5, hh))                 # back wall
        tris.extend(cube(hx, hy, hz, 1.5, hw, hh))                             # left wall
        tris.extend(cube(hx + hL - 1.5, hy, hz, 1.5, hw, hh))                  # right wall
        tris.extend(cylinder(hx + hL + 2, cy, cz + hh/2 - 3, 3.0, 5.0, axis='x', segments=12))  # spring
        tris.extend(screw_standoff(hx - 4, cy, cz + hh/2 - 5, outer_r=3.0, inner_r=1.2, h=8, segments=12))  # standoff

    return np.array(tris, dtype=np.float32)


def hv_module_bay():
    """HV multiplier module mounting bay."""
    L, W, H, T = P["L"], P["W"], P["H"], P["wall"]
    mw, mh, md = P["hv_w"], P["hv_h"], P["hv_d"]
    bx = L - T - md - 5
    by = (W - mw) / 2
    bz = T + 10

    tris = []
    tris.extend(cube(bx, by, bz, md, mw, 2.0))
    wt = 1.5
    wh = mh + 5
    tris.extend(cube(bx - wt, by - wt, bz, wt, mw + wt*2, wh))
    tris.extend(cube(bx + md, by - wt, bz, wt, mw + wt*2, wh))
    for sx, sy in [(bx+5, by+5), (bx+md-5, by+5), (bx+5, by+mw-5), (bx+md-5, by+mw-5)]:
        tris.extend(screw_standoff(sx, sy, bz+2, outer_r=3.5, inner_r=1.5, h=10, segments=12))
    tris.extend(cylinder(bx - wt - 3, W/2, bz + wh/2, 5.0, 5.0, axis='x', segments=12))
    return np.array(tris, dtype=np.float32)


def lid():
    """Top lid — snaps onto fuselage body."""
    L, W, H, T = P["L"], P["W"], P["H"], P["wall"]
    lt = P["lid_t"]
    sw, sh, sd = P["snap_w"], P["snap_h"], P["snap_d"]

    tris = []
    tris.extend(cube(T, T, H - T, L - 2*T, W - 2*T, lt))
    for sx, sy in [(L*0.25, T+5), (L*0.75, T+5), (L*0.25, W-5), (L*0.75, W-5)]:
        tris.extend(cube(sx - sd/2, sy - sw/2, H - T - sh, sd, sw, sh))
    return np.array(tris, dtype=np.float32)


def internal_ribs():
    """Lightweight honeycomb ribs inside fuselage."""
    L, W, H, T = P["L"], P["W"], P["H"], P["wall"]
    rt, sp = P["rib_t"], P["rib_spacing"]
    tris = []
    for i in range(int(L / sp)):
        x = T + (i + 0.5) * sp
        rw = sp * 0.5
        tris.extend(cube(x - rw/2, T, T, rw, W - 2*T, rt))
        tris.extend(cube(x - rw/2, T, H - T - rt, rw, W - 2*T, rt))
    return np.array(tris, dtype=np.float32)


def generate_all(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    print("Fuselage parts:")
    write_stl(os.path.join(out_dir, "fuselage_shell.stl"), fuselage_shell())
    write_stl(os.path.join(out_dir, "battery_bay.stl"), battery_bay())
    write_stl(os.path.join(out_dir, "hv_module_bay.stl"), hv_module_bay())
    write_stl(os.path.join(out_dir, "lid.stl"), lid())
    write_stl(os.path.join(out_dir, "internal_ribs.stl"), internal_ribs())


if __name__ == "__main__":
    generate_all(os.path.dirname(__file__))