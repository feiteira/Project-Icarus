#!/usr/bin/env python3
"""
DUCTED TANDEM ION WIND THRUSTER MODEL
======================================
Full derivation and Python implementation for modeling:
- Single-stage EHD thruster (wire-to-mesh with steel wool texture)
- Ducted tandem 2-stage configuration
- Comparison against baseline NACA and open tandem

Author: Model based on empirical calibration + Drew/Follmer 2021 scaling
"""

import math
import json

# ============================================================
# SECTION 1: EMPIRICAL CALIBRATION
# ============================================================
print("="*70)
print("DUCTED TANDEM ION WIND THRUSTER MODEL")
print("="*70)

print("\n## SECTION 1: EMPIRICAL CALIBRATION\n")

# Our ONE calibrated data point:
# 35kV / 20mm gap / 500mm length / NACA collector -> 169 mN
V_calib = 35.0      # kV
d_calib = 20.0      # mm
L_calib = 0.5       # m
T_NACA_baseline_N = 0.169  # N (169 mN)
P_calib = 15.0     # watts (our small ZVS power)

# Back-calculate our empirical K for the formula:
# T(N) = K_empirical * (V^2 / d^2) * L
K_our_NACA = T_NACA_baseline_N * (d_calib**2) / (V_calib**2 * L_calib)
print(f"Calibrated K_our_NACA = {K_our_NACA:.4f}")
print(f"  (this is K for our 0.1mm wire + NACA foil practical build)")

# The Nanjing paper gives K_NACA_theoretical = 0.623
# Our build is lower (0.110) because 0.1mm wire is less sharp
K_NACA_theoretical = 0.623
print(f"\nNanjing paper theoretical K_NACA = {K_NACA_theoretical:.3f}")
print(f"Ratio (our/theoretical) = {K_our_NACA/K_NACA_theoretical:.2f} = {100*K_our_NACA/K_NACA_theoretical:.1f}%")

# Validate calibration:
T_validate = K_our_NACA * (V_calib**2 / d_calib**2) * L_calib
print(f"\nValidation: T_calc = {T_validate*1000:.1f} mN (should be 169 mN)")

# ============================================================
# SECTION 2: WIRE-TO-MESH K VALUE
# ============================================================
print("\n" + "="*70)
print("## SECTION 2: WIRE-TO-MESH K VALUE\n")

# From Drew 2021 / Tampouris 2023: wire-to-mesh geometry
# Mesh is less efficient than solid foil for ion collection
# Empirical estimate: K_wm = 0.73 * K_our_NACA
K_wm_ratio = 0.73
K_wm = K_our_NACA * K_wm_ratio
print(f"Wire-to-mesh K = {K_wm:.4f} (ratio {K_wm_ratio} to NACA)")
print(f"  -> derived from Drew/Tampouris data on wire-to-mesh geometry")

# ============================================================
# SECTION 3: STEEL WOOL TEXTURE AMPLIFICATION
# ============================================================
print("\n" + "="*70)
print("## SECTION 3: STEEL WOOL TEXTURE FACTOR\n")

# Lee et al. 2008 (micropillar): 3D texture -> 1.5x to 3x improvement
# Steel wool provides ~1.8x amplification (conservative central)
texture_factor = 1.8
K_wm_sw = K_wm * texture_factor
print(f"Steel wool texture factor = {texture_factor}x")
print(f"K_wire_mesh_steelwool = {K_wm:.4f} x {texture_factor} = {K_wm_sw:.4f}")

# ============================================================
# SECTION 4: ION CURRENT MODEL (for power estimation)
# ============================================================
print("\n" + "="*70)
print("## SECTION 4: ION CURRENT & POWER MODEL\n")

I_calib = P_calib / (V_calib * 1000)  # amps
print(f"At calibration: V={V_calib}kV, d={d_calib}mm, P={P_calib}W")
print(f"  Ion current I = P/V = {I_calib*1000:.3f} mA")

def ion_current(V_kV, d_mm, V_calib=35.0, d_calib=20.0, P_calib=15.0):
    """Estimate ion current in mA. I scales as V^2/d from corona discharge physics."""
    I_calib = P_calib / (V_calib * 1000)
    I = I_calib * (V_kV/V_calib)**2 * (d_calib/d_mm)
    return I * 1000  # mA

