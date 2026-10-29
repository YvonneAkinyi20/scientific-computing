import numpy as np
from scipy.optimize import root_scalar


def model(Tamb=25.0, Q=10.0, c=20.0):
    f = lambda T: T - Tamb - Q * np.exp(-T / c)
    g = lambda T: Tamb + Q * np.exp(-T / c)
    return f, g


def bisection(f, a, b, tol=1e-10, max_iter=200):
    """Returns (root, iterations), or None when there is no sign change."""
    if f(a) * f(b) > 0:
        return None
    for i in range(1, max_iter + 1):
        c = (a + b) / 2
        if f(c) == 0:
            return c, i
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
        if (b - a) / 2 < tol:
            return (a + b) / 2, i
    return (a + b) / 2, max_iter


def fixed_point(g, x0, tol=1e-10, max_iter=100):
    """Returns (value, iterations, converged)."""
    x = x0
    with np.errstate(all="ignore"):
        for i in range(1, max_iter + 1):
            x_new = g(x)
            if not np.isfinite(x_new) or abs(x_new) > 1e6:
                return x_new, i, False
            if abs(x_new - x) < tol:
                return x_new, i, True
            x = x_new
    return x, max_iter, False


f, g = model()
true_root = root_scalar(f, bracket=[20, 40], method="brentq", xtol=1e-14).root

# Table 1: different tolerances
print("Table 1: changing the tolerance (bracket [20, 40])")
print(f"{'Tolerance':<12}{'Iterations':>12}{'Predicted':>11}{'Root':>14}{'|f(root)|':>13}{'Error':>12}")
for tol in [1e-2, 1e-4, 1e-6, 1e-8, 1e-10]:
    root, it = bisection(f, 20, 40, tol)
    predicted = int(np.floor(np.log2(20 / (2 * tol)))) + 1
    print(f"{tol:<12.0e}{it:>12}{predicted:>11}{root:>14.8f}{abs(f(root)):>13.2e}{abs(root - true_root):>12.2e}")

# Table 2: different starting brackets
print("\nTable 2: changing the bracket (tolerance 1e-10)")
print(f"{'Bracket':<16}{'f(a)':>10}{'f(b)':>10}{'Result':>34}")
for a, b in [(20, 40), (26, 30), (27, 28), (0, 100), (-100, 100), (30, 40), (0, 20)]:
    out = bisection(f, a, b)
    if out is None:
        text = "no sign change, cannot start"
    else:
        text = f"root {out[0]:.6f} in {out[1]} iterations"
    label = f"[{a}, {b}]"
    print(f"{label:<16}{f(a):>10.3f}{f(b):>10.3f}{text:>34}")

# Table 3: different