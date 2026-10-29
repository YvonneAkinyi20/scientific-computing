import numpy as np
from scipy.optimize import root

# 1. Change the initial guess (original circle and parabola)
print("=== Different initial guesses (circle r^2=4, parabola y=x^2-1) ===")
def eqs(z, r2=4.0, c=1.0):
    x, y = z
    return [x**2 + y**2 - r2, y - (x**2 - c)]

for guess in ([1, 1], [-1, 1], [0, 2], [2, -2], [0, -2], [3, 3]):
    sol = root(eqs, guess)
    print(f"guess {guess!s:<10} -> {np.round(sol.x, 6)}  "
          f"converged: {sol.success}  max|residual| = {np.abs(eqs(sol.x)).max():.1e}")

# 2. Change the circle (r^2) and the parabola (y = x^2 - c)
print("\n=== Different circles and parabolas ===")
print(f"{'r^2':>5}{'c':>5}  {'real intersections found (x, y)'}")
cases = [(4, 1), (9, 1), (1, 1), (4, -1), (4, 5)]
grid = [[x, y] for x in range(-3, 4) for y in range(-3, 4)]
for r2, c in cases:
    found = set()
    for g in grid:
        s = root(eqs, g, args=(r2, c))
        if s.success and np.allclose(eqs(s.x, r2, c), 0, atol=1e-8):
            found.add((round(s.x[0], 4) + 0.0, round(s.x[1], 4) + 0.0))
    print(f"{r2:>5}{c:>5}  {sorted(found) if found else 'none'}")