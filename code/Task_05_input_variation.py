import numpy as np

points = np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]])


def rotation_matrix(deg):
    a = np.deg2rad(deg)
    return np.array([[np.cos(a), -np.sin(a)],
                     [np.sin(a),  np.cos(a)]])


def polygon_area(pts):
    # Shoelace formula
    x, y = pts[:, 0], pts[:, 1]
    return 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))


# Table 1: different rotation angles (scale fixed at 2.0 and 1.5)
scale = np.array([[2.0, 0.0], [0.0, 1.5]])
print("Table 1: changing the rotation angle")
print(f"{'Angle':<8}{'Corner (1,1) becomes':>28}{'Determinant':>14}")
for deg in [0, 30, 45, 90, 180]:
    T = rotation_matrix(deg) @ scale
    moved = points @ T.T
    corner = f"({moved[2, 0]:.4f}, {moved[2, 1]:.4f})"
    print(f"{deg:<8}{corner:>28}{np.linalg.det(T):>14.4f}")

# Table 2: different scale factors (rotation fixed at 45 degrees)
print("\nTable 2: changing the scale factors")
print(f"{'sx':<6}{'sy':<6}{'Determinant':>14}{'New area':>12}")
for sx, sy in [(1, 1), (2, 1.5), (3, 3), (0.5, 0.5), (2, 0)]:
    S = np.array([[sx, 0.0], [0.0, sy]])
    T = rotation_matrix(45) @ S
    moved = points @ T.T
    print(f"{sx:<6}{sy:<6}{np.linalg.det(T):>14.4f}{polygon_area(moved):>12.4f}")

# Table 3: order of multiplication matters
R = rotation_matrix(45)
S = np.array([[2.0, 0.0], [0.0, 1.5]])
print("\nTable 3: rotation @ scale versus scale @ rotation")
print("rotation @ scale:\n", np.round(R @ S, 4))
print("scale @ rotation:\n", np.round(S @ R, 4))
print("Are they equal?", np.allclose(R @ S, S @ R))

# Table 4: invertibility
print("\nTable 4: determinant and inverse")
tests = {
    "A = [[1,2],[3,4]]": np.array([[1.0, 2.0], [3.0, 4.0]]),
    "B = [[2,4],[1,2]]": np.array([[2.0, 4.0], [1.0, 2.0]]),
    "Combined transformation": R @ S,
}
for name, M in tests.items():
    det = np.linalg.det(M)
    print(f"\n{name}   determinant = {det:.4f}")
    try:
        inv = np.linalg.inv(M)
        print("Inverse:\n", np.round(inv, 4))
        print("M @ inverse is the identity:", np.allclose(M @ inv, np.eye(2)))
    except np.linalg.LinAlgError:
        print("Not invertible (singular matrix)")