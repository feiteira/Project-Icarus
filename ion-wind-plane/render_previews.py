#!/usr/bin/env python3
"""Render STL files to PNG images using matplotlib 3D axes."""

import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.colors as mcolors

workspace = "/home/feiteira/.openclaw/workspace/ion-wind-plane"
output_dir = os.path.join(workspace, "previews")
os.makedirs(output_dir, exist_ok=True)

def read_stl_vertices(filepath):
    """Simple STL parser - extracts vertices from binary STL."""
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

def render_stl_to_png(stl_path, output_path, title="", color='#3498db', bg='#0a0e17', elevation=30, azimuth=45):
    try:
        triangles = read_stl_vertices(stl_path)
        fig = plt.figure(figsize=(10, 8), facecolor=bg)
        ax = fig.add_subplot(111, projection='3d', facecolor=bg)
        verts = triangles
        faces = [verts[:, 0], verts[:, 1], verts[:, 2]]
        face_color = mcolors.to_rgba(color) if isinstance(color, str) else color
        mesh = Poly3DCollection(faces, alpha=0.9, facecolor=face_color, edgecolor='#2c3e50', linewidth=0.1)
        ax.add_collection3d(mesh)
        all_vertices = verts.reshape(-1, 3)
        max_range = np.ptp(all_vertices, axis=0).max()
        mid = all_vertices.mean(axis=0)
        ax.set_xlim(mid[0] - max_range/2, mid[0] + max_range/2)
        ax.set_ylim(mid[1] - max_range/2, mid[1] + max_range/2)
        ax.set_zlim(mid[2] - max_range/2, mid[2] + max_range/2)
        ax.set_box_aspect([1, 1, 1])
        ax.axis('off')
        ax.view_init(elev=elevation, azim=azimuth)
        if title:
            ax.set_title(title, color='white', fontsize=14, pad=10)
        plt.tight_layout(pad=0)
        plt.savefig(output_path, dpi=150, facecolor=bg, bbox_inches='tight')
        plt.close()
        print(f"✓ {output_path}")
        return True
    except Exception as e:
        print(f"✗ {stl_path}: {e}")
        return False

# Good representative parts across all subsystems
parts_to_render = [
    ("fuselage/fuselage_shell.stl",        "Fuselage Shell",            '#3b82f6'),
    ("emitters/emitter_assembly.stl",      "Emitter Assembly (9 wire posts)", '#ef4444'),
    ("emitters/emitter_razor_ring.stl",     "Razor Ring Emitter",        '#f59e0b'),
    ("collectors/electroplated_collector.stl","Electroplated Collector",  '#10b981'),
    ("collectors/collector_with_frame.stl", "Collector + Frame",        '#8b5cf6'),
    ("frame/spine_assembly.stl",            "Full Spine Assembly",       '#06b6d4'),
    ("guards/duct_with_struts.stl",         "Ducted Frame",              '#ec4899'),
]

colors = ['#3b82f6','#ef4444','#f59e0b','#10b981','#8b5cf6','#06b6d4','#ec4899']

for i, (rel_path, title, color) in enumerate(parts_to_render):
    stl_path = os.path.join(workspace, rel_path)
    if os.path.exists(stl_path):
        out_path = os.path.join(output_dir, f"preview_{i+1}.png")
        render_stl_to_png(stl_path, out_path, title, color=color, elevation=25, azimuth=35+i*15)
    else:
        print(f"NOT FOUND: {stl_path}")

print("\nDone!")