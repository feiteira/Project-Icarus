"""
STL Generator Utilities v2 — Full-featured binary STL writer + geometry helpers.
No external CAD libraries required. Uses only numpy.
"""

import numpy as np
import struct
import math

# ─────────────────────────────────────────────────────────────────────────────
# Binary STL writer
# ─────────────────────────────────────────────────────────────────────────────

def write_stl(filepath: str, triangles: np.ndarray):
    """
    Write (N, 3, 3) triangle array as a binary STL file.
    Each triangle: 3 vertices × (x, y, z)
    """
    tris = np.asarray(triangles, dtype=np.float32)
    if tris.ndim != 3 or tris.shape[1:] != (3, 3):
        raise ValueError(f"Expected (N,3,3) array, got shape {tris.shape}")
    with open(filepath, 'wb') as f:
        f.write(b'\x00' * 80)
        f.write(struct.pack('<I', len(tris)))
        for tri in tris:
            v0, v1, v2 = tri[0], tri[1], tri[2]
            n = np.cross(v1 - v0, v2 - v0)
            ln = math.sqrt(n[0]**2 + n[1]**2 + n[2]**2)
            n = (n / ln).astype(np.float32) if ln > 1e-9 else np.array([0, 0, 1], dtype=np.float32)
            f.write(struct.pack('<3f', *n))
            for v in tri:
                f.write(struct.pack('<3f', *v))
            f.write(struct.pack('<H', 0))
    print(f"  -> {filepath}  ({len(tris)} tris)")


# ─────────────────────────────────────────────────────────────────────────────
# Mesh helpers
# ─────────────────────────────────────────────────────────────────────────────

def merge(*meshes):
    """Concatenate multiple meshes into one."""
    flat = []
    for m in meshes:
        arr = np.asarray(m, dtype=np.float32)
        if arr.size > 0:
            flat.append(arr)
    return np.concatenate(flat) if flat else np.zeros((0, 3, 3), dtype=np.float32)


def translate(mesh, x=0.0, y=0.0, z=0.0):
    m = mesh.copy()
    m[:, :, 0] += x
    m[:, :, 1] += y
    m[:, :, 2] += z
    return m


def rotate(mesh, angle_deg, axis='z'):
    """Rotate mesh around axis passing through origin."""
    a = math.radians(angle_deg)
    c, s = math.cos(a), math.sin(a)
    if axis == 'z':
        R = np.array([[c,-s,0],[s,c,0],[0,0,1]], dtype=np.float32)
    elif axis == 'x':
        R = np.array([[1,0,0],[0,c,-s],[0,s,c]], dtype=np.float32)
    elif axis == 'y':
        R = np.array([[c,0,s],[0,1,0],[-s,0,c]], dtype=np.float32)
    else:
        raise ValueError(f"Unknown axis: {axis}")
    m = mesh.copy()
    for i in range(m.shape[0]):
        for j in range(3):
            m[i, j] = R @ m[i, j]
    return m


def scale(mesh, sx=1.0, sy=1.0, sz=1.0):
    m = mesh.copy()
    m[:, :, 0] *= sx
    m[:, :, 1] *= sy
    m[:, :, 2] *= sz
    return m


# ─────────────────────────────────────────────────────────────────────────────
# Primitives — all return (N,3,3) float32 arrays
# Each vertex is stored as np.array (not list) so np.array() on the
# result correctly produces a (N,3,3) shape, not (N,3,3,3) or inhomogeneous.
# ─────────────────────────────────────────────────────────────────────────────

def cube(x=0.0, y=0.0, z=0.0, dx=1.0, dy=1.0, dz=1.0):
    """
    Solid axis-aligned cube with one corner at (x,y,z)
    and dimensions (dx, dy, dz).
    """
    def v(i, j, k):
        return np.array([x+i*dx, y+j*dy, z+k*dz], dtype=np.float32)
    tris = []
    for q in [
        [v(0,0,0), v(1,0,0), v(1,1,0), v(0,1,0)],
        [v(0,0,1), v(1,0,1), v(1,1,1), v(0,1,1)],
        [v(0,0,0), v(1,0,0), v(1,0,1), v(0,0,1)],
        [v(1,0,0), v(1,1,0), v(1,1,1), v(1,0,1)],
        [v(1,1,0), v(0,1,0), v(0,1,1), v(1,1,1)],
        [v(0,1,0), v(0,0,0), v(0,0,1), v(0,1,1)],
    ]:
        tris.append((q[0], q[1], q[2]))
        tris.append((q[0], q[2], q[3]))
    return np.array(tris, dtype=np.float32)


