#!/usr/bin/env python3
import numpy as np, matplotlib.pyplot as plt, matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, Polygon, Ellipse, Arc
import matplotlib.lines as mlines

fig, ax = plt.subplots(1, 1, figsize=(14, 8))
ax.set_xlim(0, 14)
ax.set_ylim(0, 8)
ax.set_aspect('equal')
ax.axis('off')
ax.set_facecolor('#0f1923')

# ---- COLORS ----
bg = '#0f1923'
white = '#e6e6e6'
fuselage_col = '#3498db'
wing_col = '#27ae60'
tail_col = '#9b59b6'
emitter_col = '#e74c3c'
collector_col = '#f39c12'
electronics_col = '#95a5a6'
stringer_col = '#7f8c8d'

# ============================================
# TOP VIEW (upper half)
# ============================================
ax_top = fig.add_axes([0.05, 0.52, 0.9, 0.43])
ax_top.set_xlim(0, 14)
ax_top.set_ylim(0, 7)
ax_top.set_aspect('equal')
ax_top.axis('off')
ax_top.set_facecolor(bg)

# Wings (top view - elongated ellipses)
wing_left = Ellipse((5, 3.5), 5, 0.6, angle=0, facecolor=wing_col, alpha=0.8, edgecolor=white, linewidth=0.5)
wing_right = Ellipse((9, 3.5), 5, 0.6, angle=0, facecolor=wing_col, alpha=0.8, edgecolor=white, linewidth=0.5)
ax_top.add_patch(wing_left)
ax_top.add_patch(wing_right)

# Fuselage (top view)
ax_top.add_patch(Ellipse((7, 3.5), 3, 0.5, facecolor=fuselage_col, alpha=0.9, edgecolor=white, linewidth=1))

# Emitter line along wing leading edge
ax_top.plot([2.5, 5.5], [3.5, 3.5], color=emitter_col, linewidth=2, label='Emitter wire')
ax_top.plot([8.5, 11.5], [3.5, 3.5], color=emitter_col, linewidth=2)

# Collector strips on wing trailing edge
ax_top.plot([5.5, 6.5], [3.5, 3.5], color=collector_col, linewidth=4, solid_capstyle='round')
ax_top.plot([7.5, 8.5], [3.5, 3.5], color=collector_col, linewidth=4, solid_capstyle='round')

# Tail (top view)
ax_top.plot([8.5, 11], [3.5, 3.5], color=stringer_col, linewidth=1.5)
ax_top.add_patch(Ellipse((11, 3.5), 0.8, 2, facecolor=tail_col, alpha=0.7, edgecolor=white, linewidth=0.5))

# Battery (18650 shown as rectangle)
ax_top.add_patch(FancyBboxPatch((6.2, 3.3), 0.6, 0.4, boxstyle="round,pad=0.05", 
                                 facecolor=electronics_col, edgecolor=white, linewidth=0.5))
ax_top.text(6.5, 3.5, '18650', fontsize=6, color=white, ha='center', va='center')

# Label
ax_top.set_title("TOP VIEW — Ion Wing Prototype", color=white, fontsize=11, pad=6)
ax_top.text(0.3, 6.5, "Wingspan: ~300mm\nWeight: ~180g\nBatt: 1× 18650", color=white, fontsize=7)

# ============================================
# SIDE VIEW (lower half)  
# ============================================
ax_side = fig.add_axes([0.05, 0.05, 0.9, 0.43])
ax_side.set_xlim(0, 14)
ax_side.set_ylim(0, 5)
ax_side.set_aspect('equal')
ax_side.axis('off')
ax_side.set_facecolor(bg)

# Fuselage body (side view)
fuselage_pts = [(5.5, 2), (6.5, 2), (7.2, 2.8), (8.5, 3), (8.5, 2), (9.5, 1.5), (9.5, 2.5), (8.5, 3), (7.5, 2.8)]
fuselage_body = Polygon(fuselage_pts, facecolor=fuselage_col, edgecolor=white, linewidth=1, alpha=0.9)
ax_side.add_patch(fuselage_body)

