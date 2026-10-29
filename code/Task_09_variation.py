import matplotlib.pyplot as plt
import numpy as np

# Building settings
m = 2.0e5        # mass of each floor (kg)
k = 5.0e7        # stiffness of each storey (N/m)
zeta = 0.02      # damping ratio (2%)

K = k * np.array([[ 2., -1.,  0.],
                  [-1.,  2., -1.],
                  [ 0., -1.,  1.]])
M = m * np.eye(3)
A = np.linalg.inv(M) @ K          # eigenvalues of this matrix are omega squared

# Eigenvalues and eigenvectors (eigh is the version for symmetric matrices)
w2, V = np.linalg.eigh(A)
omega = np.sqrt(w2)
freq_n = omega / (2 * np.pi)

print("Stiffness matrix K (N/m):\n", K)
w2_eig = np.sort(np.real(np.linalg.eig(A)[0]))
print("\neigh and eig give the same eigenvalues:", np.allclose(w2, w2_eig))
print("Mode shapes are perpendicular (V.T @ V = I):", np.allclose(V.T @ V, np.eye(3)))
print("Largest verification error ||K v - w2 M v||:",
      f"{max(np.linalg.norm(K @ V[:, i] - w2[i] * (M @ V[:, i])) for i in range(3)):.2e}")

# Mode shapes scaled so that the top floor moves 1 unit
shapes = V / V[-1, :]

# Response of the top floor to a force on the top floor
Phi = V / np.sqrt(m)                                  # mass-normalised modes
freq = np.linspace(0.01, 6.0, 3000)
w = 2 * np.pi * freq
H = sum(Phi[2, i] ** 2 / (w2[i] - w ** 2 + 2j * zeta * omega[i] * w) for i in range(3))
H0 = np.sum(Phi[2, :] ** 2 / w2)                      # static response (w = 0)
amplification = [abs(sum(Phi[2, j] ** 2 / (w2[j] - omega[i] ** 2 + 2j * zeta * omega[j] * omega[i])
                         for j in range(3))) / H0 for i in range(3)]

print(f"\n{'Mode':<6}{'w^2':>12}{'w (rad/s)':>12}{'f (Hz)':>9}{'Period (s)':>12}{'Amplification':>15}")
for i in range(3):
    print(f"{i + 1:<6}{w2[i]:>12.3f}{omega[i]:>12.3f}{freq_n[i]:>9.3f}"
          f"{1 / freq_n[i]:>12.3f}{amplification[i]:>15.1f}")

print("\nMode shapes (top floor = 1):")
print(f"{'Mode':<6}{'Floor 1':>10}{'Floor 2':>10}{'Floor 3':>10}")
for i in range(3):
    print(f"{i + 1:<6}{shapes[0, i]:>10.3f}{shapes[1, i]:>10.3f}{shapes[2, i]:>10.3f}")

# Chart
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8))

heights = [0, 1, 2, 3]
for i, color in enumerate(["steelblue", "darkorange", "seagreen"]):
    ax1.plot(np.concatenate(([0], shapes[:, i])), heights, "o-", color=color,
             label=f"Mode {i + 1} ({freq_n[i]:.2f} Hz)")
ax1.axvline(0, color="black", linewidth=0.8)
ax1.set_xlabel("Sideways movement (top floor = 1)")
ax1.set_ylabel("Floor (0 = ground)")
ax1.set_yticks(heights)
ax1.set_title("Mode shapes of the building")
ax1.legend()

ax2.semilogy(freq, np.abs(H) / H0, color="firebrick")
for f_i in freq_n:
    ax2.axvline(f_i, color="gray", linestyle="--", linewidth=0.8)
ax2.set_xlabel("Forcing frequency (Hz)")
ax2.set_ylabel("Top-floor response / static response")
ax2.set_title("Resonance at the natural frequencies")
ax2.grid(True)

plt.tight_layout()
plt.savefig("docs/Task_09_variation_plot.png", dpi=150)
plt.show()