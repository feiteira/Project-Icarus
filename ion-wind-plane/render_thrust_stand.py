#!/usr/bin/env python3
"""Render STL files to PNG images — Thrust Stand focused previews."""

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

def render_stl_to_png(stl_path, output_path, title="", subtitle="", color='#3498db', bg='#0a0e17', elevation=30, azimuth=45):
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
            ax.set_title(title, color='white', fontsize=16, pad=12)
        plt.tight_layout(pad=0)
        plt.savefig(output_path, dpi=150, facecolor=bg, bbox_inches='tight')
        plt.close()
        print(f"OK {output_path}")
        return True
    except Exception as e:
        print(f"ERR {stl_path}: {e}")
        return False

# Thrust Stand — relevant parts only (Option A build order)
parts = [
    # (stl_rel_path, title, subtitle, color, elevation, azimuth)
    ("emitters/emitter_frame.stl",       "Emitter Wire Frame",         "Holds the thin wire taut between two posts — acrylic structure", '#ef4444', 25, 35),
    ("emitters/wire_support_post.stl", "Wire Support Post",          "One of 9 posts that hold the emitter wire in tension", '#ef4444', 20, 45),
    ("collectors/collector_mount_frame.stl", "Collector Mount Frame",  "Holds the collector foil parallel to the emitter wire", '#10b981', 25, 35),
    ("collectors/adjustable_mount.stl", "Adjustable Gap Mount",       "Slide mount for tuning electrode gap (10-40mm range)", '#10b981', 20, 50),
    ("frame/spine_segment.stl",         "Spine Segment",             "Structural spine node — connects to acrylic base", '#06b6d4', 25, 35),
    ("frame/node_junction.stl",           "Spine Junction Node",        "Joins two spine segments at 90 degrees", '#06b6d4', 20, 45),
    ("fuselage/fuselage_shell.stl",       "Fuselage Shell",             "Hollow shell — holds battery bay + HV module in nose", '#8b5cf6', 25, 35),
    ("collectors/collector_plate.stl",  "Collector Foil Plate",       "Flat copper/aluminum foil on acrylic — Option A collector", '#10b981', 20, 40),
    ("guards/duct_ring.stl",             "Duct Ring",                  "Hollow ring — optional duct for ducted tandem (Option B)", '#ec4899', 25, 35),
]

for i, (rel_path, title, subtitle, color, elev, azim) in enumerate(parts):
    stl_path = os.path.join(workspace, rel_path)
    out_path = os.path.join(output_dir, f"ts_{i+1}.png")
    if os.path.exists(stl_path):
        render_stl_to_png(stl_path, out_path, title, subtitle, color=color, elevation=elev, azimuth=azim)
    else:
        print(f"MISSING: {stl_path}")

print("\nThrust Stand previews complete!")
