import time

import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import lu_factor, lu_solve

# Rod and simulation settings
L = 1.0          # length (m)
k = 50.0         # thermal conductivity (W/m.K)
T_end = 20.0     # both ends held at 20 degrees C
n = 500          # interior points
steps = 300      # one new heat-source value per minute
h = L / (n + 1)
x = np.linspace(h, L - h, n)

# Tridiagonal coefficient matrix (never changes)
A = (np.diag(2.0 * np.ones(n))
     + np.diag(-np.ones(n - 1), 1)
     + np.diag(-np.ones(n - 1), -1))

# Heat source (W/m^3) rises from 10,000 to 40,000 over the 300 minutes
q_values = np.linspace(10_000, 40_000, steps)


def make_b(q):
    b = np.full(n, h ** 2 * q / k)
    b[0] += T_end
    b[-1] += T_end
    return b


# Method 1: solve from scratch at every step
t0 = time.perf_counter()
solutions_direct = [np.linalg.solve(A, make_b(q)) for q in q_values]
time_direct = time.perf_counter() - t0

# Method 2: factor once, reuse the factors
t0 = time.perf_counter()
factors = lu_factor(A)
solutions_lu = [lu_solve(factors, make_b(q)) for q in q_values]
time_lu = time.perf_counter() - t0

# Checks
max_diff = max(np.max(np.abs(a - b)) for a, b in zip(solutions_direct, solutions_lu))
max_residual = max(np.linalg.norm(make_b(q) - A @ T) for q, T in zip(q_values, solutions_lu))
q_last = q_values[-1]
exact_last = T_end + q_last / (2 * k) * x * (L - x)       # exact formula, uniform source
error_vs_exact = np.max(np.abs(solutions_lu[-1] - exact_last))

print(f"Points: {n}, time steps: {steps}")
print(f"Repeated solve: {time_direct:.4f} s")
print(f"LU once + reuse: {time_lu:.4f} s")
print(f"Speed-up: {time_direct / time_lu:.1f}x")
print(f"Largest difference between the two methods: {max_diff:.2e}")
print(f"Largest residual norm: {max_residual:.2e}")
print(f"Largest error against the exact formula (last step): {error_vs_exact:.2e}")

print(f"\n{'Minute':<10}{'Heat source (W/m^3)':>22}{'Hottest point (C)':>20}")
for step in [0, steps // 2, steps - 1]:
    print(f"{step + 1:<10}{q_values[step]:>22.0f}{solutions_lu[step].max():>20.3f}")

# Chart
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))

for step, color in zip([0, steps // 2, steps - 1], ["steelblue", "darkorange", "firebrick"]):
    ax1.plot(x, solutions_lu[step], color=color, label=f"Minute {step + 1}")
ax1.set_xlabel("Position along rod (m)")
ax1.set_ylabel("Temperature (C)")
ax1.set_title("Temperature along the rod")
ax1.legend()

ax2.bar(["Repeated solve", "LU once + reuse"], [time_direct, time_lu],
        color=["gray", "seagreen"])
ax2.set_ylabel("Total time (s)")
ax2.set_title(f"{steps} time steps, {n} points")

plt.tight_layout()
plt.savefig("docs/Task_07_variation_plot.png", dpi=150)
plt.show()