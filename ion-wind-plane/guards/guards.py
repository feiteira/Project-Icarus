"""
Propeller Guard / Duct for Ion Wind Aircraft
Optional protective duct for any cooling fan.
Parametric design for Bambu Lab 3D printing.
"""

from stl_utils import *
import os

PARAMS = dict(
    duct_outer_r=32.0,    # outer duct radius (mm)
    duct_inner_r=28.0,    # inner duct radius (mm)
    duct_L=35.0,          # axial length (mm)
    mount_flange_r=38.0,  # mounting flange outer radius
    mount_flange_t=3.0,   # mounting flange thickness
    strut_count=6,         # number of internal struts
    strut_w=4.0,           # strut width
    segments=24,          # circumferential resolution
)


def duct_ring():
    """Hollow cylindrical duct ring."""
    p = PARAMS
    R_out = p["duct_outer_r"]
    R_in = p["duct_inner_r"]
    L = p["duct_L"]
    seg = p["segments"]
    
    tris = []
    
    # Outer cylinder
    tris.extend(cylinder(0, 0, 0, R_out, L, axis='x', segments=seg))
    
    # Inner cylinder surface (add as separate walls — we need the shell)
    # For a proper hollow duct: create inner surface + side walls
    for i in range(seg):
        t0 = 2*np.pi*i/seg
        t1 = 2*np.pi*(i+1)/seg
        
        # Outer wall quad
        o0 = [0, R_out*np.cos(t0), R_out*np.sin(t0)]
        o1 = [0, R_out*np.cos(t1), R_out*np.sin(t1)]
        o2 = [L, R_out*np.cos(t1), R_out*np.sin(t1)]
        o3 = [L, R_out*np.cos(t0), R_out*np.sin(t0)]
        
        tris.append([o0, o1, o2])
        tris.append([o0, o2, o3])
        
        # Inner wall quad
        i0 = [0, R_in*np.cos(t0), R_in*np.sin(t0)]
        i1 = [0, R_in*np.cos(t1), R_in*np.sin(t1)]
        i2 = [L, R_in*np.cos(t1), R_in*np.sin(t1)]
        i3 = [L, R_in*np.cos(t0), R_in*np.sin(t0)]
        
        # Side connecting wall
        tris.append([o0, i1, i0])
        tris.append([o0, o1, i1])
        tris.append([o0, i0, o3])
        tris.append([o3, i0, i3])
    
    # End ring flanges
    flange_r = p["mount_flange_r"]
    flange_t = p["mount_flange_t"]
    
    # Front flange (outer + inner)
    tris.extend(cylinder(0, 0, 0, flange_r, flange_t, axis='x', segments=seg))
    tris.extend(tube(0, 0, 0, R_in, R_out, flange_t, axis='x', segments=seg))
    
    # Back flange
    tris.extend(cylinder(L - flange_t, 0, 0, flange_r, flange_t, axis='x', segments=seg))
    tris.extend(tube(L - flange_t, 0, 0, R_in, flange_r, flange_t, axis='x', segments=seg))
    
    return np.array(tris, dtype=np.float32)


def duct_with_struts():
    """Duct with internal structural struts between inner and outer walls."""
    p = PARAMS
    R_out = p["duct_outer_r"]
    R_in = p["duct_inner_r"]
    L = p["duct_L"]
    seg = p["segments"]
    n = p["strut_count"]
    
    tris = []
    
    # Outer shell
    tris.extend(cylinder(0, 0, 0, R_out, L, axis='x', segments=seg))
    
    # Inner shell
    tris.extend(cylinder(0, 0, 0, R_in, L, axis='x', segments=seg))
    
    # Struts along the length
    strut_w = p["strut_w"]
    mid_r = (R_out + R_in) / 2
    
    for i in range(n):
        angle = 2*np.pi*i/n
        cx = mid_r * np.cos(angle)
        cz = mid_r * np.sin(angle)
        
        # Strut as thin rectangular box along X
        # Cross section perpendicular to radial direction
        strut_t = R_out - R_in
        tris.extend(cube(0, cx - strut_w/2, cz - strut_t/2,
                          L, strut_w, strut_t))
    
    # Mount flanges
    flange_r = p["mount_flange_r"]
    flange_t = p["mount_flange_t"]
    for x_f in [0, L - flange_t]:
        tris.extend(cylinder(x_f, 0, 0, flange_r, flange_t, axis='x', segments=seg))
    
    return np.array(tris, dtype=np.float32)


def wire_guard_mesh():
    """
    Wire-frame protective ring — minimal material, good for prop protection.
    No solid walls; just crossed wires.
    """
    p = PARAMS
    R = p["duct_outer_r"]
    L = p["duct_L"]
    n = p["strut_count"]
    wire_r = 1.5
    
    tris = []
    
    # Ring circles at each end
    for x_end in [0, L]:
        for i in range(n):
            t1 = 2*np.pi*i/n
            t2 = 2*np.pi*(i+1)/n
            
            p1 = [x_end, R*np.cos(t1), R*np.sin(t1)]
            p2 = [x_end, R*np.cos(t2), R*np.sin(t2)]
            
            seg_L = np.sqrt((p2[1]-p1[1])**2 + (p2[2]-p1[2])**2)
            mx = x_end
            my = (p1[1] + p2[1]) / 2
            mz = (p1[2] + p2[2]) / 2
            tris.extend(cylinder(mx, my, mz, wire_r, seg_L, axis='z', segments=6))
    
    # Axial wires (longitudinal)
    for i in range(n):
        angle = 2*np.pi*i/n
        cx = R * np.cos(angle)
        cz = R * np.sin(angle)
        tris.extend(cylinder(0, cx, cz, wire_r, L, axis='x', segments=6))
    
    # Cross wires (diagonal)
    for i in range(n):
        angle = np.pi*i/n
        cx = R * np.cos(angle)
        cz = R * np.sin(angle)
        tris.extend(cylinder(L/2, cx, cz, wire_r, L*0.7, axis='x', segments=6))
    
    return np.array(tris, dtype=np.float32)


def generate_all(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    print("Guard parts:")
    
    write_stl(os.path.join(out_dir, "duct_ring.stl"), duct_ring())
    write_stl(os.path.join(out_dir, "duct_with_struts.stl"), duct_with_struts())
    write_stl(os.path.join(out_dir, "wire_guard_mesh.stl"), wire_guard_mesh())


if __name__ == "__main__":
    generate_all(os.path.dirname(__file__))