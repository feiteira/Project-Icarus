#!/usr/bin/env python3
"""Focused: understand what makes V_c converge to 0.10 m/s always"""
import math
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
    raw = K * (V_kv ** 2) / (d_mm ** 2) * L_m
    return raw * 1.28 if sawtooth else raw

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

def evaluate(b_mm, c_mm, L_mm, V_kv, d_mm, h_m, W_g, elec_type='smooth'):
    b_m = b_mm / 1000
    c_m = c_mm / 1000
    L_m = L_mm / 1000
    S = b_m * c_m
    AR = (b_m**2) / S if S > 0 else 0
    rho = calc_rho(h_m)
    W_N = (W_g / 1000) * 9.81
    sawtooth = elec_type == 'sawtooth'
    T_s = calc_thrust(V_kv, d_mm, L_m, False)
    T_st = calc_thrust(V_kv, d_mm, L_m, True)
    T = T_st if sawtooth else T_s
    T_N = T / 1000
    V_c = calc_cruise_velocity(T_N, W_N, rho, S, AR)
    D_p, D_i, D_t = calc_drag(W_N, rho, V_c, S, AR)
    TW = T_N / W_N if W_N > 0 else 0
    LD = W_N / D_t if D_t > 0 else 0
    viable = (TW >= 1.0) and (LD >= 8.0) and (0.5 <= V_c <= 5.0)
    return {
        'b': b_mm, 'c': c_mm, 'L': L_mm, 'V': V_kv, 'd': d_mm,
        'W': W_g, 'elec': elec_type,
        'T': round(T, 4), 'T_st': round(T_st, 4),
        'T_N': T_N, 'W_N': W_N,
        'V_c': V_c, 'D_t_mN': D_t*1000,
        'TW': TW, 'glide': LD,
        'AR': AR, 'S': S, 'rho': rho,
        'viable': viable
    }

print("="*70)
print("ION WIND AIRCRAFT - FOCUSED INVESTIGATION")
print("="*70)

# The V_c is always 0.10 m/s issue - debug
print("\n1. Debug: Why is V_c always 0.10 m/s?")
# Let's trace through for MIT case
b, c, L, V, d, h, W = 5000, 500, 5000, 75, 25, 0, 2500
b_m, c_m, L_m = b/1000, c/1000, L/1000
S = b_m * c_m
AR = (b_m**2) / S
rho = calc_rho(h)
W_N = (W/1000) * 9.81
T_s = calc_thrust(V, d, L_m, False)
T_N = T_s / 1000
print(f"MIT: S={S:.2f}m2 AR={AR:.1f} rho={rho:.4f}")
print(f"W_N={W_N:.3f}N T_N={T_N:.6f}N T/W={T_N/W_N:.6f}")
print(f"T_N/thrust={T_N:.6f} vs W_N={W_N:.3f}")

# If thrust << weight, V_c will be very low
# The equilibrium: D_t(V) = T_N
# D_t = 0.5*rho*V2*(Cd*S + W2/(0.5*rho*V2*pi*AR*e))
# When V is small: induced drag dominates
# D_t ≈ W2/(0.5*rho*V2*pi*AR*e)
# Setting D_t = T_N: V = sqrt(W2 * 2 / (T_N * rho * pi * AR * e))
V_test = math.sqrt(W_N**2 * 2 / (T_N * rho * math.pi * AR * E_OSW))
print(f"Estimated V_c from simplified equation: {V_test:.4f} m/s")

# But the actual iterative solver gave 0.10 m/s
# Let's check what D_t is at V=0.10
D_p, D_i, D_t = calc_drag(W_N, rho, 0.10, S, AR)
print(f"At V=0.10: D_p={D_p*1000:.4f}mN D_i={D_i*1000:.2f}mN D_t={D_t*1000:.2f}mN T_N={T_N*1000:.4f}mN")
print(f"T_N vs D_t at V=0.10: {T_N*1000:.4f}mN vs {D_t*1000:.4f}mN")

# With T_N=0.01125N, W_N=24.525N:
# D_i = W_N^2/(0.5*rho*V^2*pi*AR*e) = 600/(0.5*1.225*0.01*pi*10*0.8)
# = 600/(0.153) = 3917 N... wait that can't be right
D_i_test = (W_N**2) / (0.5 * rho * 0.10**2 * math.pi * AR * E_OSW)
print(f"D_i at V=0.10: {D_i_test:.2f}N")
print(f"D_t at V=0.10: {D_p + D_i_test:.2f}N")
print(f"T_N: {T_N:.6f}N")
# So at V=0.10, D_t is ~3917N but T_N is only 0.011N
# The solver must be finding a very low V

# The cruise velocity converges to 0.10 m/s (the floor I set) because
# with such tiny thrust, the equilibrium speed where D_t = T_N would be
# extremely low (mm/s range), but I floor it at 0.10 m/s