def cylinder(cx=0.0, cy=0.0, cz=0.0, r=1.0, h=1.0, axis='z', segments=24):
    """
    Solid cylinder centered at (cx,cy,cz), radius r, height h,
    axis of revolution = 'x', 'y', or 'z'.
    """
    tris = []
    for i in range(segments):
        t0 = 2*math.pi*i/segments
        t1 = 2*math.pi*(i+1)/segments
        if axis == 'z':
            p0 = np.array([cx+r*math.cos(t0), cy+r*math.sin(t0), cz], dtype=np.float32)
            p1 = np.array([cx+r*math.cos(t1), cy+r*math.sin(t1), cz], dtype=np.float32)
            p2 = np.array([cx, cy, cz], dtype=np.float32)
            p3 = np.array([cx, cy, cz+h], dtype=np.float32)
            p4 = np.array([cx+r*math.cos(t0), cy+r*math.sin(t0), cz+h], dtype=np.float32)
            p5 = np.array([cx+r*math.cos(t1), cy+r*math.sin(t1), cz+h], dtype=np.float32)
        elif axis == 'x':
            p0 = np.array([cx, cy+r*math.cos(t0), cz+r*math.sin(t0)], dtype=np.float32)
            p1 = np.array([cx, cy+r*math.cos(t1), cz+r*math.sin(t1)], dtype=np.float32)
            p2 = np.array([cx, cy, cz], dtype=np.float32)
            p3 = np.array([cx+h, cy, cz], dtype=np.float32)
            p4 = np.array([cx+h, cy+r*math.cos(t0), cz+r*math.sin(t0)], dtype=np.float32)
            p5 = np.array([cx+h, cy+r*math.cos(t1), cz+r*math.sin(t1)], dtype=np.float32)
        elif axis == 'y':
            p0 = np.array([cx+r*math.cos(t0), cy, cz+r*math.sin(t0)], dtype=np.float32)
            p1 = np.array([cx+r*math.cos(t1), cy, cz+r*math.sin(t1)], dtype=np.float32)
            p2 = np.array([cx, cy, cz], dtype=np.float32)
            p3 = np.array([cx, cy+h, cz], dtype=np.float32)
            p4 = np.array([cx+r*math.cos(t0), cy+h, cz+r*math.sin(t0)], dtype=np.float32)
            p5 = np.array([cx+r*math.cos(t1), cy+h, cz+r*math.sin(t1)], dtype=np.float32)
        else:
            raise ValueError(f"Bad axis: {axis}")
        tris.append((p0, p1, p5)); tris.append((p0, p5, p4))
        tris.append((p2, p1, p0)); tris.append((p3, p4, p5))
    return np.array(tris, dtype=np.float32)


