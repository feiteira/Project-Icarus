#!/usr/bin/env python3
"""
Ion Wind Thrust Calculator — Practical DIY ZVS Flyback Voltages (≤50kV)
Carlos's ion wind plane project
"""

import math
import json

# Physical constants
eps0 = 8.854e-12  # F/m (vacuum permittivity)
q = 1.602e-19     # C (elementary charge)

# Electrode types and their K correction factors
# K=0.071: smooth MIT calibrated emitters
# K=0.623: NACA airfoil collectors
K_SMOOTH = 0.071
K_NACA = 0.623

# Voltage levels to evaluate (V)
voltages = [20_000, 25_000, 30_000, 35_000, 40_000, 45_000, 50_000]

# Electrode lengths (mm)
lengths = [200, 300, 400, 500]

# Gap distances (mm) — must be ≥8mm for practical arcing avoidance
gaps = [8, 10, 12, 15, 20, 25, 30]

# Practical constraints
MAX_PRACTICAL_KV = 50_000
NEED_THRUST_MN = 163.5  # 3x baseline 54.5 mN
ZVS_POWER_W = 15  # Typical small ZVS flyback module
ZVS_MAX_KV = 50  # Practical max for small ZVS

# Flyback ion current estimates (A) at different voltages
# Based on approximate ion production rates for small gaps
# Higher voltage = more ionization = higher current
def estimate_ion_current(V, d_mm, L_mm):
    """Estimate ion current (A) for a given config."""
    # Electric field
    E = V / (d_mm * 1e-3)

    # Approximate ionization rate — proportional to E^1.5 and volume
    # Heuristic based on typical DIY ion wind currents (0.1-5 mA range)
    d = d_mm * 1e-3
    L = L_mm * 1e-3

    # At high E fields (>2e6 V/m), ionization becomes significant
    # Ion current scales roughly with E^1.5 and active volume
    if E < 1.5e6:
        I = 0.05e-3  # 0.05 mA floor for weak ionization
    elif E < 2.5e6:
        I = 0.2e-3   # 0.2 mA
    elif E < 3.5e6:
        I = 0.5e-3   # 0.5 mA
    elif E < 4.5e6:
        I = 1.0e-3   # 1.0 mA
    else:
        I = 2.0e-3   # 2.0 mA cap for small ZVS

    # Scale with electrode area (longer electrodes = more ion production)
    scaling = (L * 0.1)  # roughly proportional to length
    I = I * scaling

    # Cap at realistic ZVS current levels
    I = min(I, 3.0e-3)  # 3 mA max for small flyback

    return I

def calc_thrust(K, V, d_mm, L_mm):
    """Calculate thrust in mN."""
    d = d_mm * 1e-3  # gap in meters
    L = L_mm * 1e-3  # length in meters
    E = V / d        # electric field V/m
    A = L * d        # gap area

    T_N = K * eps0 * E**2 * A
    return T_N * 1000  # convert to mN

def calc_input_power(V, I, thrust_mN, K, d_mm, L_mm):
    """
    Estimate input power (W) for the configuration.
    Uses: beam_power = V×I, then apply propulsion efficiency.
    Efficiency depends on how well the ion beam is captured.
    """
    if thrust_mN < 0.01:
        return float('inf')

    d = d_mm * 1e-3
    L = L_mm * 1e-3
    E = V / d

    # Exhaust velocity (effective)
    # Not all V contributes to ion acceleration (space charge, recombination)
    # Use voltage utilization factor that increases with E
    if E < 2e6:
        eta_V = 0.3
    elif E < 3e6:
        eta_V = 0.5
    elif E < 4e6:
        eta_V = 0.65
    else:
        eta_V = 0.8

    v_ex = eta_V * E * d  # effective exhaust velocity m/s

    # Beam power
    P_beam = V * I

    # Mechanical power output
    T_N = thrust_mN * 1e-3
    P_mech = T_N * v_ex

    if P_beam < 0.001:
        return float('inf')

    # Propulsion efficiency (ratio of mechanical power to beam power)
    eta_prop = P_mech / P_beam if P_beam > 0 else 0

    # Beam efficiency (what fraction of beam power becomes useful thrust)
    # Lower K (smooth) = worse beam capture
    beam_eff = min(eta_prop * 3, 0.85)  # cap at 85%

    # Total input power
    P_input = P_beam / beam_eff if beam_eff > 0.001 else float('inf')

    return P_input

def make_config(v, d, L, K, K_name, I):
    T = calc_thrust(K, v, d, L)
    P = calc_input_power(v, I, T, K, d, L)

    if T < 0.001:
        return None

    # Thrust per watt (mN/W)
    tpw = T / P if P < float('inf') else 0

    return {
        'voltage_kv': v / 1000,
        'gap_mm': d,
        'length_mm': L,
        'K': K,
        'electrode_type': K_name,
        'thrust_mN': T,
        'ion_current_mA': I * 1000,
        'input_power_W': P if P < float('inf') else None,
        'thrust_per_watt': tpw,
        'efficiency': None,  # filled below
        'practical': P <= ZVS_POWER_W * 3 if P < float('inf') else False,  # 3x headroom
        'practical_strict': P <= ZVS_POWER_W if P < float('inf') else False,
    }

# Compute all configurations
all_configs = []

for v in voltages:
    for d in gaps:
        for L in lengths:
            for K, K_name in [(K_SMOOTH, 'smooth'), (K_NACA, 'naca_airfoil')]:
                I = estimate_ion_current(v, d, L)
                cfg = make_config(v, d, L, K, K_name, I)
                if cfg:
                    all_configs.append(cfg)

