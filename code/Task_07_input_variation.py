import time

import numpy as np
from scipy.linalg import lu, lu_factor, lu_solve


def gaussian_elimination(A, b):
    """Gaussian elimination with partial pivoting and back-substitution."""
    A = A.astype(float).copy()
    b = b.astype(float).copy()
    n = len(b)
    for k in range(n - 1):
        p = k + np.argmax(np.abs(A[k:, k]))      # pivot row
        if p != k:
            A[[k, p]] = A[[p, k]]
            b[[k, p]] = b[[p, k]]
        for i in range(k + 1, n):
            factor = A[i, k] / A[k, k]
            A[i, k:] -= factor * A[k, k:]
            b[i] -= factor * b[k]
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):               # back-substitution
        x[i] = (b[i] - A[i, i + 1:] @ x[i + 1:]) / A[i, i]
    return x


A = np.array([[4.0, -1.0, 0.0],
              [-1.0, 4.0, -1.0],
              [0.0, -1.0, 3.0]])

# Table 1: different measurement vectors, same matrix
print("Table 1: changing the measurement vector b")
print(f"{'b':<22}{'Solution':>34}{'Residual norm':>16}{'Matches solve':>15}")
lu_piv = lu_factor(A)
for b in [[15, 10, 10], [30, 20, 20], [0, 0, 0], [1, 0, 0], [-15, 10, 5]]:
    b = np.array(b, dtype=float)
    x = lu_solve(lu_piv, b)
    print(f"{str(b.astype(int)):<22}{str(np.round(x, 4)):>34}"
          f"{np.linalg.norm(b - A @ x):>16.2e}{str(np.allclose(x, np.linalg.solve(A, b))):>15}")

# Table 2: the factors P, L, U
P, L, U = lu(A)
print("\nTable 2: LU factors of A (A = P @ L @ U)")
print("P:\n", P)
print("L:\n", np.round(L, 4))
print("U:\n", np.round(U, 4))
print("P @ L @ U equals A:", np.allclose(P @ L @ U, A))

# Table 3: hand-written Gaussian elimination versus NumPy
print("\nTable 3: Gaussian elimination written by hand")
for b in [[15, 10, 10], [16, 11, 9], [14, 12, 11]]:
    b = np.array(b, dtype=float)
    mine = gaussian_elimination(A, b)
    ref = np.linalg.solve(A, b)
    print(f"b = {b.astype(int)}  elimination = {np.round(mine, 6)}  "
          f"same as solve: {np.allclose(mine, ref)}")

# Table 4: different matrices
print("\nTable 4: changing the matrix")
print(f"{'Matrix':<28}{'Determinant':>13}{'Rank':>6}{'Condition no.':>16}{'Result':>26}")
b = np.array([15.0, 10.0, 10.0])
matrices = [
    ("Original (diagonal 4,4,3)", A),
    ("Weaker diagonal (2,2,2)", np.array([[2.0, -1, 0], [-1, 2, -1], [0, -1, 2]])),
    ("Very weak diagonal", np.array([[1.01, -1, 0], [-1, 1.01, -1], [0, -1, 1.01]])),
    ("Singular [[1,2,3],[4,5,6],[7,8,9]]", np.array([[1.0, 2, 3], [4, 5, 6], [7, 8, 9]])),
]
for name, M in matrices:
    rank = np.linalg.matrix_rank(M)
    cond = np.linalg.cond(M)
    result = "No unique solution" if rank < 3 else str(np.round(np.linalg.solve(M, b), 3))
    print(f"{name:<28}{np.linalg.det(M):>13.4f}{rank:>6}{cond:>16.3e}{result:>26}")

# Table 5: timing with 200 measurement vectors for different matrix sizes
print("\nTable 5: LU reuse versus repeated solving (200 vectors)")
print(f"{'n':<8}{'Repeated solve (s)':>20}{'LU once + reuse (s)':>22}{'Speed-up':>10}")
rng = np.random.default_rng(42)
for n in [100, 500, 1000]:
    M = rng.random((n, n)) + n * np.eye(n)
    bs = rng.random((200, n))
    t0 = time.perf_counter()
    for b in bs:
        np.linalg.solve(M, b)
    t_repeat = time.perf_counter() - t0
    t0 = time.perf_counter()
    f = lu_factor(M)
    for b in bs:
        lu_solve(f, b)
    t_lu = time.perf_counter() - t0
    print(f"{n:<8}{t_repeat:>20.4f}{t_lu:>22.4f}{t_repeat / t_lu:>9.1f}x")python code/Task_07_input_variation.py
    