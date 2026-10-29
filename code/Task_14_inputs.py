import numpy as np
from scipy.optimize import curve_fit

users = np.array([50, 100, 150, 200, 250, 300, 350], dtype=float)
resp = np.array([82, 95, 115, 145, 185, 238, 305], dtype=float)


def rmse(y, yhat):
    return np.sqrt(np.mean((y - yhat) ** 2))


# 1. Change the model (polynomial degree)
print("=== Model comparison ===")
print(f"{'model':<12}{'RMSE (ms)':>11}{'at 400':>10}{'at 600':>10}")
for deg, name in [(1, "linear"), (2, "quadratic"), (3, "cubic")]:
    p = np.polyfit(users, resp, deg)
    print(f"{name:<12}{rmse(resp, np.polyval(p, users)):>11.2f}"
          f"{np.polyval(p, 400):>10.1f}{np.polyval(p, 600):>10.1f}")


def expo(x, a, b, c):
    return a * np.exp(b * x) + c


p, _ = curve_fit(expo, users, resp, p0=[10, 0.01, 70], maxfev=20000)
print(f"{'exponential':<12}{rmse(resp, expo(users, *p)):>11.2f}"
      f"{expo(400, *p):>10.1f}{expo(600, *p):>10.1f}")

# 2. Change one measurement (a faulty reading at 250 users: 185 -> 285)
print("\n=== One faulty measurement (185 changed to 285) ===")
bad = resp.copy()
bad[4] = 285.0
for label, y in [("original", resp), ("with outlier", bad)]:
    p = np.polyfit(users, y, 2)
    print(f"{label:<13} a={p[0]:.6f} b={p[1]:.4f} c={p[2]:.2f} "
          f"RMSE={rmse(y, np.polyval(p, users)):.2f}  at 400: {np.polyval(p, 400):.1f}")

# 3. Fewer points (drop 100, 200, 300)
print("\n=== Fewer points (50, 150, 250, 350 only) ===")
keep = [0, 2, 4, 6]
p = np.polyfit(users[keep], resp[keep], 2)
print(f"a={p[0]:.6f} b={p[1]:.4f} c={p[2]:.2f}  at 400: {np.polyval(p, 400):.1f}")
print(f"Prediction error on the dropped points: "
      f"{np.round(resp[[1, 3, 5]] - np.polyval(p, users[[1, 3, 5]]), 2)}")

# 4. Change the prediction load (extrapolation)
print("\n=== Quadratic prediction at other loads ===")
p = np.polyfit(users, resp, 2)
for x in [250, 400, 500, 800, 1000]:
    print(f"{x:>5} users -> {np.polyval(p, x):8.1f} ms")