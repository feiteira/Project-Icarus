#!/usr/bin/env python3
import os, numpy as np, matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.colors as mcolors

def read_stl_vertices(filepath):
    with open(filepath, 'rb') as f:
        header = f.read(80)
        num_triangles = np.frombuffer(f.read(4), dtype='<u4')[0]
        vertices = []
        for _ in range(num_triangles):
            normal = np.frombuffer(f.read(12), dtype='<f4')
            v1 = np.frombuffer(f.read(12), dtype='<f4')
            v2 = np.frombuffer(f.read(12), dtype='<f4')
            v3 = np.frombuffer(f.read(12), dtype='<f4')
            f.read(2)
            vertices.append([v1, v2, v3])
    return np.array(vertices)

def render(stl_path, out_path, title, color):
    triangles = read_stl_vertices(stl_path)
    fig = plt.figure(figsize=(8, 6), facecolor='#1a1a2e')
    ax = fig.add_subplot(111, projection='3d', facecolor='#1a1a2e')
    verts = triangles
    faces = [verts[:, 0], verts[:, 1], verts[:, 2]]
    mesh = Poly3DCollection(faces, alpha=0.9, facecolor=mcolors.to_rgba(color), edgecolor='#2c3e50', linewidth=0.1)
    ax.add_collection3d(mesh)
    all_vertices = verts.reshape(-1, 3)
    max_range = np.ptp(all_vertices, axis=0).max()
    mid = all_vertices.mean(axis=0)
    ax.set_xlim(mid[0]-max_range/2, mid[0]+max_range/2)
    ax.set_ylim(mid[1]-max_range/2, mid[1]+max_range/2)
    ax.set_zlim(mid[2]-max_range/2, mid[2]+max_range/2)
    ax.set_box_aspect([1, 1, 1])
    ax.axis('off')
    ax.view_init(elev=25, azim=35)
    ax.set_title(title, color='white', fontsize=12, pad=8)
    plt.tight_layout(pad=0)
    plt.savefig(out_path, dpi=120, facecolor='#1a1a2e', bbox_inches='tight')
    plt.close()
    print(f"Done: {out_path}")

base = "/home/feiteira/.openclaw/workspace/ion-wind-plane"
os.makedirs(f"{base}/previews", exist_ok=True)

render(f"{base}/fuselage/fuselage_shell.stl", f"{base}/previews/1_fuselage.png", "Fuselage Shell", '#3498db')
render(f"{base}/emitters/emitter_assembly.stl", f"{base}/previews/2_emitters.png", "Emitter Array (9 posts)", '#e74c3c')
render(f"{base}/collectors/collector_with_frame.stl", f"{base}/previews/3_collectors.png", "Collector Plates + Frame", '#2ecc71')
render(f"{base}/frame/spine_assembly.stl", f"{base}/previews/4_spine.png", "Full Spine Assembly", '#9b59b6')
render(f"{base}/guards/duct_with_struts.stl", f"{base}/previews/5_duct.png", "Ducted Frame", '#f39c12')