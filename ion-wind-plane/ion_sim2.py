#!/usr/bin/env python3
"""Ion Wind Simulator - Wider exploration including K sensitivity and gap analysis"""
import math
import json
from datetime import datetime

K = 0.25
RHO_SEA = 1.225
H_SCALE = 8500
CD_P = 0.02
E_OSW = 0.8
EPS0 = 8.854e-12
RHO_AIR = 1.225

def calc_rho(h_m):
    return RHO_SEA * math.exp(-h_m / H_SCALE)

def calc_thrust(V_kv, d_mm, L_m, sawtooth=False):
    if V_kv <= 0 or d_mm <= 0 or L_m <= 0:
        return 0.0
    raw = K * (V_kv ** 2) / (d_mm ** 2) * L_m
    return raw * 1.28 if sawtooth else raw

def calc_thrust_vaddi(V_kv, d_mm, L_m, mu=1.4e-4, r_e_mm=0.125):
    if V_kv <= 0 or d_mm <= 0 or L_m <= 0 or mu <= 0:
        return 0.0
    E = (V_kv * 1000) / d_mm
    A = math.pi * d_mm * L_m
    F_N = (EPS0 * RHO_AIR * mu * E * E * A * L_m) / d_mm
    return max(F_N * 1000, 0)

def calc_drag(weightN, rho, V_ms, S_m2, AR):
    D_p = 0.5 * rho * V_ms**2 * CD_P * S_m2
    D_i = (weightN**2) / (0.5 * rho * V_ms**2 * math.pi * AR * E_OSW)
    return D_p, D_i, D_p + D_i

def calc_cruise_velocity(thrustN, weightN, rho, S_m2, AR):
    if thrustN <= 0:
        return 0.0
    V = 1.0
    for i in range(500):
        D_p, D_i, D_t = calc_drag(weightN, rho, V, S_m2, AR)
        f = D_t - thrustN
        denom = 0.5 * rho * V * (2 * CD_P * S_m2 +
                  (2 * weightN * weightN) / (0.5 * rho * V**3 * math.pi * AR * E_OSW))
        if abs(denom) < 1e-12:
            break
        V -= f / denom
        if V < 0.1:
            V = 0.1
        if abs(f) < 1e-9:
            break
    return max(V, 0.1)

def evaluate(b_mm, c_mm, L_mm, V_kv, d_mm, h_m, W_g,
             elec_type='smooth', mu=1.4e-4, r_e_mm=0.125):
    b_m = b_mm / 1000
    c_m = c_mm / 1000
    L_m = L_mm / 1000
    S = b_m * c_m
    AR = (b_m**2) / S if S > 0 else 0
    rho = calc_rho(h_m)
    W_N = (W_g / 1000) * 9.81

    sawtooth = elec_type == 'sawtooth'
    T_s = calc_thrust(V_kv, d_mm, L_m, sawtooth=False)
    T_st = calc_thrust(V_kv, d_mm, L_m, sawtooth=True)
    T_v = calc_thrust_vaddi(V_kv, d_mm, L_m, mu, r_e_mm)
    T = T_st if sawtooth else T_s
    T_N = T / 1000

    V_c = calc_cruise_velocity(T_N, W_N, rho, S, AR)
    D_p, D_i, D_t = calc_drag(W_N, rho, V_c, S, AR)

    TW = T_N / W_N if W_N > 0 else 0
    LD = W_N / D_t if D_t > 0 else 0

    viable = (TW >= 1.0) and (LD >= 8.0) and (0.5 <= V_c <= 5.0)

    return {
        'b': b_mm, 'c': c_mm, 'L': L_mm, 'V': V_kv, 'd': d_mm,
        'h': h_m, 'W': W_g, 'elec': elec_type,
        'T_emp': round(T_s, 3), 'T_emp_st': round(T_st, 3),
        'T_vaddi': round(T_v, 3), 'T_N': T_N,
        'W_N': W_N, 'V_c': V_c, 'D_t': D_t*1000,
        'TW': round(TW, 5), 'glide': round(LD, 3),
        'AR': round(AR, 2), 'S': round(S, 5), 'rho': round(rho, 4),
        'viable': viable
    }

print("="*70)
print("ION WIND AIRCRAFT - EXTENDED ANALYSIS")
print(f"Started: {datetime.now()}")
print("="*70)

# First: verify MIT reference
print("\n--- MIT Reference Verification ---")
mit = evaluate(5000, 500, 5000, 75, 25, 0, 2500)
print(f"MIT (5000mm, 75kV, 25mm, 2500g, smooth):")
print(f"  T_emp = {mit['T_emp']} mN ({mit['T_emp']/1000:.4f} N)")
print(f"  T_vaddi = {mit['T_vaddi']} mN")
print(f"  T/W = {mit['TW']}, Glide = {mit['glide']}")
print(f"  V_c = {mit['V_c']:.2f} m/s")
print(f"  Viable = {mit['viable']}")

mit_st = evaluate(5000, 500, 5000, 75, 25, 0, 2500, elec_type='sawtooth')
print(f"MIT sawtooth: T={mit_st['T_emp_st']} mN, T/W={mit_st['TW']}")

