from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Water level (cm) in a tank, read every 10 minutes
time = np.array([0, 10, 20, 30, 40, 50, 60], dtype=float)   # minutes
level = np.array([20.0, 23.1, 27.0, 31.8, 37.5, 44.1, 51.6])  # cm
AREA_CM2 = 20_000          # tank floor area: 2 m^2
HEIGHT_CM = 100.0          # tank height
ALARM = 0.6                # cm/min

rate = np.zeros_like(level)
rate[0] = (level[1] - level[0]) / (time[1] - time[0])
for i in range(1, len(time) - 1):
    rate[i] = (level[i + 1] - level[i - 1]) / (time[i + 1] - time[i - 1])
rate[-1] = (level[-1] - level[-2]) / (time[-1] - time[-2])

flow = rate * AREA_CM2 / 1000.0                  # litres per minute

print("Time (min)  Level (cm)  Rise (cm/min)  Inflow (L/min)")
for t, h, r, q in zip(time, level, rate, flow):
    print(f"{t:>10.0f}{h:>12.1f}{r:>15.3f}{q:>16.2f}")

print("\nMatches np.gradient:", np.allclose(rate, np.gradient(level, time)))
alarm_times = time[rate > ALARM]
print(f"Rise exceeds {ALARM} cm/min from t = {alarm_times[0]:.0f} min")
remaining = HEIGHT_CM - level[-1]
print(f"Time to overflow at the latest rate: {remaining / rate[-1]:.1f} min "
      f"(upper estimate, the rate is still increasing)")

out = Path(__file__).resolve().parent.parent / "docs"
out.mkdir(exist_ok=True)
fig, ax = plt.subplots(1, 2, figsize=(11, 4.5))
ax[0].plot(time, level, "o-")
ax[0].set_xlabel("Time (min)")
ax[0].set_ylabel("Water level (cm)")
ax[0].set_title("Measured level")
ax[0].grid(True)
ax[1].plot(time, rate, "o-", label="Estimated rise rate")
ax[1].axhline(ALARM, color="red", linestyle=":", label="Alarm level")
ax[1].set_xlabel("Time (min)")
ax[1].set_ylabel("Rise rate (cm/min)")
ax[1].set_title("Rate of change from differences")
ax[1].legend()
ax[1].grid(True)
plt.tight_layout()
plt.savefig(out / "Task_15_variation_plot.png", dpi=150)
plt.show()