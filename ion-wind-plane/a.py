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

def load_stl(filepath):
    return read_stl_vertices(filepath)

base = "/home/feiteira/.openclaw/workspace/ion-wind-plane"

# Load all major components
parts = {
    "Fuselage": (load_stl(f"{base}/fuselage/fuselage_shell.stl"), '#3498db'),
    "Battery Bay": (load_stl(f"{base}/fuselage/battery_bay.stl"), '#2980b9'),
    "HV Module": (load_stl(f"{base}/fuselage/hv_module_bay.stl"), '#1a5276'),
    "Emitter Array": (load_stl(f"{base}/emitters/emitter_assembly.stl"), '#e74c3c'),
    "Collectors": (load_stl(f"{base}/collectors/collector_with_frame.stl"), '#2ecc71'),
    "Spine": (load_stl(f"{base}/frame/spine_assembly.stl"), '#9b59b6'),
    "Duct": (load_stl(f"{base}/guards/duct_with_struts.stl"), '#f39c12'),
}

fig = plt.figure(figsize=(14, 9), facecolor='#0d1117')
ax = fig.add_subplot(111, projection='3d', facecolor='#0d1117')

# Position transforms for each part to approximate assembly layout
# rough placement - spine is central, fuselage above, emitters/collectors flanking
transforms = {
    "Fuselage":     (np.array([0, 0, 30]),  0.8),
    "Battery Bay":  (np.array([0, 0, 28]),  0.7),
    "HV Module":    (np.array([0, 0, 32]),  0.8),
    "Emitter Array":(np.array([0, -60, 0]), 0.6),
    "Collectors":   (np.array([0, 60, 0]),   0.6),
    "Spine":       (np.array([0, 0, 0]),     1.0),
    "Duct":        (np.array([0, -30, -10]), 0.7),
}

for name, (verts, color) in parts.items():
    offset, scale = transforms[name]
    v = verts * scale + offset
    faces = [v[:, 0], v[:, 1], v[:, 2]]
    mesh = Poly3DCollection(faces, alpha=0.92, facecolor=mcolors.to_rgba(color), 
                             edgecolor='#1a1a2e', linewidth=0.05)
    ax.add_collection3d(mesh)

# Compute bounds
all_v = []
for name, (verts, _) in parts.items():
    offset, scale = transforms[name]
    all_v.append(verts * scale + offset)
all_v = np.concatenate(all_v).reshape(-1, 3)
max_range = np.ptp(all_v, axis=0).max()
mid = all_v.mean(axis=0)
ax.set_xlim(mid[0]-max_range/2*1.1, mid[0]+max_range/2*1.1)
ax.set_ylim(mid[1]-max_range/2*1.1, mid[1]+max_range/2*1.1)
ax.set_zlim(mid[2]-max_range/2*1.1, mid[2]+max_range/2*1.1)

ax.set_box_aspect([1.2, 1.8, 0.5])
ax.axis('off')
ax.view_init(elev=20, azim=30)

ax.set_title("Ion Wind Aircraft — Full Assembly Preview", color='white', fontsize=14, pad=12)

# Legend
legend_colors = ['#3498db', '#2980b9', '#1a5276', '#e74c3c', '#2ecc71', '#9b59b6', '#f39c12']
legend_labels = list(parts.keys())
for i, (color, label) in enumerate(zip(legend_colors, legend_labels)):
    ax.scatter([], [], [], c=color, label=label)
ax.legend(loc='upper right', fontsize=9, framealpha=0.3, labelcolor='white', 
          facecolor='#1a1a2e', edgecolor='white')

plt.tight_layout(pad=0)
plt.savefig(f"{base}/previews/assembly.png", dpi=150, facecolor='#0d1117', bbox_inches='tight')
plt.close()
print("Assembly rendered: previews/assembly.png")