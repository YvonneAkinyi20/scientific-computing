import time

import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import diags, identity, kron
from scipy.sparse.linalg import spsolve

# Plate settings
N = 30                                   # interior points per side (900 unknowns)
top, bottom, left, right = 100.0, 0.0, 50.0, 0.0     # edge temperatures (C)
tol = 1e-6
max_iter = 20000


def make_grid():
    T = np.zeros((N + 2, N + 2))
    T[0, :], T[-1, :], T[:, 0], T[:, -1] = top, bottom, left, right
    return T


def jacobi():
    T = make_grid()
    errors = []
    for _ in range(max_iter):
        new = T.copy()
        new[1:-1, 1:-1] = 0.25 * (T[:-2, 1:-1] + T[2:, 1:-1] + T[1:-1, :-2] + T[1:-1, 2:])
        error = np.max(np.abs(new - T))
        errors.append(error)
        T = new
        if error < tol:
            break
    return T, errors


def sor(omega):
    """omega = 1 gives Gauss-Seidel; omega between 1 and 2 gives SOR."""
    T = make_grid()
    errors = []
    for _ in range(max_iter):
        error = 0.0
        for i in range(1, N + 1):
            for j in range(1, N + 1):
                gs = 0.25 * (T[i - 1, j] + T[i + 1, j] + T[i, j - 1] + T[i, j + 1])
                new = (1 - omega) * T[i, j] + omega * gs
                error = max(error, abs(new - T[i, j]))
                T[i, j] = new
        errors.append(error)
        if error < tol:
            break
    return T, errors


# Direct sparse solution for comparison (A x = b with 900 unknowns)
I = identity(N)
T1 = diags([-1.0, 2.0, -1.0], [-1, 0, 1], shape=(N, N))
A = (kron(I, T1) + kron(T1, I)).tocsc()
b = np.zeros((N, N))
b[0, :] += top
b[-1, :] += bottom
b[:, 0] += left
b[:, -1] += right

t0 = time.perf_counter()
direct = spsolve(A, b.ravel()).reshape(N, N)
time_direct = time.perf_counter() - t0

print(f"Unknowns: {N * N}, non-zero coefficients: {A.nnz} "
      f"({100 * A.nnz / (N * N) ** 2:.2f}% of the matrix)")

omega_best = 2 / (1 + np.sin(np.pi / (N + 1)))
results = {}
for name, func in [("Jacobi", jacobi),
                   ("Gauss-Seidel", lambda: sor(1.0)),
                   (f"SOR (omega={omega_best:.2f})", lambda: sor(omega_best))]:
    t0 = time.perf_counter()
    T, errors = func()
    elapsed = time.perf_counter() - t0
    error_vs_direct = np.max(np.abs(T[1:-1, 1:-1] - direct))
    results[name] = (T, errors, elapsed, error_vs_direct)

print(f"\n{'Method':<22}{'Iterations':>12}{'Time (s)':>11}{'Error vs direct':>18}")
for name, (T, errors, elapsed, err) in results.items():
    print(f"{name:<22}{len(errors):>12}{elapsed:>11.3f}{err:>18.2e}")
print(f"{'Direct sparse solve':<22}{'-':>12}{time_direct:>11.3f}{'-':>18}")

# Temperature at a few points
T_gs = results["Gauss-Seidel"][0]
print("\nTemperature at selected points (Gauss-Seidel):")
for label, (i, j) in {"Near top edge": (1, N // 2), "Centre": (N // 2, N // 2),
                      "Near left edge": (N // 2, 1), "Near bottom edge": (N, N // 2)}.items():
    print(f"  {label:<18}{T_gs[i, j]:.2f} C")

# Chart
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8))

for name, (T, errors, elapsed, err) in results.items():
    ax1.semilogy(errors, label=f"{name} ({len(errors)} iterations)")
ax1.axhline(tol, color="gray", linestyle="--", linewidth=0.8)
ax1.set_xlabel("Iteration")
ax1.set_ylabel("Maximum change")
ax1.set_title("Convergence on the 30 x 30 plate")
ax1.legend()
ax1.grid(True)

image = ax2.imshow(T_gs, cmap="inferno", origin="upper")
fig.colorbar(image, ax=ax2, label="Temperature (C)")
ax2.set_title("Temperature across the plate")

plt.tight_layout()
plt.savefig("docs/Task_08_variation_plot.png", dpi=150)
plt.show()