import numpy as np

A = np.array([[4.0, 2.0], [8.0, 12.0]])

# Table 1: different observed totals (same server types)
print("Table 1: changing the observed totals")
print(f"{'CPU':<8}{'Memory':<10}{'Type A':>10}{'Type B':>10}{'Residual norm':>18}")
for cpu, mem in [(20, 72), (40, 144), (10, 36), (24, 80), (6, 100)]:
    b = np.array([cpu, mem], dtype=float)
    x = np.linalg.solve(A, b)
    print(f"{cpu:<8}{mem:<10}{x[0]:>10.3f}{x[1]:>10.3f}{np.linalg.norm(b - A @ x):>18.2e}")
print("A negative or fractional answer is not a valid server count.")

# Table 2: different server resource values (totals fixed at 20 CPU, 72 GB)
print("\nTable 2: changing the resources used by each server")
print(f"{'Matrix A':<26}{'Determinant':>13}{'Result':>30}")
b = np.array([20.0, 72.0])
matrices = [
    ("[[4,2],[8,12]]", np.array([[4.0, 2.0], [8.0, 12.0]])),
    ("[[2,1],[4,6]]", np.array([[2.0, 1.0], [4.0, 6.0]])),
    ("[[5,3],[7,9]]", np.array([[5.0, 3.0], [7.0, 9.0]])),
    ("[[4,2],[8,4]] (dependent)", np.array([[4.0, 2.0], [8.0, 4.0]])),
]
for name, M in matrices:
    det = np.linalg.det(M)
    try:
        x = np.linalg.solve(M, b)
        result = f"A = {x[0]:.3f}, B = {x[1]:.3f}"
    except np.linalg.LinAlgError:
        result = "No unique solution (singular)"
    print(f"{name:<26}{det:>13.4f}{result:>30}")

# Table 3: nearly singular matrices amplify small input errors
print("\nTable 3: sensitivity to a small change in b (nearly singular matrices)")
print(f"{'eps':<10}{'Condition no.':>16}{'x before':>22}{'x after':>22}")
for eps in [1.0, 1e-2, 1e-4, 1e-8]:
    M = np.array([[4.0, 2.0], [8.0, 4.0 + eps]])
    b1 = np.array([20.0, 40.0 + eps])
    b2 = b1 + np.array([0.0, 0.001])      # tiny measurement error
    x1 = np.linalg.solve(M, b1)
    x2 = np.linalg.solve(M, b2)
    print(f"{eps:<10.0e}{np.linalg.cond(M):>16.3e}"
          f"{str(np.round(x1, 3)):>22}{str(np.round(x2, 3)):>22}")