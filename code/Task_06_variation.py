import matplotlib.pyplot as plt
import numpy as np

# Rows = nutrients (N, P, K); columns = fertilizers (F1, F2, F3)
# Each value is the fraction of that nutrient in one kg of fertilizer
A = np.array([
    [0.20, 0.10, 0.05],
    [0.10, 0.30, 0.05],
    [0.10, 0.10, 0.40]
])
# Nutrients needed per hectare (kg of N, P, K)
b = np.array([30.0, 25.0, 30.0])
# Price per kg of each fertilizer (KES)
price = np.array([90.0, 110.0, 80.0])

nutrients = ["N", "P", "K"]
fertilizers = ["F1", "F2", "F3"]

print("Nutrient matrix A:\n", A)
print("Required nutrients b (kg):", b)
print(f"Determinant: {np.linalg.det(A):.5f}")
print(f"Condition number: {np.linalg.cond(A):.2f}")

x = np.linalg.solve(A, b)
supplied = A @ x
residual = b - supplied

print("\nKilograms of each fertilizer needed:")
for name, kg in zip(fertilizers, x):
    print(f"  {name}: {kg:.2f} kg")
print("All amounts are positive (practical):", bool(np.all(x > 0)))
print("Supplied nutrients (A @ x):", np.round(supplied, 4))
print("Residual:", residual)
print("Residual norm:", np.linalg.norm(residual))
print(f"Total fertilizer: {x.sum():.2f} kg")
print(f"Total cost: KES {x @ price:,.2f}")

# Sensitivity: what if the crop needs 1% more of every nutrient?
x_new = np.linalg.solve(A, b * 1.01)
print("\nIf requirements rise by 1%:")
for name, old, new in zip(fertilizers, x, x_new):
    print(f"  {name}: {old:.2f} -> {new:.2f} kg  (change {100 * (new - old) / old:.2f}%)")

# Chart
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))

ax1.bar(fertilizers, x, color="seagreen")
ax1.set_ylabel("Amount needed (kg)")
ax1.set_title("Fertilizer needed per hectare")

pos = np.arange(len(nutrients))
ax2.bar(pos - 0.2, b, width=0.4, label="Required", color="steelblue")
ax2.bar(pos + 0.2, supplied, width=0.4, label="Supplied (A @ x)", color="darkorange")
ax2.set_xticks(pos)
ax2.set_xticklabels(nutrients)
ax2.set_ylabel("Nutrient (kg)")
ax2.set_title("Nutrients required and supplied")
ax2.legend()

plt.tight_layout()
plt.savefig("docs/Task_06_variation_plot.png", dpi=150)
plt.show()