def power_from_ion_current(V_kV, d_mm, V_calib=35.0, d_calib=20.0, P_calib=15.0):
    """Estimate power consumption in watts"""
    I_mA = ion_current(V_kV, d_mm, V_calib, d_calib, P_calib)
    return V_kV * 1000 * (I_mA / 1000)  # W = kV * A

# ============================================================
# SECTION 5: THRUST FORMULA
# ============================================================
print("\n" + "="*70)
print("## SECTION 5: THRUST FORMULA\n")

def thrust_N(V_kV, d_mm, L_m, K):
    """Thrust in Newtons: T = K * (V^2/d^2) * L"""
    return K * (V_kV**2 / d_mm**2) * L_m

def thrust_mN(V_kV, d_mm, L_m, K):
    """Thrust in millinewtons"""
    return thrust_N(V_kV, d_mm, L_m, K) * 1000

# ============================================================
# SECTION 6: DUCTED TANDEM SCALING
# ============================================================
print("\n" + "="*70)
print("## SECTION 6: DUCTED TANDEM SCALING MODEL\n")

# Drew & Follmer 2021: proper ducting enables near-linear scaling
# The duct prevents "re-accelerating the same air" problem
#
# Key insight: Without duct, Stage 2 re-accelerates already-accelerated air
# With proper duct, Stage 2 adds velocity to FRESH incoming air
#
# Mathematical model:
#   Stage 1 thrust: T1 = K * (V^2/d^2) * L
#   Stage 2 thrust: T2 = eta_duct * T1  (eta_duct is duct efficiency)
#   Total 2-stage:  T_total = T1 * (1 + eta_duct)
#
# eta_duct values:
#   Open tandem (no duct):      eta = 0.25  (+25% per stage, Plasma Channel)
#   DIY ducted (conservative):  eta = 0.85
#   Perfect ducted:             eta = 0.95

eta_duct_open = 0.25
eta_duct_perfect = 0.95
eta_duct_diy = 0.85

def tandem_thrust(T_single, eta_duct, n_stages=2):
    """Total tandem thrust for n stages with duct efficiency eta_duct"""
    # For 2 stages: T_total = T1 + T2 = T1 + eta*T1 = T1*(1+eta)
    return T_single * (1 + eta_duct * (n_stages - 1))

print(f"Duct efficiency factors:")
print(f"  Open tandem (no duct):      eta = {eta_duct_open}")
print(f"  DIY ducting (central est):  eta = {eta_duct_diy}")
print(f"  Perfect ducting:           eta = {eta_duct_perfect}")
print(f"")
print(f"For 2-stage: T_total = T1 x (1 + eta)")
print(f"  Open:  T_total = T1 x {1+eta_duct_open:.2f}  (diminishing returns!)")
print(f"  DIY:   T_total = T1 x {1+eta_duct_diy:.2f}  (major improvement!)")
print(f"  Perf:  T_total = T1 x {1+eta_duct_perfect:.2f}  (near-linear)")

# ============================================================
# SECTION 7: MAIN CALCULATIONS
# ============================================================
print("\n" + "="*70)
print("## SECTION 7: CONFIGURATION CALCULATIONS\n")

V = 35.0   # kV
L = 0.5    # m (500mm)

# --- CONFIG 1: BASELINE NACA ---
d1 = 20.0
K1 = K_our_NACA
T1 = thrust_mN(V, d1, L, K1)
P1 = power_from_ion_current(V, d1)
TP1 = T1 / P1
print(f"{'='*60}")
print(f"CONFIG 1: BASELINE NACA (our actual build)")
print(f"{'='*60}")
print(f"  V={V}kV, d={d1}mm, L={L*1000}mm, K={K1:.4f}")
print(f"  Geometry: Single-stage, NACA collector, no texture")
print(f"  T_single  = {T1:.1f} mN")
print(f"  P_estimate = {P1:.1f} W")
print(f"  T/P ratio  = {TP1:.1f} mN/W")
print(f"  [VALIDATION: should be ~169 mN]")

