#!/usr/bin/env python3
"""
Ion Wind Aircraft Simulator - Physics Calculations
Implements the same formulas as simulator.html
"""
import math
import json
from datetime import datetime

# Physics constants (from HTML)
K = 0.25         # Empirical thrust constant
RHO_SEA = 1.225  # sea-level air density kg/m3
H_SCALE = 8500   # scale height for density decay (m)
CD_P = 0.02      # parasitic drag coefficient
E_OSW = 0.8      # Oswald efficiency factor
EPS0 = 8.854e-12 # vacuum permittivity F/m
RHO_AIR = 1.225  # air density kg/m3

def calc_rho(h_m):
    return RHO_SEA * math.exp(-h_m / H_SCALE)

def calc_thrust_empirical(V_kv, d_mm, L_m, sawtooth=False):
    if V_kv <= 0 or d_mm <= 0 or L_m <= 0:
        return 0.0
    raw = K * (V_kv ** 2) / (d_mm ** 2) * L_m
    return raw * 1.28 if sawtooth else raw

def calc_thrust_vaddi(V_kv, d_mm, L_m, mu=1.4e-4, r_e_mm=0.125):
    """Vaddi EHD first-principles thrust in mN"""
    if V_kv <= 0 or d_mm <= 0 or L_m <= 0 or mu <= 0:
        return 0.0
    E = (V_kv * 1000) / d_mm  # electric field V/m
    A = math.pi * d_mm * L_m   # cylindrical area m2
    F_N = (EPS0 * RHO_AIR * mu * E * E * A * L_m) / d_mm
    return max(F_N * 1000, 0)  # convert to mN

def calc_drag(weightN, rho, V_ms, S_m2, AR):
    D_p = 0.5 * rho * V_ms**2 * CD_P * S_m2
    D_i = (weightN**2) / (0.5 * rho * V_ms**2 * math.pi * AR * E_OSW)
    return D_p, D_i, D_p + D_i

def calc_cruise_velocity(thrustN, weightN, rho, S_m2, AR):
    """Iterate to find V where thrust equals total drag"""
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

def calc_feasibility(TW, glide):
    """Return (color, label)"""
    if TW < 0.3 or glide < 2:
        return 'red', 'NO FLIGHT'
    if TW < 0.8 or glide < 6:
        return 'yellow', 'MARGINAL'
    return 'green', 'FLIGHT POSSIBLE'

def evaluate(b_mm, c_mm, L_mm, V_kv, d_mm, h_m, W_g,
             elec_type='smooth', mu=1.4e-4, r_e_mm=0.125,
             verbose=False):
    """Full evaluation of a configuration"""
    b_m = b_mm / 1000
    c_m = c_mm / 1000
    L_m = L_mm / 1000
    d_m = d_mm / 1000
    S = b_m * c_m
    AR = (b_m**2) / S if S > 0 else 0
    rho = calc_rho(h_m)
    W_N = (W_g / 1000) * 9.81

    sawtooth = elec_type == 'sawtooth'

    T_s = calc_thrust_empirical(V_kv, d_mm, L_m, sawtooth=False)
    T_st = calc_thrust_empirical(V_kv, d_mm, L_m, sawtooth=True)
    T_v = calc_thrust_vaddi(V_kv, d_mm, L_m, mu, r_e_mm)
    T = T_st if sawtooth else T_s
    T_N = T / 1000

    V_c = calc_cruise_velocity(T_N, W_N, rho, S, AR)
    D_p, D_i, D_t = calc_drag(W_N, rho, V_c, S, AR)

    TW = T_N / W_N if W_N > 0 else 0
    LD = W_N / D_t if D_t > 0 else 0
    feas, feas_label = calc_feasibility(TW, LD)

    # Check flight viability criteria (all must be met)
    viable = (TW >= 1.0) and (LD >= 8.0) and (0.5 <= V_c <= 5.0) and (feas == 'green')

    result = {
        'b_mm': b_mm, 'c_mm': c_mm, 'L_mm': L_mm, 'V_kv': V_kv,
        'd_mm': d_mm, 'h_m': h_m, 'W_g': W_g, 'elec_type': elec_type,
        'S_m2': S, 'AR': AR, 'rho': rho,
        'T_s_mN': T_s, 'T_st_mN': T_st, 'T_v_mN': T_v, 'T_mN': T,
        'T_N': T_N, 'W_N': W_N,
        'V_c_ms': V_c, 'D_p_mN': D_p*1000, 'D_i_mN': D_i*1000, 'D_t_mN': D_t*1000,
        'TW': TW, 'glide': LD, 'feas': feas, 'feas_label': feas_label,
        'viable': viable
    }

    if verbose:
        print(f"  Wingspan: {b_mm}mm | Chord: {c_mm}mm | Electrode: {L_mm}mm")
        print(f"  Voltage: {V_kv}kV | Gap: {d_mm}mm | Alt: {h_m}m | Weight: {W_g}g")
        print(f"  T_s={T_s:.1f}mN | T_st={T_st:.1f}mN | T_v={T_v:.1f}mN")
        print(f"  V_c={V_c:.2f}m/s | T/W={TW:.3f} | Glide={LD:.2f} | {feas_label}")
        print(f"  Viable: {viable}")

    return result

