from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d, CubicSpline

# Soil-moisture sensor calibration table: raw sensor reading (ADC) -> moisture %
adc = np.array([250, 350, 450, 550, 650, 750], dtype=float)
moisture = np.array([80.0, 62.0, 45.0, 31.0, 20.0, 12.0])

linear = interp1d(adc, moisture)
cubic = CubicSpline(adc, moisture)

print("Reading   Linear (%)   Cubic (%)")
for reading in [300, 400, 500, 600, 700]:
    print(f"{reading:>7}{float(linear(reading)):>12.2f}{float(cubic(reading)):>12.2f}")

# Hold-out check: remove the 450 point, then estimate it and compare with the true 45%
keep = [0, 1, 3, 4, 5]
lin_h = interp1d(adc[keep], moisture[keep])
cub_h = CubicSpline(adc[keep], moisture[keep])
print(f"\nHold-out test at reading 450 (true value 45.0 %):")
print(f"  Linear: {float(lin_h(450)):.2f} %  (error {abs(float(lin_h(450)) - 45):.2f})")
print(f"  Cubic : {float(cub_h(450)):.2f} %  (error {abs(float(cub_h(450)) - 45):.2f})")

irrigate_below = 35.0
fine = np.linspace(250, 750, 500)
dry_start = fine[cubic(fine) < irrigate_below][0]
print(f"\nMoisture falls below {irrigate_below}% at a reading of about {dry_start:.0f}")

out = Path(__file__).resolve().parent.parent / "docs"
out.mkdir(exist_ok=True)
plt.figure(figsize=(7.5, 4.8))
plt.scatter(adc, moisture, color="black", zorder=3, label="Calibration points")
plt.plot(fine, linear(fine), "--", label="Linear")
plt.plot(fine, cubic(fine), label="Cubic spline")
plt.axhline(irrigate_below, color="red", linestyle=":", label="Irrigation threshold")
plt.xlabel("Sensor reading (ADC)")
plt.ylabel("Soil moisture (%)")
plt.title("Soil-moisture sensor calibration")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(out / "Task_13_variation_plot.png", dpi=150)
plt.show()