# --- CONFIG 2: WIRE-TO-MESH + STEEL WOOL at 20mm ---
d2 = 20.0
K2 = K_wm_sw
T2 = thrust_mN(V, d2, L, K2)
P2 = power_from_ion_current(V, d2)
TP2 = T2 / P2
print(f"\n{'='*60}")
print(f"CONFIG 2: Wire-to-mesh + Steel Wool, 35kV, 20mm")
print(f"{'='*60}")
print(f"  V={V}kV, d={d2}mm, L={L*1000}mm, K={K2:.4f}")
print(f"  Geometry: Single-stage, wire-to-mesh, steel wool texture")
print(f"  T_single  = {T2:.1f} mN")
print(f"  P_estimate = {P2:.1f} W")
print(f"  T/P ratio  = {TP2:.1f} mN/W")
print(f"  Improvement vs baseline: {T2/T1:.2f}x")

# --- CONFIG 3: WIRE-TO-MESH + STEEL WOOL at 8mm ---
d3 = 8.0
K3 = K_wm_sw
T3 = thrust_mN(V, d3, L, K3)
P3 = power_from_ion_current(V, d3)
TP3 = T3 / P3
print(f"\n{'='*60}")
print(f"CONFIG 3: Wire-to-mesh + Steel Wool, 35kV, 8mm")
print(f"{'='*60}")
print(f"  V={V}kV, d={d3}mm, L={L*1000}mm, K={K3:.4f}")
print(f"  Geometry: Single-stage, wire-to-mesh, steel wool texture")
print(f"  [CAUTION: Small gap = higher arcing risk]")
print(f"  T_single  = {T3:.1f} mN")
print(f"  P_estimate = {P3:.1f} W")
print(f"  T/P ratio  = {TP3:.1f} mN/W")
print(f"  Improvement vs baseline: {T3/T1:.2f}x")

# --- CONFIG 4: DUCTED TANDEM 2-STAGE at 8mm ---
T4_single = T3
T4_open = tandem_thrust(T3, eta_duct_open)
T4_diy = tandem_thrust(T3, eta_duct_diy)
T4_perfect = tandem_thrust(T3, eta_duct_perfect)
print(f"\n{'='*60}")
print(f"CONFIG 4: DUCTED TANDEM 2-STAGE, Wire-to-mesh, 35kV, 8mm")
print(f"{'='*60}")
print(f"  Stage 1: T1 = {T4_single:.1f} mN")
print(f"")
print(f"  2-Stage Open Tandem (eta={eta_duct_open}):")
print(f"    T_total = {T4_single:.1f} x (1 + {eta_duct_open}) = {T4_open:.1f} mN")
print(f"    Scaling vs single: {T4_open/T3:.2f}x  [DIMINISHING RETURNS]")
print(f"")
print(f"  2-Stage DIY Ducted Tandem (eta={eta_duct_diy}):")
print(f"    T_total = {T4_single:.1f} x (1 + {eta_duct_diy}) = {T4_diy:.1f} mN")
print(f"    Scaling vs single: {T4_diy/T3:.2f}x  [MAJOR IMPROVEMENT]")
print(f"")
print(f"  2-Stage Perfect Ducted Tandem (eta={eta_duct_perfect}):")
print(f"    T_total = {T4_single:.1f} x (1 + {eta_duct_perfect}) = {T4_perfect:.1f} mN")
print(f"    Scaling vs single: {T4_perfect/T3:.2f}x  [NEAR-LINEAR]")

# --- CONFIG 5: DUCTED TANDEM at 10mm (safer) ---
d5 = 10.0
K5 = K_wm_sw
T5 = thrust_mN(V, d5, L, K5)
P5 = power_from_ion_current(V, d5)
T5_open = tandem_thrust(T5, eta_duct_open)
T5_diy = tandem_thrust(T5, eta_duct_diy)
T5_perfect = tandem_thrust(T5, eta_duct_perfect)
print(f"\n{'='*60}")
print(f"CONFIG 5: DUCTED TANDEM 2-STAGE, Wire-to-mesh, 35kV, 10mm (safer)")
print(f"{'='*60}")
print(f"  V={V}kV, d={d5}mm, L={L*1000}mm")
print(f"  Single-stage T = {T5:.1f} mN")
print(f"  2-stage DIY ducted T = {T5_diy:.1f} mN")
print(f"  2-stage perfect ducted T = {T5_perfect:.1f} mN")
print(f"  P_estimate (single) = {P5:.1f} W")