def tube(cx=0.0, cy=0.0, cz=0.0, r_inner=0.8, r_outer=1.0, h=1.0, axis='z', segments=24):
    """
    Hollow annular tube (cylinder shell).
    """
    tris = []
    for i in range(segments):
        t0 = 2*math.pi*i/segments
        t1 = 2*math.pi*(i+1)/segments
        if axis == 'z':
            i0 = np.array([cx+r_inner*math.cos(t0), cy+r_inner*math.sin(t0), cz], dtype=np.float32)
            i1 = np.array([cx+r_inner*math.cos(t1), cy+r_inner*math.sin(t1), cz], dtype=np.float32)
            o0 = np.array([cx+r_outer*math.cos(t0), cy+r_outer*math.sin(t0), cz], dtype=np.float32)
            o1 = np.array([cx+r_outer*math.cos(t1), cy+r_outer*math.sin(t1), cz], dtype=np.float32)
            i2 = np.array([cx+r_inner*math.cos(t0), cy+r_inner*math.sin(t0), cz+h], dtype=np.float32)
            i3 = np.array([cx+r_inner*math.cos(t1), cy+r_inner*math.sin(t1), cz+h], dtype=np.float32)
            o2 = np.array([cx+r_outer*math.cos(t0), cy+r_outer*math.sin(t0), cz+h], dtype=np.float32)
            o3 = np.array([cx+r_outer*math.cos(t1), cy+r_outer*math.sin(t1), cz+h], dtype=np.float32)
        elif axis == 'x':
            i0 = np.array([cx, cy+r_inner*math.cos(t0), cz+r_inner*math.sin(t0)], dtype=np.float32)
            i1 = np.array([cx, cy+r_inner*math.cos(t1), cz+r_inner*math.sin(t1)], dtype=np.float32)
            o0 = np.array([cx, cy+r_outer*math.cos(t0), cz+r_outer*math.sin(t0)], dtype=np.float32)
            o1 = np.array([cx, cy+r_outer*math.cos(t1), cz+r_outer*math.sin(t1)], dtype=np.float32)
            i2 = np.array([cx+h, cy+r_inner*math.cos(t0), cz+r_inner*math.sin(t0)], dtype=np.float32)
            i3 = np.array([cx+h, cy+r_inner*math.cos(t1), cz+r_inner*math.sin(t1)], dtype=np.float32)
            o2 = np.array([cx+h, cy+r_outer*math.cos(t0), cz+r_outer*math.sin(t0)], dtype=np.float32)
            o3 = np.array([cx+h, cy+r_outer*math.cos(t1), cz+r_outer*math.sin(t1)], dtype=np.float32)
        elif axis == 'y':
            i0 = np.array([cx+r_inner*math.cos(t0), cy, cz+r_inner*math.sin(t0)], dtype=np.float32)
            i1 = np.array([cx+r_inner*math.cos(t1), cy, cz+r_inner*math.sin(t1)], dtype=np.float32)
            o0 = np.array([cx+r_outer*math.cos(t0), cy, cz+r_outer*math.sin(t0)], dtype=np.float32)
            o1 = np.array([cx+r_outer*math.cos(t1), cy, cz+r_outer*math.sin(t1)], dtype=np.float32)
            i2 = np.array([cx+r_inner*math.cos(t0), cy+h, cz+r_inner*math.sin(t0)], dtype=np.float32)
            i3 = np.array([cx+r_inner*math.cos(t1), cy+h, cz+r_inner*math.sin(t1)], dtype=np.float32)
            o2 = np.array([cx+r_outer*math.cos(t0), cy+h, cz+r_outer*math.sin(t0)], dtype=np.float32)
            o3 = np.array([cx+r_outer*math.cos(t1), cy+h, cz+r_outer*math.sin(t1)], dtype=np.float32)
        else:
            raise ValueError(f"Bad axis: {axis}")
        # Inner wall
        tris.append((i0, i1, i3)); tris.append((i0, i3, i2))
        # Outer wall
        tris.append((o0, o1, o3)); tris.append((o0, o3, o2))
    return np.array(tris, dtype=np.float32)


def screw_standoff(cx=0.0, cy=0.0, cz=0.0, outer_r=3.5, inner_r=1.5, h=10.0, segments=16):
    """Hollow standoff pillar with center through-hole (for M3 screw)."""
    return tube(cx, cy, cz, r_inner=inner_r, r_outer=outer_r, h=h, axis='z', segments=segments)


def snap_tab(x=0.0, y=0.0, z=0.0, w=4.0, h=2.0, d=3.0):
    """Small snap-fit protrusion tab."""
    return cube(x, y - w/2, z, d, w, h)


def add_quad(tris_list, v0, v1, v2, v3):
    """Add a quad as two triangles to a tris list (helper for hulls)."""
    tris_list.append((v0, v1, v2))
    tris_list.append((v0, v2, v3))


def panel(x=0.0, y=0.0, z=0.0, dx=1.0, dy=1.0, dz=0.2):
    """Thin flat panel."""
    return cube(x, y, z, dx, dy, dz)


def verify_mesh(triangles):
    """Assert mesh is valid (N,3,3) float32."""
    arr = np.asarray(triangles, dtype=np.float32)
    assert arr.ndim == 3 and arr.shape[1:] == (3, 3), f"Bad shape {arr.shape}"
    return arr