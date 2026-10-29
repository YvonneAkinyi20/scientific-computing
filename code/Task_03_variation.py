import timeit
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Simulated solar-panel readings, one per second (1,000,000 readings)
rng = np.random.default_rng(1)
voltage_v = rng.uniform(12, 22, 1_000_000)      # volts
current_ma = rng.uniform(100, 5000, 1_000_000)  # milliamps


def loop_version():
    power = []
    for v, i in zip(voltage_v, current_ma):
        power.append(v * (i / 1000.0))          # P = V x I, in watts
    return power


def vectorized_version():
    return voltage_v * (current_ma / 1000.0)


loop_time = timeit.timeit(loop_version, number=1)
vector_time = timeit.timeit(vectorized_version, number=3) / 3

power_w = vectorized_version()
energy_kwh = power_w.sum() / 3_600_000          # watt-seconds -> kWh

# Identity check from the concept: sin^2(x) + cos^2(x) = 1 for every x
x = rng.uniform(0, 2 * np.pi, 1_000_000)
identity_ok = np.allclose(np.sin(x) ** 2 + np.cos(x) ** 2, 1.0)

print(f"Mean power: {power_w.mean():.2f} W, maximum: {power_w.max():.2f} W")
print(f"Energy produced: {energy_kwh:.2f} kWh")
print(f"Loop time: {loop_time:.4f} s")
print(f"Vectorized time: {vector_time:.4f} s")
print(f"Approximate speed-up: {loop_time / vector_time:.1f}x")
print("sin^2 + cos^2 = 1 for all 1,000,000 values:", identity_ok)

out = Path(__file__).resolve().parent.parent / "docs"
out.mkdir(exist_ok=True)
plt.figure(figsize=(6, 4.5))
plt.bar(["Python loop", "Vectorized"], [loop_time, vector_time],
        color=["tomato", "seagreen"])
plt.yscale("log")
plt.ylabel("Time (s, log scale)")
plt.title("Power calculation: loop vs vectorized")
plt.tight_layout()
plt.savefig(out / "Task_03_variation_plot.png", dpi=150)
plt.show()