# Sort by thrust
all_configs.sort(key=lambda x: -x['thrust_mN'])

print(f"Total configurations evaluated: {len(all_configs)}")
print(f"Baseline thrust: 54.5 mN")
print(f"Need 3x baseline: {NEED_THRUST_MN} mN")
print(f"Max practical voltage: {MAX_PRACTICAL_KV/1000} kV")
print(f"ZVS module power budget: {ZVS_POWER_W} W")
print()

# Top 20 by thrust
print("=" * 100)
print("TOP 20 CONFIGURATIONS BY THRUST (all ≤50kV)")
print("=" * 100)
for i, c in enumerate(all_configs[:20]):
    p_str = f"{c['input_power_W']:.1f} W" if c['input_power_W'] else "N/A"
    practical = "✓ ZVS OK" if c['practical_strict'] else ("~ borderline" if c['practical'] else "✗ high power")
    print(f"{i+1:2d}. {c['voltage_kv']:5.1f}kV | {c['gap_mm']:2d}mm gap | {c['length_mm']:3d}mm len | "
          f"{c['electrode_type']:15s} | K={c['K']:.3f} | "
          f"T={c['thrust_mN']:8.2f} mN | P={p_str:>10s} | {practical}")

print()
print("=" * 100)
print("TOP 10 BY THRUST/POWER RATIO (thrust efficiency)")
print("=" * 100)
by_tpw = sorted([c for c in all_configs if c['thrust_per_watt'] > 0], key=lambda x: -x['thrust_per_watt'])
for i, c in enumerate(by_tpw[:10]):
    p_str = f"{c['input_power_W']:.1f} W" if c['input_power_W'] else "N/A"
    print(f"{i+1:2d}. {c['voltage_kv']:5.1f}kV | {c['gap_mm']:2d}mm gap | {c['length_mm']:3d}mm len | "
          f"{c['electrode_type']:15s} | T={c['thrust_mN']:8.2f} mN | "
          f"TPW={c['thrust_per_watt']:6.2f} mN/W | P={p_str}")

print()
print("=" * 100)
print("THRUST VS WEIGHT ANALYSIS (T/W ratios)")
print("=" * 100)

weights = [50, 100, 200]  # grams
for c in all_configs[:5]:
    print(f"\nConfig: {c['voltage_kv']}kV / {c['gap_mm']}mm / {c['length_mm']}mm / {c['electrode_type']}")
    print(f"  Thrust: {c['thrust_mN']:.2f} mN")
    for w_g in weights:
        w_N = w_g * 1e-3 * 9.81
        tw = c['thrust_mN'] * 1e-3 * 9.81 / w_N
        print(f"  T/W for {w_g}g: {tw:.4f} (need >0.05 to hover, ideally >0.10)")

# Summary stats
configs_above_target = [c for c in all_configs if c['thrust_mN'] >= NEED_THRUST_MN]
configs_zvs_ok = [c for c in all_configs if c['practical_strict']]
configs_zvs_borderline = [c for c in all_configs if c['practical'] and not c['practical_strict']]

print()
print("=" * 100)
print("SUMMARY")
print("=" * 100)
print(f"Total configs: {len(all_configs)}")
print(f"Configs meeting 3x thrust target ({NEED_THRUST_MN} mN): {len(configs_above_target)}")
print(f"Configs practical with ZVS module: {len(configs_zvs_ok)}")
print(f"Configs borderline for ZVS: {len(configs_zvs_borderline)}")

if configs_above_target:
    best = configs_above_target[0]
    print(f"\n*** BEST OVERALL: {best['voltage_kv']}kV / {best['gap_mm']}mm gap / {best['length_mm']}mm / {best['electrode_type']} ***")
    print(f"    Thrust: {best['thrust_mN']:.2f} mN")
    if best['input_power_W']:
        print(f"    Input Power: {best['input_power_W']:.1f} W")
    else:
        print(f"    Input Power: N/A")

# Best practical
if configs_zvs_ok:
    best_practical = max(configs_zvs_ok, key=lambda x: x['thrust_mN'])
    print(f"\n*** BEST PRACTICAL ZVS: {best_practical['voltage_kv']}kV / {best_practical['gap_mm']}mm gap / {best_practical['length_mm']}mm / {best_practical['electrode_type']} ***")
    print(f"    Thrust: {best_practical['thrust_mN']:.2f} mN")
    if best_practical['input_power_W']:
        print(f"    Input Power: {best_practical['input_power_W']:.1f} W")

# Voltage breakdown table
print()
print("=" * 100)
print("BEST CONFIG PER VOLTAGE LEVEL")
print("=" * 100)
for v in voltages:
    v_configs = [c for c in all_configs if c['voltage_kv'] == v/1000]
    if v_configs:
        best_v = max(v_configs, key=lambda x: x['thrust_mN'])
        p_str = f"{best_v['input_power_W']:.1f} W" if best_v['input_power_W'] else "N/A"
        mark = " ◀ BEST" if best_v == all_configs[0] else ""
        print(f"{v/1000:5.1f}kV: {best_v['gap_mm']:2d}mm gap | {best_v['length_mm']:3d}mm | {best_v['electrode_type']:15s} | "
              f"T={best_v['thrust_mN']:8.2f} mN | P={p_str:>10s}{mark}")

# Store results for markdown report
results = {
    'all_configs': all_configs,
    'configs_above_target': configs_above_target,
    'configs_zvs_ok': configs_zvs_ok,
}

with open('/home/feiteira/.openclaw/workspace/ion-wind-plane/practical_thrust_data.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\nData saved to practical_thrust_data.json")