def rdict(r):
    """Convert result to readable dict"""
    return {
        'b': r['b_mm'], 'c': r['c_mm'], 'L': r['L_mm'],
        'V': r['V_kv'], 'd': r['d_mm'], 'W': r['W_g'],
        'elec': r['elec_type'],
        'TW': round(r['TW'], 4), 'Glide': round(r['glide'], 2),
        'V_c': round(r['V_c_ms'], 2), 'feas': r['feas'],
        'viable': r['viable'], 'T_emp': round(r['T_mN'], 1),
        'T_vaddi': round(r['T_v_mN'], 1)
    }

def main():
    print("ION WIND AIRCRAFT SIMULATOR - PARAMETER SWEEPS")
    print(f"Started: {datetime.now()}")

    all_results = {}
    all_viable = []

    # SWEEP 1: Wingspan at 40kV/25mm gap/200g
    print("\n" + "="*60)
    print("SWEEP 1: WINGSPAN (40kV, 25mm gap, 200g, chord=80mm, L=200mm)")
    print("="*60)
    s1 = []
    for b in [150, 250, 350, 450, 500]:
        r = evaluate(b, 80, 200, 40, 25, 0, 200, verbose=True)
        s1.append(r)
        if r['viable']: all_viable.append(r)
    all_results['sweep1'] = [rdict(x) for x in s1]
    best_s1 = max(s1, key=lambda x: x['TW'])
    best_b = int(best_s1['b_mm'])
    print(f"  Highest TW: {best_b}mm, TW={best_s1['TW']:.4f}, Glide={best_s1['glide']:.2f}, Viable={best_s1['viable']}")

    # SWEEP 2: Voltage with best wingspan
    print("\n" + "="*60)
    print(f"SWEEP 2: VOLTAGE (best wingspan={best_b}mm, 25mm gap, 200g)")
    print("="*60)
    s2 = []
    for V in [20, 30, 40, 50, 60, 80]:
        r = evaluate(best_b, 80, 200, V, 25, 0, 200, verbose=True)
        s2.append(r)
        if r['viable']: all_viable.append(r)
    all_results['sweep2'] = [rdict(x) for x in s2]
    best_s2 = max(s2, key=lambda x: x['TW'])
    best_V = int(best_s2['V_kv'])
    print(f"  Highest TW: {best_V}kV, TW={best_s2['TW']:.4f}, Glide={best_s2['glide']:.2f}, Viable={best_s2['viable']}")

    # SWEEP 3: Weight with best wingspan and voltage
    print("\n" + "="*60)
    print(f"SWEEP 3: WEIGHT (best wingspan={best_b}mm, best voltage={best_V}kV, 25mm gap)")
    print("="*60)
    s3 = []
    for W in [100, 150, 200, 300]:
        r = evaluate(best_b, 80, 200, best_V, 25, 0, W, verbose=True)
        s3.append(r)
        if r['viable']: all_viable.append(r)
    all_results['sweep3'] = [rdict(x) for x in s3]
    best_s3 = max(s3, key=lambda x: x['TW'])
    best_W = int(best_s3['W_g'])
    print(f"  Highest TW: {best_W}g, TW={best_s3['TW']:.4f}, Glide={best_s3['glide']:.2f}, Viable={best_s3['viable']}")

    # SWEEP 4: Electrode type
    print("\n" + "="*60)
    print(f"SWEEP 4: ELECTRODE TYPE (b={best_b}mm, V={best_V}kV, W={best_W}g)")
    print("="*60)
    s4_smooth = evaluate(best_b, 80, 200, best_V, 25, 0, best_W, elec_type='smooth', verbose=True)
    s4_saw = evaluate(best_b, 80, 200, best_V, 25, 0, best_W, elec_type='sawtooth', verbose=True)
    s4 = [s4_smooth, s4_saw]
    all_results['sweep4'] = [rdict(x) for x in s4]
    if s4_saw['viable'] and s4_saw['TW'] > s4_smooth['TW']:
        best_elec = 'sawtooth'
        best_s4 = s4_saw
    elif s4_smooth['viable']:
        best_elec = 'smooth'
        best_s4 = s4_smooth
    else:
        best_elec = 'sawtooth' if s4_saw['TW'] > s4_smooth['TW'] else 'smooth'
        best_s4 = s4_saw if s4_saw['TW'] > s4_smooth['TW'] else s4_smooth
    for r in s4:
        if r['viable']: all_viable.append(r)
    print(f"  Smooth: TW={s4_smooth['TW']:.4f}, Viable={s4_smooth['viable']}")
    print(f"  Sawtooth: TW={s4_saw['TW']:.4f}, Viable={s4_saw['viable']}")
    print(f"  Best electrode: {best_elec}")

    # STRETCH: larger wingspans
    print("\n" + "="*60)
    print(f"STRETCH: wingspans > 500mm (V={best_V}kV, W={best_W}g)")
    print("="*60)
    s_stretch = []
    for b in [550, 600, 700]:
        r = evaluate(b, 80, 200, best_V, 25, 0, best_W, verbose=True)
        s_stretch.append(r)
        if r['viable']: all_viable.append(r)
    all_results['stretch'] = [rdict(x) for x in s_stretch]

    # Chord sweep
    print("\n" + "="*60)
    print(f"SWEEP CHORD (b={best_b}mm, V={best_V}kV, W={best_W}g)")
    print("="*60)
    s_chord = []
    for c in [50, 80, 120, 160, 200]:
        r = evaluate(best_b, c, 200, best_V, 25, 0, best_W, verbose=True)
        s_chord.append(r)
        if r['viable']: all_viable.append(r)
    all_results['chord'] = [rdict(x) for x in s_chord]

    # Electrode length sweep
    print("\n" + "="*60)
    print(f"SWEEP ELECTRODE LENGTH (b={best_b}mm, c=80mm, V={best_V}kV, W={best_W}g)")
    print("="*60)
    s_L = []
    for L in [50, 100, 150, 200, 300, 400]:
        r = evaluate(best_b, 80, L, best_V, 25, 0, best_W, verbose=True)
        s_L.append(r)
        if r['viable']: all_viable.append(r)
    all_results['electrode_length'] = [rdict(x) for x in s_L]

    # Gap sweep
    print("\n" + "="*60)
    print(f"SWEEP GAP (b={best_b}mm, V={best_V}kV, W={best_W}g)")
    print("="*60)
    s_gap = []
    for d in [20, 25, 30, 40, 50]:
        r = evaluate(best_b, 80, 200, best_V, d, 0, best_W, verbose=True)
        s_gap.append(r)
        if r['viable']: all_viable.append(r)
    all_results['gap'] = [rdict(x) for x in s_gap]

    # MIT reference
    print("\n" + "="*60)
    print("MIT REFERENCE CASE: 5000mm/75kV/25mm/2500g (c=500mm, L=5000mm)")
    print("="*60)
    mit = evaluate(5000, 500, 5000, 75, 25, 0, 2500, elec_type='smooth', verbose=True)
    mit_saw = evaluate(5000, 500, 5000, 75, 25, 0, 2500, elec_type='sawtooth', verbose=True)
    all_results['mit'] = rdict(mit)
    all_results['mit_saw'] = rdict(mit_saw)

    # Altitude sweep for best config
    print("\n" + "="*60)
    print(f"SWEEP ALTITUDE (best config: b={best_b}mm, V={best_V}kV, W={best_W}g, elec={best_elec})")
    print("="*60)
    s_alt = []
    for h in [0, 200, 500, 800, 1000]:
        r = evaluate(best_b, 80, 200, best_V, 25, h, best_W, elec_type=best_elec, verbose=True)
        s_alt.append(r)
        if r['viable']: all_viable.append(r)
    all_results['altitude'] = [rdict(x) for x in s_alt]

    # Find best viable
    print(f"\n\nTotal viable configs found: {len(all_viable)}")
    all_viable.sort(key=lambda x: x['TW'], reverse=True)

    best = all_viable[0] if all_viable else best_s4
    second = all_viable[1] if len(all_viable) > 1 else None

    print("\n" + "="*60)
    print("BEST VIABLE CONFIGURATION")
    print("="*60)
    print(f"  Wingspan: {best['b_mm']}mm | Chord: {best['c_mm']}mm | Electrode: {best['L_mm']}mm")
    print(f"  Voltage: {best['V_kv']}kV | Gap: {best['d_mm']}mm | Alt: {best['h_m']}m | Weight: {best['W_g']}g")
    print(f"  Electrode type: {best['elec_type']}")
    print(f"  T/W: {best['TW']:.4f} | Glide: {best['glide']:.2f} | Cruise: {best['V_c_ms']:.2f}m/s")
    print(f"  Thrust (emp smooth): {best['T_s_mN']:.1f}mN")
    print(f"  Thrust (emp sawtooth): {best['T_st_mN']:.1f}mN")
    print(f"  Thrust (Vaddi): {best['T_v_mN']:.1f}mN")

    if second:
        print(f"\nSecond best: b={second['b_mm']}mm V={second['V_kv']}kV W={second['W_g']}g TW={second['TW']:.4f}")

    print("\n" + "="*60)
    print("MIT REFERENCE RESULT")
    print("="*60)
    print(f"  Wingspan: {mit['b_mm']}mm | Chord: {mit['c_mm']}mm | Electrode: {mit['L_mm']}mm")
    print(f"  Voltage: {mit['V_kv']}kV | Gap: {mit['d_mm']}mm | Weight: {mit['W_g']}g")
    print(f"  T/W: {mit['TW']:.4f} | Glide: {mit['glide']:.2f} | Cruise: {mit['V_c_ms']:.2f}m/s")
    print(f"  Thrust (emp smooth): {mit['T_s_mN']:.1f}mN")
    print(f"  Thrust (emp sawtooth): {mit_saw['T_mN']:.1f}mN (sawtooth)")
    print(f"  Thrust (Vaddi): {mit['T_v_mN']:.1f}mN")

    # Key insights
    print("\n" + "="*60)
    print("KEY INSIGHTS")
    print("="*60)

    # Empirical vs Vaddi divergence
    print(f"\nEmpirical vs Vaddi divergence (best DIY config):")
    print(f"  Empirical: {best['T_mN']:.1f} mN")
    print(f"  Vaddi: {best['T_v_mN']:.1f} mN")
    print(f"  Ratio (emp/vaddi): {best['T_mN']/max(best['T_v_mN'],0.001):.2f}x")

    print(f"\nEmpirical vs Vaddi divergence (MIT reference):")
    print(f"  Empirical: {mit['T_s_mN']:.1f} mN")
    print(f"  Vaddi: {mit['T_v_mN']:.1f} mN")
    print(f"  Ratio (emp/vaddi): {mit['T_s_mN']/max(mit['T_v_mN'],0.001):.2f}x")

    # Save JSON
    output = {
        'sweeps': all_results,
        'all_viable': [rdict(x) for x in all_viable[:20]],
        'best': rdict(best),
        'second_best': rdict(second) if second else None,
        'mit_reference': rdict(mit),
        'mit_reference_sawtooth': rdict(mit_saw),
    }
    with open('/home/feiteira/.openclaw/workspace/ion-wind-plane/sweep_results.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nResults saved to sweep_results.json")
    print(f"Finished: {datetime.now()}")
    return best, second, mit, all_viable, all_results

if __name__ == '__main__':
    main()
