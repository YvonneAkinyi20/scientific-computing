import math
from decimal import Decimal

import matplotlib.pyplot as plt
import numpy as np

# Real-world case: summing 1,000,000 payments of KES 0.10
n = 1_000_000
amount = 0.10
exact_total = Decimal("0.10") * n          # exact decimal arithmetic

loop_total = 0.0
for _ in range(n):
    loop_total += amount                   # plain float addition

numpy_total = float(np.sum(np.full(n, amount)))   # pairwise summation
fsum_total = math.fsum([amount] * n)              # error-compensated sum

methods = {
    "Python loop": loop_total,
    "np.sum": numpy_total,
    "math.fsum": fsum_total,
}

print(f"Exact total (Decimal): {exact_total}")
print(f"{'Method':<14}{'Total':>24}{'Absolute error':>18}{'Relative error %':>20}")
abs_errors = []
for name, total in methods.items():
    abs_err = abs(Decimal(total) - exact_total)
    rel_err = abs_err / exact_total
    abs_errors.append(float(abs_err))
    print(f"{name:<14}{total:>24.12f}{float(abs_err):>18.3e}{float(rel_err) * 100:>20.3e}")

print("\nLoop total == 100000.0 ?", loop_total == 100000.0)
print("np.isclose(loop total, 100000.0) ?", np.isclose(loop_total, 100000.0))

# Unstable vs stable formula over many values of x
x = np.logspace(-16, -1, 200)
direct = (np.sqrt(1 + x) - 1) / x
stable = 1 / (np.sqrt(1 + x) + 1)
rel_error = np.maximum(np.abs(direct - stable) / np.abs(stable), 1e-18)

# Chart
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))

floor = 1e-14
ax1.bar(list(methods.keys()), [max(e, floor) for e in abs_errors], color="steelblue")
ax1.set_yscale("log")
ax1.set_ylabel("Absolute error (KES, log scale)")
ax1.set_title("Error when summing 1,000,000 x KES 0.10")

ax2.loglog(x, rel_error, color="firebrick")
ax2.set_xlabel("x")
ax2.set_ylabel("Relative error of direct formula")
ax2.set_title("Unstable formula: error grows as x shrinks")

plt.tight_layout()
plt.savefig("docs/Task_04_variation_plot.png", dpi=150)
plt.show()