# Check arcing constraint: E = V/d. Air breaks down at ~3MV/m
# At 80kV/3mm: E = 80kV/3mm = 26.67 MV/m (well below 3 MV/m breakdown... wait)
# Actually air breaks down at ~3 MV/m, not 3 MV/m... let me recalculate
# 80kV/3mm = 80000/0.003 = 26.67 MV/m = 26.67e6 V/m >> 3e6 V/m → ARCING!
# Minimum gap to avoid arcing at 80kV: d = 80kV/3MV = 80/3 = 26.7mm
# At 80kV with 26.7mm gap: E = 3 MV/m (at breakdown threshold)
# At 40kV with 13.3mm: E = 3 MV/m
# So realistic minimum gaps: at 80kV → 27mm min, at 40kV → 13mm min
print("\n--- Arcing Analysis ---")
for V in [40, 60, 80]:
    d_min = V / 3.0  # mm, to stay below 3 MV/m
    print(f"  {V}kV: min gap to avoid arcing = {d_min:.1f}mm (E=3MV/m)")
    T_at_min = calc_thrust(V, d_min, 0.5, sawtooth=False)
    print(f"    Thrust at min gap (L=500mm): {T_at_min:.2f} mN")

# K sensitivity: what K would make DIY flight viable?
print("\n--- K Sensitivity Analysis ---")
# Target: T/W=1 for W=100g at 80kV, d=27mm (min arcing-free)
W_target = 0.1 * 9.81  # N for 100g
for K_test in [0.25, 1.0, 5.0, 10.0, 25.0, 50.0, 100.0]:
    T_test = K_test * (80**2) / (27**2) * 0.5  # L=500mm=0.5m
    TW_test = (T_test/1000) / W_target
    print(f"  K={K_test}: T={T_test:.1f}mN, T/W={TW_test:.3f}")

# Grid search with K=0.25 across full param space (with arcing constraint)
print("\n--- Full Grid Search (K=0.25, arcing-free) ---")
print("Constraint: d >= V/3 mm (to stay below 3MV/m)")

all_configs = []

# Coarse grid
for b in [150, 200, 250, 300, 350, 400, 450, 500]:
    for c in [50, 80, 120, 160, 200]:
        for L in [100, 200, 300, 400]:
            for V in [20, 30, 40, 50, 60, 80]:
                for W in [50, 100, 150, 200, 300]:
                    # Arcing constraint
                    d_min = V / 3.0
                    for d in [max(3, d_min), max(20, d_min), max(30, d_min)]:
                        if d < d_min:
                            continue
                        for h in [0, 500, 1000]:
                            for et in ['smooth', 'sawtooth']:
                                r = evaluate(b, c, L, V, d, h, W, et)
                                if r['T_emp'] > 0:
                                    all_configs.append(r)

viable = [r for r in all_configs if r['viable']]
print(f"Total configs evaluated: {len(all_configs)}")
print(f"Viable configs (T/W>=1, glide>=8, V_c 0.5-5 m/s): {len(viable)}")

if viable:
    viable.sort(key=lambda x: x['TW'], reverse=True)
    best = viable[0]
    print(f"\nBest viable:")
    print(f"  b={best['b']}mm c={best['c']}mm L={best['L']}mm V={best['V']}kV d={best['d']}mm W={best['W']}g {best['elec']}")
    print(f"  T={best['T_emp']}mN (smooth), T_st={best['T_emp_st']}mN (sawtooth)")
    print(f"  T/W={best['TW']}, Glide={best['glide']}, V_c={best['V_c']:.2f}m/s")
    print(f"  Viable: {best['viable']}")
else:
    print("\nNO VIABLE CONFIGURATIONS FOUND with K=0.25")
    print("Showing best approximations (highest T/W):")

    # Sort by TW
    all_configs.sort(key=lambda x: x['TW'], reverse=True)
    top10 = all_configs[:20]
    for r in top10:
        print(f"  b={r['b']} c={r['c']} L={r['L']} V={r['V']}kV d={r['d']}mm W={r['W']}g {r['elec']}")
        print(f"    T={r['T_emp']}mN TW={r['TW']} glide={r['glide']} V_c={r['V_c']:.2f}m/s")

# Also show what the model predicts for MIT
print("\n--- MIT Reference with different interpretations ---")
# Different chord and electrode lengths
for mit_c in [200, 500, 1000]:
    for mit_L in [1000, 3000, 5000]:
        r = evaluate(5000, mit_c, mit_L, 75, 25, 0, 2500)
        print(f"MIT c={mit_c}mm L={mit_L}mm: T={r['T_emp']:.1f}mN TW={r['TW']:.5f} glide={r['glide']:.2f}")

# Show Vaddi results for MIT
print("\n--- Vaddi Model: MIT Reference ---")
r_vaddi = evaluate(5000, 500, 5000, 75, 25, 0, 2500)
print(f"Vaddi T = {r_vaddi['T_vaddi']:.3f} mN")
print(f"Empirical T = {r_vaddi['T_emp']:.1f} mN")
print(f"Ratio (emp/vaddi) = {r_vaddi['T_emp']/max(r_vaddi['T_vaddi'],0.001):.1f}x")

# Vaddi for DIY range
print("\n--- Vaddi Model: DIY Range ---")
for V in [40, 60, 80]:
    for d in [3, 20, 30]:
        r = evaluate(300, 80, 200, V, d, 0, 100)
        print(f"V={V}kV d={d}mm DIY: Vaddi T={r['T_vaddi']:.3f}mN, Emp T={r['T_emp']:.2f}mN")

# Show what T/W is achievable with K=0.25
print("\n--- Max Achievable T/W (K=0.25, sea level) ---")
# Use minimum arcing-free gap at max voltage
V_max = 80
d_min = V_max / 3.0  # 26.7mm
L_max = 500  # max electrode mm
for W in [50, 100, 200, 300, 500]:
    T = calc_thrust(V_max, d_min, L_max/1000, sawtooth=True)  # sawtooth max
    TW = (T/1000) / ((W/1000)*9.81)
    print(f"  W={W}g: T={T:.1f}mN, T/W={TW:.5f} (needs >=1.0 for flight)")

print(f"\nFinished: {datetime.now()}")
