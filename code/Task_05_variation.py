import matplotlib.pyplot as plt
import numpy as np

# Resistors in ohms
R1, R2, R3, R4, R5 = 10.0, 20.0, 30.0, 15.0, 25.0
# Voltage sources in volts
V1, V2 = 12.0, 5.0

# Mesh-current equations: A @ I = V
A = np.array([
    [R1 + R2,      -R2,         0.0],
    [-R2,     R2 + R3 + R4,     -R4],
    [0.0,          -R4,     R4 + R5]
])
V = np.array([V1, 0.0, -V2])

det = np.linalg.det(A)
print("Resistance matrix A:\n", A)
print("Voltage vector V:", V)
print(f"Determinant of A: {det:.2f}")

if abs(det) > 1e-12:
    inverse = np.linalg.inv(A)
    currents_inv = inverse @ V
    currents_solve = np.linalg.solve(A, V)

    print("\nA @ inverse is the identity:", np.allclose(A @ inverse, np.eye(3)))
    print("Currents using inverse (A):", np.round(currents_inv * 1000, 4))
    print("Currents using solve   (A):", np.round(currents_solve * 1000, 4))
    print("Both methods agree:", np.allclose(currents_inv, currents_solve))

    I1, I2, I3 = currents_solve
    print("\nMesh currents (mA):")
    for i, c in enumerate(currents_solve, start=1):
        print(f"  I{i} = {c * 1000:.3f} mA")

    # Current and power in each resistor
    branch_current = {"R1": I1, "R2": I1 - I2, "R3": I2, "R4": I2 - I3, "R5": I3}
    resistance = {"R1": R1, "R2": R2, "R3": R3, "R4": R4, "R5": R5}
    power_mw = {k: branch_current[k] ** 2 * resistance[k] * 1000 for k in resistance}

    print(f"\n{'Resistor':<10}{'Current (mA)':>14}{'Power (mW)':>14}")
    for k in resistance:
        print(f"{k:<10}{branch_current[k] * 1000:>14.3f}{power_mw[k]:>14.3f}")

    # Check: power supplied by the sources equals power used by the resistors
    supplied = (V1 * I1 + (-V2) * I3) * 1000
    print(f"\nPower supplied: {supplied:.3f} mW, power used: {sum(power_mw.values()):.3f} mW")
    print("Power balance holds:", np.isclose(supplied, sum(power_mw.values())))

    # Chart
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
    ax1.bar(["I1", "I2", "I3"], currents_solve * 1000, color="steelblue")
    ax1.set_ylabel("Current (mA)")
    ax1.set_title("Mesh currents")
    ax1.axhline(0, color="black", linewidth=0.8)

    ax2.bar(list(power_mw.keys()), list(power_mw.values()), color="darkorange")
    ax2.set_ylabel("Power (mW)")
    ax2.set_title("Power used by each resistor")

    plt.tight_layout()
    plt.savefig("docs/Task_05_variation_plot.png", dpi=150)
    plt.show()
else:
    print("The matrix is singular, so the circuit cannot be solved this way.")