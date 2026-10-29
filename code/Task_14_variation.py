from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# Monthly active users (thousands) of a new mobile-payment app
months = np.arange(1, 9, dtype=float)
users_k = np.array([12, 15, 19, 24, 31, 38, 48, 60], dtype=float)


def linear(t, a, b):
    return a * t + b


def exponential(t, a, b):
    return a * np.exp(b * t)


def rmse(y, yhat):
    return np.sqrt(np.mean((y - yhat) ** 2))


p_lin, _ = curve_fit(linear, months, users_k)
p_exp, _ = curve_fit(exponential, months, users_k, p0=[10, 0.2])

print(f"Linear     : y = {p_lin[0]:.3f} t + {p_lin[1]:.2f}   RMSE = "
      f"{rmse(users_k, linear(months, *p_lin)):.2f}")
print(f"Exponential: y = {p_exp[0]:.3f} exp({p_exp[1]:.4f} t)   RMSE = "
      f"{rmse(users_k, exponential(months, *p_exp)):.2f}")
print(f"Monthly growth rate: {(np.exp(p_exp[1]) - 1) * 100:.1f}%")
print(f"Doubling time: {np.log(2) / p_exp[1]:.2f} months")
for m in [9, 12]:
    print(f"Forecast month {m}: linear {linear(m, *p_lin):.1f}k, "
          f"exponential {exponential(m, *p_exp):.1f}k")

out = Path(__file__).resolve().parent.parent / "docs"
out.mkdir(exist_ok=True)
t = np.linspace(1, 12, 200)
fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
ax[0].scatter(months, users_k, color="black", label="Observed")
ax[0].plot(t, linear(t, *p_lin), "--", label="Linear fit")
ax[0].plot(t, exponential(t, *p_exp), label="Exponential fit")
ax[0].set_xlabel("Month")
ax[0].set_ylabel("Active users (thousands)")
ax[0].set_title("User growth and forecast")
ax[0].legend()
ax[0].grid(True)
ax[1].scatter(months, users_k - linear(months, *p_lin), label="Linear residuals")
ax[1].scatter(months, users_k - exponential(months, *p_exp), marker="s",
              label="Exponential residuals")
ax[1].axhline(0, color="grey")
ax[1].set_xlabel("Month")
ax[1].set_ylabel("Residual (thousands)")
ax[1].set_title("Residuals")
ax[1].legend()
ax[1].grid(True)
plt.tight_layout()
plt.savefig(out / "Task_14_variation_plot.png", dpi=150)
plt.show()