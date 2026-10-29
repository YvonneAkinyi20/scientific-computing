import numpy as np


def jacobi(A, b, tol=1e-8, max_iter=500):
    D = np.diag(A)
    R = A - np.diagflat(D)
    x = np.zeros_like(b)
    errors = []
    for _ in range(max_iter):
        x_new = (b - R @ x) / D
        error = np.linalg.norm(x_new - x, ord=np.inf)
        errors.append(error)
        x = x_new
        if error < tol:
            break
    return x, errors


def gauss_seidel(A, b, tol=1e-8, max_iter=500):
    x = np.zeros_like(b)
    errors = []
    for _ in range(max_iter):
        old = x.copy()
        for i in range(len(b)):
            x[i] = (b[i] - A[i, :i] @ x[:i] - A[i, i + 1:] @ old[i + 1:]) / A[i, i]
        error = np.linalg.norm(x - old, ord=np.inf)
        errors.append(error)
        if error < tol:
            break
    return x, errors


def tridiagonal(n):
    return 2 * np.eye(n) - np.eye(n, k=1) - np.eye(n, k=-1)


def spectral_radii(A):
    D = np.diag(np.diag(A))
    L = np.tril(A, -1)
    U = np.triu(A, 1)
    rj = max(abs(np.linalg.eigvals(-np.linalg.inv(D) @ (L + U))))
    rg = max(abs(np.linalg.eigvals(-np.linalg.inv(D + L) @ U)))
    return rj, rg


A5 = tridiagonal(5)
b5 = np.array([100., 0., 0., 0., 20.])
exact5 = np.linalg.solve(A5, b5)

# Table 1: different tolerances
print("Table 1: changing the tolerance")
print(f"{'Tolerance':<12}{'Jacobi iter':>13}{'GS iter':>10}{'Jacobi error':>16}{'GS error':>14}")
for tol in [1e-2, 1e-4, 1e-6, 1e-8, 1e-10]:
    xj, ej = jacobi(A5, b5, tol, 5000)
    xg, eg = gauss_seidel(A5, b5, tol, 5000)
    print(f"{tol:<12.0e}{len(ej):>13}{len(eg):>10}"
          f"{np.max(np.abs(xj - exact5)):>16.2e}{np.max(np.abs(xg - exact5)):>14.2e}")

# Table 2: different boundary temperatures
print("\nTable 2: changing the boundary temperatures (tolerance 1e-8)")
print(f"{'b':<26}{'Jacobi iter':>13}{'GS iter':>10}   Temperatures (Gauss-Seidel)")
for b in [[100, 0, 0, 0, 20], [200, 0, 0, 0, 40], [0, 0, 0, 0, 0],
          [50, 0, 0, 0, 50], [100, 0, 0, 0, -20]]:
    b = np.array(b, dtype=float)
    xj, ej = jacobi(A5, b, 1e-8, 5000)
    xg, eg = gauss_seidel(A5, b, 1e-8, 5000)
    print(f"{str(b.astype(int)):<26}{len(ej):>13}{len(eg):>10}   {np.round(xg, 3)}")

# Table 3: different numbers of grid points
print("\nTable 3: changing the number of grid points (tolerance 1e-8)")
print(f"{'n':<6}{'Jacobi iter':>13}{'GS iter':>10}{'Ratio':>8}{'Jacobi radius':>16}{'GS radius':>12}")
for n in [5, 10, 20, 40]:
    A = tridiagonal(n)
    b = np.zeros(n)
    b[0], b[-1] = 100.0, 20.0
    xj, ej = jacobi(A, b, 1e-8, 50000)
    xg, eg = gauss_seidel(A, b, 1e-8, 50000)
    rj, rg = spectral_radii(A)
    print(f"{n:<6}{len(ej):>13}{len(eg):>10}{len(ej) / len(eg):>8.2f}{rj:>16.5f}{rg:>12.5f}")

# Table 4: changing the matrix (convergence needs a suitable matrix)
print("\nTable 4: changing the matrix (maximum 100 iterations)")
print(f"{'Matrix':<34}{'Jacobi radius':>15}{'GS radius':>11}{'Jacobi':>14}{'Gauss-Seidel':>16}")
cases = [
    ("Diagonally dominant 3x3", np.array([[4., -1, 0], [-1, 4, -1], [0, -1, 4]]),
     np.array([15., 10, 10])),
    ("Weakly dominant 3x3", tridiagonal(3), np.array([100., 0, 20])),
    ("[[1,2],[3,1]] (not dominant)", np.array([[1., 2], [3, 1]]), np.array([5., 5])),
    ("[[3,1],[1,2]] (rows swapped)", np.array([[3., 1], [1, 2]]), np.array([5., 5])),
]
for name, A, b in cases:
    rj, rg = spectral_radii(A)
    xj, ej = jacobi(A, b, 1e-8, 100)
    xg, eg = gauss_seidel(A, b, 1e-8, 100)
    rj_text = f"{len(ej)} iter" if ej[-1] < 1e-8 else "diverges"
    rg_text = f"{len(eg)} iter" if eg[-1] < 1e-8 else "diverges"
    print(f"{name:<34}{rj:>15.4f}{rg:>11.4f}{rj_text:>14}{rg_text:>16}")