print("\n2. Glide ratio always terrible - why?")
# Glide ratio = L/D = W_N / D_t
# At V=0.10: D_i is huge because induced drag ~ 1/V2
# L/D = W_N / (D_p + D_i) ≈ W_N/D_i when D_i >> D_p
# D_i ~ 1/V^2 so as V->0, D_i -> infinity, L/D -> 0
# That's why glide is always terrible at V_c = 0.10 m/s

print("\n3. What gap/d conditions would give T/W >= 1?")
# T/W >= 1 means T_N >= W_N
# T_N = K * V^2 / d^2 * L / 1000
# W_N = W_g/1000 * 9.81
# So: K * V^2 * L / d^2 >= W_g * 9.81
# d^2 <= K * V^2 * L / (W_g * 9.81)

for V in [40, 60, 80]:
    for W_g in [50, 100, 200, 500]:
        for L_mm in [200, 400, 500]:
            d2_max = K * (V**2) * (L_mm/1000) / (W_g/1000 * 9.81)
            d_max = math.sqrt(d2_max) * 1000  # in mm
            if d_max > 0 and d_max < 60:
                print(f"V={V}kV W={W_g}g L={L_mm}mm: d_max={d_max:.1f}mm")

print("\n4. Can we get T/W >= 1 at any gap within 3-50mm?")
# Max T at given V: use smallest d=3mm
# T_saw = 0.25 * V^2 / 9 * L * 1.28
# W_N = W_g/1000 * 9.81
# T/W = (0.25 * V^2 / 9 * L * 1.28/1000) / (W_g/1000 * 9.81)
#     = 0.25 * V^2 * L * 1.28 / (9 * 9.81 * W_g)

for V in [40, 60, 80]:
    for W_g in [50, 100, 200, 300, 500]:
        for L_mm in [200, 400, 500]:
            TW_max = 0.25 * V**2 * (L_mm/1000) * 1.28 / (9 * 9.81 * W_g)
            if TW_max >= 0.01:
                print(f"V={V}kV W={W_g}g L={L_mm}mm: max T/W={TW_max:.4f}")

print("\n5. Maximum T/W possible (d=3mm, L=500mm, sawtooth, V=80kV)")
T_max = calc_thrust(80, 3, 0.5, True)
for W_g in [50, 100, 200, 300, 500]:
    TW = (T_max/1000) / (W_g/1000 * 9.81)
    print(f"  W={W_g}g: T={T_max:.1f}mN, T/W={TW:.5f}")

print("\n6. If we relax glide constraint: what does it take to get T/W >= 1?")
# From eq: d^2 <= K * V^2 * L / (W_g * 9.81)
# For W=100g, V=80kV, L=0.5m: d^2 <= 0.25 * 6400 * 0.5 / (0.1 * 9.81) = 816
# d <= 28.6mm (for T/W=1)
# At d=20mm (within 20-50 range): T/W = (28.6/20)^2 = 2.04
# Hmm, d=28.6mm is within range! And at 80kV, min arc-free gap = 27mm
# So 80kV/28mm might work!
print("\nCalculating exact T/W at d=27mm (just below arcing threshold for 80kV):")
V, d, L, W_g = 80, 27, 500, 100
T = calc_thrust(V, d, L/1000, True)
TW = (T/1000) / (W_g/1000 * 9.81)
print(f"V={V}kV d={d}mm L={L}mm W={W_g}g: T={T:.2f}mN, T/W={TW:.4f}")
print(f"For T/W=1 at V=80kV, L=500mm, W=100g: d_max={math.sqrt(0.25*6400*0.5/(0.1*9.81))*1000:.1f}mm")

print("\n7. But arcing constraint: d >= V/3 mm (E=3MV/m)")
print(f"At 80kV: d_min_arc = {80/3:.1f}mm")
print(f"For T/W=1 with 80kV, 500mm, 100g: d_needed = {math.sqrt(0.25*6400*0.5/(0.1*9.81))*1000:.1f}mm")
d_needed = math.sqrt(0.25*6400*0.5/(0.1*9.81))*1000
d_arc_min = 80/3
print(f"d_needed ({d_needed:.1f}mm) vs d_arc_min ({d_arc_min:.1f}mm): ratio = {d_needed/d_arc_min:.2f}")
print(f"=> With K=0.25, NO ARcing-free T/W=1 is achievable at 80kV/500mm/100g")

