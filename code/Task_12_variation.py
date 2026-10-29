from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import root

# A radar at the origin detects objects within R = 6 km (a circle).
# An aircraft flies along the curved path y = 0.05 x^2 - 4 (km).
# Where does it enter and leave radar coverage?
R = 6.0
a, b = 0.05, 4.0


def equations(z):
    x, y = z
    return [x**2 + y**2 - R**2,
            y - (a * x**2 - b)]


points = []
for guess in ([5.0, -2.0], [-5.0, -2.0]):
    sol = root(equations, guess)
    print("Initial guess:", guess)
    print("Intersection (km):", np.round(sol.x, 4))
    print("Residuals:", equations(sol.x))
    print("Converged:", sol.success, "\n")
    points.append(sol.x)

points = np.array(points)
width = abs(points[0, 0] - points[1, 0])
speed = 600.0                                   # assumed horizontal speed, km/h
print(f"Horizontal distance inside coverage: {width:.3f} km")
print(f"Time inside coverage at {speed:.0f} km/h: {width / speed * 60:.2f} minutes")

out = Path(__file__).resolve().parent.parent / "docs"
out.mkdir(exist_ok=True)

theta = np.linspace(0, 2 * np.pi, 400)
xs = np.linspace(-9, 9, 400)
plt.figure(figsize=(6.5, 6))
plt.plot(R * np.cos(theta), R * np.sin(theta), label="Radar range (6 km)")
plt.plot(xs, a * xs**2 - b, label="Flight path")
plt.scatter(points[:, 0], points[:, 1], color="red", zorder=3,
            label="Entry / exit points")
plt.scatter([0], [0], color="black", marker="^", label="Radar")
plt.axis("equal")
plt.xlim(-9, 9)
plt.ylim(-8, 8)
plt.xlabel("x (km)")
plt.ylabel("y (km)")
plt.title("Aircraft path crossing radar coverage")
plt.legend()
plt.tight_layout()
plt.savefig(out / "Task_12_variation_plot.png", dpi=150)
plt.show()