# Wing (side - thin profile)
ax_side.plot([2, 6.5], [3.5, 3], color=wing_col, linewidth=3, solid_capstyle='round')
ax_side.plot([7.5, 11.5], [3, 3.5], color=wing_col, linewidth=3, solid_capstyle='round')

# Emitter wire (above wing)
ax_side.plot([2, 6.5], [4.5, 3.5], color=emitter_col, linewidth=1.5, linestyle='--')
ax_side.plot([7.5, 11.5], [3.5, 4.5], color=emitter_col, linewidth=1.5, linestyle='--')

# Collector strip (below wing)
ax_side.plot([2, 6.5], [2.5, 2.5], color=collector_col, linewidth=2)
ax_side.plot([7.5, 11.5], [2.5, 2.5], color=collector_col, linewidth=2)

# Arrow showing thrust direction (ion wind pushes backward = plane moves forward)
ax_side.annotate('', xy=(11.8, 3), xytext=(10.8, 3),
                 arrowprops=dict(arrowstyle='->', color='#00d4ff', lw=2))
ax_side.text(11.5, 2.6, '→ Thrust', color='#00d4ff', fontsize=7)

# Tail fin (side)
ax_side.plot([10, 10.5], [3, 4.5], color=tail_col, linewidth=3)

# Battery inside fuselage
ax_side.add_patch(FancyBboxPatch((7, 2.1), 0.7, 0.3, boxstyle="round,pad=0.03",
                                 facecolor=electronics_col, edgecolor=white, linewidth=0.5))
ax_side.text(7.35, 2.25, 'BAT', fontsize=5, color=bg, ha='center', va='center')

# HV electronics module
ax_side.add_patch(FancyBboxPatch((6.5, 2.4), 0.4, 0.25, boxstyle="round,pad=0.02",
                                 facecolor='#e67e22', edgecolor=white, linewidth=0.3))
ax_side.text(6.7, 2.52, 'HV', fontsize=4, color=bg, ha='center', va='center')

# Label
ax_side.set_title("SIDE VIEW — Ion Wind Propulsion", color=white, fontsize=11, pad=6)

# Arrows showing ion flow
ax_side.annotate('', xy=(5, 2.5), xytext=(3, 4),
                 arrowprops=dict(arrowstyle='->', color=emitter_col, lw=1.5))
ax_side.text(3.5, 3.5, 'Ionize', color=emitter_col, fontsize=6)

ax_side.annotate('', xy=(5, 2.5), xytext=(7, 2.5),
                 arrowprops=dict(arrowstyle='->', color=collector_col, lw=1.5))
ax_side.text(5.5, 2.2, '→ Collect', color=collector_col, fontsize=6)

# Air flow arrows
ax_side.annotate('', xy=(1, 3.5), xytext=(0, 3.5),
                 arrowprops=dict(arrowstyle='->', color=white, lw=1, linestyle='dashed'))
ax_side.text(0.3, 3.2, 'Air', color=white, fontsize=6)

# Main title
fig.suptitle("Mini Ion Wing — Conceptual Design", color=white, fontsize=16, y=0.97, fontweight='bold')

# Legend
legend_items = [
    mpatches.Patch(color=wing_col, label='Wing (ionization zone)'),
    mpatches.Patch(color=fuselage_col, label='Fuselage'),
    mpatches.Patch(color=emitter_col, label='Emitter wire (HV)'),
    mpatches.Patch(color=collector_col, label='Collector strip'),
    mpatches.Patch(color=tail_col, label='Tail stabilizer'),
    mlines.Line2D([], [], color='#00d4ff', linestyle='-', linewidth=2, label='Thrust direction'),
]
fig.legend(handles=legend_items, loc='lower right', fontsize=8, 
           framealpha=0.3, facecolor='#1a1a2e', edgecolor=white, labelcolor=white,
           ncol=3, bbox_to_anchor=(0.98, 0.01))

plt.savefig('/home/feiteira/.openclaw/workspace/ion-wind-plane/previews/concept.png', 
            dpi=150, facecolor=bg, bbox_inches='tight')
plt.close()
print("Concept render done: previews/concept.png")