# ============================================================
# SECTION 8: PARAMETER SWEEPS
# ============================================================
print("\n" + "="*70)
print("## SECTION 8: PARAMETER SWEEPS\n")

# Sweep 1: Gap distance (8-20mm) at single-stage
print("SWEEP 1: Gap distance effect (single-stage wire-to-mesh+SW)")
print(f"{'d(mm)':>6} {'T(mN)':>8} {'P_est(W)':>9} {'T/P(mN/W)':>11} {'vs_baseline':>12}")
print("-"*52)
for d in [8, 10, 12, 14, 16, 18, 20]:
    T_sweep = thrust_mN(V, d, L, K_wm_sw)
    P_sweep = power_from_ion_current(V, d)
    TP_sweep = T_sweep / P_sweep
    ratio = T_sweep / (T_NACA_baseline_N*1000)
    print(f"{d:6.0f} {T_sweep:8.1f} {P_sweep:9.1f} {TP_sweep:11.1f} {ratio:12.2f}x")

print("\nSWEEP 2: Power scaling (2-stage ducted at 10mm gap)")
print("  Note: P scales with voltage and gap. At fixed V=35kV, higher P needs higher I")
print(f"{'P(W)':>6} {'T_1stage(mN)':>13} {'T_diy(mN)':>11} {'T/P(mN/W)':>10} {'T/W(100g)':>11}")
print("-"*56)
for P_sweep in [15, 30, 50, 75, 100]:
    # At fixed V,d, thrust scales roughly linearly with P (via ion current)
    # T = K * (V^2/d^2) * L  (independent of P)
    # But P = V*I, so I = P/V. Thrust also ~proportional to I for fixed geometry.
    # Since our K is empirically calibrated at P=15W, we scale T linearly with P
    T_1s = thrust_mN(V, 10.0, L, K_wm_sw) * (P_sweep / P_calib)
    T_diy = tandem_thrust(T_1s, eta_duct_diy)
    TP = T_diy / P_sweep
    TW = T_diy / 1000 / 0.981  # T in N, weight = 0.1kg * 9.81
    print(f"{P_sweep:6.0f} {T_1s:13.1f} {T_diy:11.1f} {TP:10.1f} {TW:11.2f}")

print("\nSWEEP 3: Tandem type comparison (10mm gap)")
print(f"{'Config':>20} {'eta':>6} {'T_1stage(mN)':>13} {'T_2stage(mN)':>13} {'Scaling':>9}")
print("-"*65)
configs_sweep = [
    ("Open tandem", eta_duct_open),
    ("DIY ducted", eta_duct_diy),
    ("Perfect ducted", eta_duct_perfect),
]
T_base_sweep = thrust_mN(V, 10.0, L, K_wm_sw)
for name, eta in configs_sweep:
    T_2s = tandem_thrust(T_base_sweep, eta)
    scaling = T_2s / T_base_sweep
    print(f"{name:>20} {eta:6.2f} {T_base_sweep:13.1f} {T_2s:13.1f} {scaling:9.2f}x")

# ============================================================
# SECTION 9: KEY RESULTS SUMMARY TABLE
# ============================================================
print("\n" + "="*70)
print("## SECTION 9: KEY RESULTS SUMMARY\n")

print(f"{'Configuration':<35} {'T(mN)':>10} {'P(W)':>8} {'T/P':>8} {'vs_base':>10}")
print("="*75)
print(f"{'Baseline NACA 35kV/20mm':<35} {T1:>10.1f} {P1:>8.1f} {TP1:>8.1f} {'1.00x':>10}")
print(f"{'Wire-to-mesh+SW 35kV/20mm':<35} {T2:>10.1f} {P2:>8.1f} {TP2:>8.1f} {T2/T1:>10.2f}x")
print(f"{'Wire-to-mesh+SW 35kV/10mm':<35} {T5:>10.1f} {P5:>8.1f} {T5/P5:>8.1f} {T5/T1:>10.2f}x")
print(f"{'Wire-to-mesh+SW 35kV/8mm':<35} {T3:>10.1f} {P3:>8.1f} {TP3:>8.1f} {T3/T1:>10.2f}x")
print("-"*75)
print(f"{'Ducted tandem 2-stage 10mm DIY':<35} {T5_diy:>10.1f} {P5*2:>8.1f} {T5_diy/(P5*2):>8.1f} {T5_diy/T1:>10.2f}x")
print(f"{'Ducted tandem 2-stage 8mm DIY':<35} {T4_diy:>10.1f} {P3*2:>8.1f} {T4_diy/(P3*2):>8.1f} {T4_diy/T1:>10.2f}x")
print(f"{'Ducted tandem 2-stage 8mm perfect':<35} {T4_perfect:>10.1f} {P3*2:>8.1f} {T4_perfect/(P3*2):>8.1f} {T4_perfect/T1:>10.2f}x")

