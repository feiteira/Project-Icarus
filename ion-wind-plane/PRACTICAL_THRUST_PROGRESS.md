# Ion Wind Practical Thrust — Progress Report
**Status: COMPLETE** — Final report saved to PRACTICAL_THRUST.md

---

## Summary of Findings

### Best Practical Config (Overall Winner)
**40kV / 30mm gap / 500mm / NACA airfoil collector**
- Thrust: 147 mN (2.7× baseline)
- Power: ~12W (excellent efficiency)
- T/W for 100g: 1.47

### Best Config That Hits 3× Target (163.5 mN)
**35kV / 20mm gap / 500mm / NACA airfoil collector**
- Thrust: 169 mN (3.1× target!)
- Power: ~15W (fits small ZVS)
- T/W for 100g: 1.69

---

## Top 10 Practical Configs

| Rank | V | Gap | Len | T(mN) | P(W) | TPW | 3x? | ZVS OK? |
|------|---|-----|-----|-------|------|-----|-----|---------|
| 1 | 50kV | 30mm | 500mm | 230 | 31 | 7.4 | YES | marginal |
| 2 | 45kV | 25mm | 500mm | 223 | 23 | 9.5 | YES | OK |
| 3 | 40kV | 20mm | 500mm | 221 | 26 | 8.6 | YES | marginal |
| 4 | 40kV | 25mm | 500mm | 177 | 21 | 8.5 | YES | OK |
| 5 | 35kV | 20mm | 500mm | 169 | 15 | 11.6 | YES | OK |
| 6 | 35kV | 15mm | 400mm | 180 | 14 | 13.4 | YES | OK |
| 7 | 30kV | 15mm | 500mm | 165 | 14 | 11.5 | YES | OK |
| 8 | 40kV | 30mm | 500mm | 147 | 12 | 12.3 | NO | OK |
| 9 | 35kV | 25mm | 500mm | 135 | 9 | 15.4 | NO | OK |
| 10 | 30kV | 25mm | 500mm | 107 | 8 | 14.0 | NO | OK |

---

## Key Insight: Large Gaps = Better Power Efficiency

Small gaps (8mm) give high thrust but require prohibitively high power:
- 50kV / 8mm / 500mm → 862 mN but needs ~200W!

Larger gaps (20-30mm) give less thrust but need manageable power:
- 40kV / 30mm / 500mm → 147 mN at ~12W

**Trade-off:** You can't get both maximum thrust AND low power with ion wind.

---

## Voltage Level Summary

| Voltage | Best Gap | Best Thrust | Power | Verdict |
|---------|----------|-------------|-------|---------|
| 20kV | 30mm | 52 mN | 5W | Below target |
| 25kV | 25mm | 86 mN | 8W | Below target |
| 30kV | 15mm | 165 mN | 14W | ✓ Hits 3× |
| 35kV | 20mm | 169 mN | 15W | ✓ Sweet spot |
| 40kV | 20mm | 221 mN | 26W | Good (needs better ZVS) |
| 45kV | 25mm | 223 mN | 23W | Good |
| 50kV | 25mm | 276 mN | 40W | Needs powerful ZVS |

---

## Arcing Risk Notes

- **<15mm gap at ≥35kV**: Risky for DIY, especially with rough surfaces
- **20-30mm gap**: Safe from arcing even at 50kV
- **>30mm gap**: Very safe but thrust drops significantly

---

## Files Generated
- `PRACTICAL_THRUST.md` — Final comprehensive report
- `practical_thrust.py` — Python calculation script (for reference)