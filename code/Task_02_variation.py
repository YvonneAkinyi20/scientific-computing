from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# 24 hourly readings (degrees Celsius) from a vaccine cold room
temps_c = np.array([
    4.2, 4.0, 3.8, 3.9, 4.1, 4.5, 5.0, 5.6,
    6.3, 7.1, 7.8, 8.4, 8.9, 8.6, 7.9, 7.2,
    6.5, 5.9, 5.3, 4.8, 4.5, 4.3, 4.2, 4.1
])
SAFE_MIN, SAFE_MAX = 2.0, 8.0      # assumed safe storage range

hours = np.arange(24)
temps_f = 1.8 * temps_c + 32       # vectorized conversion
temps_k = temps_c + 273.15         # vectorized conversion

out_of_range = (temps_c < SAFE_MIN) | (temps_c > SAFE_MAX)

print(f"Mean temperature : {temps_c.mean():.2f} C = {temps_f.mean():.2f} F = {temps_k.mean():.2f} K")
print(f"Minimum / Maximum: {temps_c.min():.1f} C at {hours[temps_c.argmin()]}:00, "
      f"{temps_c.max():.1f} C at {hours[temps_c.argmax()]}:00")
print(f"Hours outside {SAFE_MIN}-{SAFE_MAX} C: {out_of_range.sum()} "
      f"(at {hours[out_of_range].tolist()})")

out = Path(__file__).resolve().parent.parent / "docs"
out.mkdir(exist_ok=True)

plt.figure(figsize=(8, 4.5))
plt.plot(hours, temps_c, "o-", label="Temperature")
plt.axhspan(SAFE_MIN, SAFE_MAX, alpha=0.15, color="green", label="Safe range")
plt.scatter(hours[out_of_range], temps_c[out_of_range], color="red", zorder=3,
            label="Out of range")
plt.xlabel("Hour of day")
plt.ylabel("Temperature (C)")
plt.title("Cold-room temperature over 24 hours")
plt.legend()
plt.tight_layout()
plt.savefig(out / "Task_02_variation_plot.png", dpi=150)
plt.show()