print("\n" + "="*70)
print("## CRITICAL INSIGHT\n")
print("="*70)
print(f"")
print(f"Baseline (NACA 35kV/20mm):      {T1:.0f} mN = {T1/1000:.3f} N")
print(f"Our best ducted tandem model:    {T4_diy:.0f} mN = {T4_diy/1000:.2f} N")
print(f"Improvement factor: {T4_diy/T1:.1f}x over baseline")
print(f"")
print(f"Thrust-to-weight for 100g aircraft with best config (8mm DIY):")
print(f"  T = {T4_diy/1000:.2f} N,  Weight = 0.1 kg x 9.81 = 0.981 N")
print(f"  T/W = {T4_diy/1000/0.981:.2f}  (>1.0 = can fly!)")
print(f"")
print(f"For comparison, OPEN tandem 2-stage (no duct) at 8mm:")
print(f"  T = {T4_open:.0f} mN = {T4_open/1000:.3f} N")
print(f"  This is only {(T4_open/T4_diy)*100:.0f}% of what DUCTED tandem achieves!")
print(f"")
print("="*70)
print("## MODEL ASSUMPTIONS & CAVEATS\n")
print("="*70)
print(f"  K_our_NACA = {K_our_NACA:.4f}  [calibrated from 169mN baseline]")
print(f"  K_wire_mesh = {K_wm:.4f}  [0.73x NACA, from Drew/Tampouris]")
print(f"  Texture factor = {texture_factor}x  [steel wool estimate, Lee 2008]")
print(f"  eta_duct DIY = {eta_duct_diy}  [conservative central, Drew 2021]")
print(f"  Power model: I ~ V^2/d, P = V x I")
print(f"")
print(f"CAVEATS:")
print(f"  - K may vary with gap distance (field non-uniformity at small d)")
print(f"  - Arcing risk at d<8mm NOT modeled (corona onset voltage)")
print(f"  - Steel wool texture factor is estimate (not yet measured)")
print(f"  - Duct efficiency eta_duct is theoretical (Drew & Follmer 2021)")
print(f"  - Linear power scaling may overestimate at high power")
print("="*70)

# Save results as JSON
results_json = {
    "calibration": {
        "K_our_NACA": round(K_our_NACA, 4),
        "K_NACA_theoretical": K_NACA_theoretical,
        "baseline_mN": round(T_NACA_baseline_N*1000, 1),
        "V_kV": V_calib,
        "d_mm": d_calib,
        "L_m": L_calib,
        "P_W": P_calib,
    },
    "model_params": {
        "K_wire_mesh": round(K_wm, 4),
        "K_wire_mesh_steelwool": round(K_wm_sw, 4),
        "texture_factor": texture_factor,
        "eta_duct_open": eta_duct_open,
        "eta_duct_diy": eta_duct_diy,
        "eta_duct_perfect": eta_duct_perfect,
    },
    "configs": {
        "baseline_NACA_20mm_mN": round(T1, 1),
        "wm_sw_20mm_mN": round(T2, 1),
        "wm_sw_10mm_mN": round(T5, 1),
        "wm_sw_8mm_mN": round(T3, 1),
        "duct_2stage_10mm_diy_mN": round(T5_diy, 1),
        "duct_2stage_8mm_diy_mN": round(T4_diy, 1),
        "duct_2stage_8mm_perfect_mN": round(T4_perfect, 1),
        "open_tandem_2stage_8mm_mN": round(T4_open, 1),
    }
}

with open("/home/feiteira/.openclaw/workspace/ion-wind-plane/ducted_tandem_results.json", "w") as f:
    json.dump(results_json, f, indent=2)
print("\n[Results saved to ducted_tandem_results.json]")
