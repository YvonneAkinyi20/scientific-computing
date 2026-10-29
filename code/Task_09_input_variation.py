import numpy as np


def adjacency(n, edges):
    A = np.zeros((n, n))
    for i, j in edges:
        A[i, j] = A[j, i] = 1.0
    return A


def centrality(A):
    """Eigenvector centrality (eigh is the version for symmetric matrices)."""
    vals, vecs = np.linalg.eigh(A)
    v = np.abs(vecs[:, -1])
    return vals[-1], v / v.sum()


def power_iteration(A, x0, tol=1e-10, max_iter=1000):
    x = x0 / np.linalg.norm(x0)
    for i in range(1, max_iter + 1):
        y = A @ x
        y = y / np.linalg.norm(y)
        if np.linalg.norm(y - x) < tol:
            return y @ A @ y, i, True
        x = y
    return x @ A @ x, max_iter, False


# Table 1: different matrices
print("Table 1: eigenvalues of different matrices")
print(f"{'Matrix':<26}{'Eigenvalues':<30}{'Trace=sum':>11}{'Det=prod':>10}{'Max residual':>14}")
mats = [
    ("Diagonal [[2,0],[0,3]]", np.array([[2., 0], [0, 3]])),
    ("[[4,1],[2,3]]", np.array([[4., 1], [2, 3]])),
    ("Symmetric [[2,1],[1,2]]", np.array([[2., 1], [1, 2]])),
    ("Rotation 90 deg", np.array([[0., -1], [1, 0]])),
    ("Singular [[1,2],[2,4]]", np.array([[1., 2], [2, 4]])),
]
for name, M in mats:
    vals, vecs = np.linalg.eig(M)
    res = max(np.linalg.norm(M @ vecs[:, i] - vals[i] * vecs[:, i]) for i in range(len(vals)))
    tr = np.isclose(np.trace(M), vals.sum())
    dt = np.isclose(np.linalg.det(M), np.prod(vals))
    print(f"{name:<26}{str(np.round(vals, 4)):<30}{str(tr):>11}{str(dt):>10}{res:>14.2e}")

# Table 2: different networks
orig_edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)]
networks = {
    "Original (A,B,C,D)": adjacency(4, orig_edges),
    "Add edge A-D": adjacency(4, orig_edges + [(0, 3)]),
    "Remove edge B-C": adjacency(4, [(0, 1), (0, 2), (1, 3), (2, 3)]),
    "Star (hub + 4 nodes)": adjacency(5, [(0, i) for i in range(1, 5)]),
    "Path of 4 nodes": adjacency(4, [(0, 1), (1, 2), (2, 3)]),
}
print("\nTable 2: changing the network")
print(f"{'Network':<24}{'Dominant eigenvalue':>21}   Importance of nodes A, B, C, ...")
for name, A in networks.items():
    lam, c = centrality(A)
    print(f"{name:<24}{lam:>21.4f}   {np.round(c, 4)}")

# Table 3: scaling and shifting
A = networks["Original (A,B,C,D)"]
_, base = centrality(A)
print("\nTable 3: scaling and shifting the original matrix")
print(f"{'Matrix':<12}{'Eigenvalues':<44}{'Same dominant vector':>22}")
for name, M in [("A", A), ("2A", 2 * A), ("A + 3I", A + 3 * np.eye(4)), ("-A", -A)]:
    vals = np.linalg.eigvalsh(M)[::-1]
    _, c = centrality(M)
    print(f"{name:<12}{str(np.round(vals, 4)):<44}{str(np.allclose(c, base)):>22}")

# Table 4: power iteration
print("\nTable 4: power iteration (start vector 1, 2, 3, ...; tolerance 1e-10)")
print(f"{'Network':<24}{'|l2|/|l1|':>11}{'On A':>20}{'On A + I':>16}{'Eigenvalue found':>18}")
extra = dict(networks)
extra["Complete graph K4"] = adjacency(4, [(i, j) for i in range(4) for j in range(i + 1, 4)])
extra["Ring of 5"] = adjacency(5, [(i, (i + 1) % 5) for i in range(5)])
for name, A in extra.items():
    n = len(A)
    x0 = np.arange(1, n + 1, dtype=float)
    mags = np.sort(np.abs(np.linalg.eigvalsh(A)))[::-1]
    ratio = mags[1] / mags[0]
    lam1, it1, ok1 = power_iteration(A, x0)
    lam2, it2, ok2 = power_iteration(A + np.eye(n), x0)
    text1 = f"{it1} iterations" if ok1 else "no convergence"
    text2 = f"{it2} iterations" if ok2 else "no convergence"
    print(f"{name:<24}{ratio:>11.4f}{text1:>20}{text2:>16}{lam2 - 1:>18.4f}")