print("\n8. Check at what V the arcing-free T/W=1 becomes possible")
# Condition: d_needed <= V/3
# sqrt(K*V^2*L/(W*9.81)) <= V/3
# sqrt(K*L/(W*9.81)) <= V/(3*V) * sqrt(V^2)
# hmm, let me solve: d_needed = sqrt(K*V^2*L/(W*9.81)) = V*sqrt(K*L/(W*9.81))
# We need d_needed <= V/3 => V*sqrt(K*L/(W*9.81)) <= V/3 => sqrt(K*L/(W*9.81)) <= 1/3
# => K*L/(W*9.81) <= 1/9 => K*L <= W*9.81/9
# For W=100g: K*L <= 0.108 => with K=0.25: L <= 0.432m
# So with L<=432mm, arcing-free T/W=1 MIGHT be achievable
# Let's check more carefully
print("Checking V=80kV, W=100g for various L:")
for L_mm in [100, 200, 300, 400, 450, 500]:
    d_needed = math.sqrt(K * 80**2 * (L_mm/1000) / (0.1*9.81)) * 1000
    d_arc = 80/3
    TW_arc_free = (calc_thrust(80, d_arc, L_mm/1000, True)/1000) / (0.1*9.81)
    print(f"  L={L_mm}mm: d_needed={d_needed:.1f}mm (arc-free at {d_arc:.1f}mm) => T/W at arc-free={TW_arc_free:.4f}")

print("\n9. With chord variation (affects AR and S, thus glide ratio)")
# Try b=500mm, c=50mm (high AR wing), V=80kV, d=26.7mm, L=500mm, W=100g
r = evaluate(500, 50, 500, 80, 27, 0, 100, 'smooth')
print(f"b=500 c=50 L=500 V=80 d=27 W=100: T={r['T']:.2f}mN TW={r['TW']:.4f} glide={r['glide']:.3f} V_c={r['V_c']:.2f}")
r2 = evaluate(500, 50, 500, 80, 27, 0, 100, 'sawtooth')
print(f"b=500 c=50 L=500 V=80 d=27 W=100 sawtooth: T={r2['T']:.2f}mN TW={r2['TW']:.4f} glide={r2['glide']:.3f} V_c={r2['V_c']:.2f}")

print("\n10. Grid search: BEST achievable T/W at each weight with d=27mm (arc-free at 80kV)")
print("Checking various L and V combos at arc-free d=V/3mm:")
results_by_weight = {}
for V in [40, 50, 60, 70, 80]:
    d = V / 3.0  # arc-free gap
    for L_mm in [100, 200, 300, 400, 500]:
        for W_g in [50, 100, 200, 300, 500]:
            r = evaluate(500, 50, L_mm, V, d, 0, W_g, 'sawtooth')
            if W_g not in results_by_weight or r['TW'] > results_by_weight[W_g]['TW']:
                results_by_weight[W_g] = {**r, 'V': V, 'd': d}

for W_g, r in sorted(results_by_weight.items()):
    print(f"W={W_g}g: b=500 c=50 L={r['L']}mm V={r['V']}kV d={r['d']:.1f}mm")
    print(f"  T={r['T']:.2f}mN TW={r['TW']:.4f} glide={r['glide']:.3f} V_c={r['V_c']:.2f}m/s viable={r['viable']}")

print("\n11. Check all arcing-free configs (d >= V/3) for viability")
print("Relaxing gap to allow smaller d where T/W might reach 1")
print("Testing d=V/3, V/2.5, V/2, and 20mm (minimum practical):")
viable_found = []
for V in [20, 30, 40, 50, 60, 70, 80]:
    for d_mult in [1/3, 0.4, 0.5, 1/2, 1]:
        d = max(20, V * d_mult)
        for b in [200, 300, 400, 500]:
            for c in [50, 80, 120]:
                for L_mm in [200, 400, 500]:
                    for W_g in [50, 100, 200]:
                        for et in ['smooth', 'sawtooth']:
                            r = evaluate(b, c, L_mm, V, d, 0, W_g, et)
                            if r['viable']:
                                viable_found.append(r)

print(f"\nViable configs found: {len(viable_found)}")
if viable_found:
    viable_found.sort(key=lambda x: x['TW'], reverse=True)
    for r in viable_found[:10]:
        print(f"  b={r['b']} c={r['c']} L={r['L']} V={r['V']}kV d={r['d']:.1f}mm W={r['W']}g {r['elec']}")
        print(f"    T={r['T']:.2f}mN TW={r['TW']:.4f} glide={r['glide']:.3f} V_c={r['V_c']:.2f}")
else:
    print("NO VIABLE CONFIGURATIONS - even with d=V/3")
    print("\nBest TW at 80kV, d=26.7mm (arc-free), various weights:")
    for W_g in [50, 100, 200, 300]:
        for L_mm in [500]:
            for et in ['sawtooth']:
                r = evaluate(500, 50, L_mm, 80, 26.7, 0, W_g, et)
                print(f"  W={W_g}g L=500mm: T={r['T']:.2f}mN TW={r['TW']:.4f} glide={r['glide']:.3f} V_c={r['V_c']:.2f}")

print(f"\nFinished: {datetime.now()}")
