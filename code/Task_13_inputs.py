import numpy as np
from scipy.interpolate import interp1d, CubicSpline

hours = np.array([8, 9, 10, 11, 12, 13, 14], dtype=float)
temperature = np.array([18.0, 20.0, 22.5, 24.0, 25.0, 25.5, 25.0])

# 1. Change the interpolation method (estimate at 10:30)
print("=== Method comparison at 10:30 ===")
for kind in ["nearest", "previous", "linear", "quadratic", "cubic"]:
    f = interp1d(hours, temperature, kind=kind)
    print(f"interp1d {kind:<10}: {float(f(10.5)):.3f} C")
print(f"CubicSpline         : {float(CubicSpline(hours, temperature)(10.5)):.3f} C")

# 2. Change one measurement (a faulty spike at 11:00: 24.0 -> 30.0)
print("\n=== Faulty reading at 11:00 (24.0 changed to 30.0) ===")
bad = temperature.copy()
bad[3] = 30.0
for label, data in [("original", temperature), ("with spike", bad)]:
    lin = interp1d(hours, data)
    cub = CubicSpline(hours, data)
    print(f"{label:<11} 10:30 linear {float(lin(10.5)):.2f}  cubic {float(cub(10.5)):.2f} | "
          f"12:30 linear {float(lin(12.5)):.2f}  cubic {float(cub(12.5)):.2f}")

# 3. Use fewer points (every 2 hours) and estimate the hours we removed
print("\n=== Fewer points: keep 8, 10, 12, 14 and estimate 9, 11, 13 ===")
keep = np.array([0, 2, 4, 6])
lin2 = interp1d(hours[keep], temperature[keep])
cub2 = CubicSpline(hours[keep], temperature[keep])
print(f"{'hour':>5}{'actual':>9}{'linear':>9}{'lin err':>9}{'cubic':>9}{'cub err':>9}")
for h, actual in [(9, 20.0), (11, 24.0), (13, 25.5)]:
    l, c = float(lin2(h)), float(cub2(h))
    print(f"{h:>5}{actual:>9.2f}{l:>9.2f}{abs(l - actual):>9.2f}{c:>9.2f}{abs(c - actual):>9.2f}")

# 4. Change the evaluation time: outside the measured range (extrapolation)
print("\n=== Estimate at 15:00 (outside 8:00-14:00) ===")
print(f"CubicSpline at 15:00: {float(CubicSpline(hours, temperature)(15.0)):.2f} C")
try:
    interp1d(hours, temperature)(15.0)
except ValueError as e:
    print("interp1d at 15:00 : ValueError:", e)
    