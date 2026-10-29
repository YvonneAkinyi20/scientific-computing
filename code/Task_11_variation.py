import math

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq

# Circuit settings
Vs = 5.0        # supply voltage (V)
R = 1000.0      # series resistor (ohm)
Is = 1e-12      # diode saturation current (A)
Vt = 0.02585    # thermal voltage (V)


def make_circuit(supply, resistor):
    """f(V) = diode current - resistor current. f(V) = 0 gives the diode voltage."""
    def f(V):
        return Is * (math.exp(V / Vt) - 1) - (supply - V) / resistor

    def df(V):
        return Is / Vt * math.exp(V / Vt) + 1 / resistor

    return f, df


def newton(f, df, x0, tol=1e-12, max_iter=500):
    x = x0
    hist = [x]
    try:
        for i in range(1, max_iter + 1):
            x_new = x - f(x) / df(x)
            hist.append(x_new)
            if abs(x_new - x) < tol:
                return x_new, i, True, hist
            x = x_new
    except (OverflowError, ZeroDivisionError):
        return x, len(hist), False, hist
    return x, max_iter, False, hist


def secant(f, x0, x1, tol=1e-12, max_iter=500):
    hist = [x0, x1]
    try:
        for i in range(1, max_iter + 1):
            f0, f1 = f(x0), f(x1)
            if f1 == f0:
                return x1, i, False, hist
            x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
            hist.append(x2)
            if abs(x2 - x1) < tol:
                return x2, i, True, hist
            x0, x1 = x1, x2
    except (OverflowError, ZeroDivisionError):
        return x1, len(hist), False, hist
    return x1, max_iter, False, hist


def bisection(f, a, b, tol=1e-12, max_iter=200):
    fa = f(a)
    mids = []
    for i in range(1, max_iter + 1):
        c = (a + b) / 2
        mids.append(c)
        fc = f(c)
        if fc == 0 or (b - a) / 2 < tol:
            return c, i, True, mids
        if fa * fc < 0:
            b = c
        else:
            a, fa = c, fc
    return c, max_iter, False, mids


f, df = make_circuit(Vs, R)
V_ref = brentq(f, 0.0, Vs, xtol=1e-15)

runs = {
    "Newton, start 0.7 V": newton(f, df, 0.7),
    "Newton, start 1.0 V": newton(f, df, 1.0),
    "Newton, start 5.0 V": newton(f, df, 5.0),
    "Secant, 0.5 and 0.7 V": secant(f, 0.5, 0.7),
    "Bisection, [0, 5] V": bisection(f, 0.0, Vs),
}


def evaluations(name, it):
    if name.startswith("Newton"):
        return 2 * it
    if name.startswith("Secant"):
        return it + 1
    return it + 2


print(f"Supply {Vs} V, resistor {R:.0f} ohm, Is = {Is}, Vt = {Vt} V")
print(f"Reference diode voltage (Brent's method): {V_ref:.10f} V\n")
print(f"{'Method':<24}{'Voltage (V)':>14}{'Iterations':>12}{'Evaluations':>13}{'|f(V)|':>12}{'Error (V)':>12}{'Converged':>11}")
for name, (value, it, ok, hist) in runs.items():
    print(f"{name:<24}{value:>14.10f}{it:>12}{evaluations(name, it):>13}"
          f"{abs(f(value)):>12.2e}{abs(value - V_ref):>12.2e}{str(ok):>11}")

# Operating point and circuit checks
V = runs["Newton, start 0.7 V"][0]
I = (Vs - V) / R
print(f"\nDiode voltage: {V:.4f} V")
print(f"Circuit current: {I * 1000:.4f} mA")
print(f"Voltage across the resistor: {I * R:.4f} V")
print(f"Supply - resistor drop - diode voltage: {Vs - I * R - V:.2e} V (should be 0)")
print(f"Diode equation current: {Is * (math.exp(V / Vt) - 1) * 1000:.4f} mA")
print(f"Power in the diode: {V * I * 1000:.3f} mW, power in the resistor: {I * I * R * 1000:.3f} mW")

# Different supplies and resistors (Newton from 0.7 V)
print(f"\n{'Supply (V)':<12}{'R (ohm)':<10}{'Diode V':>10}{'Current (mA)':>14}{'Iterations':>12}{'Matches Brent':>15}")
for supply, res in [(3, 1000), (5, 1000), (9, 1000), (12, 2200), (5, 100), (5, 10000)]:
    f2, df2 = make_circuit(supply, res)
    v2, it2, ok2, _ = newton(f2, df2, 0.7)
    ref2 = brentq(f2, 0.0, supply, xtol=1e-15)
    print(f"{supply:<12}{res:<10}{v2:>10.4f}{(supply - v2) / res * 1000:>14.4f}"
          f"{it2:>12}{str(abs(v2 - ref2) < 1e-9):>15}")

# Chart
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.8))

volts = np.linspace(0.0, 0.8, 400)
diode_ma = Is * (np.exp(volts / Vt) - 1) * 1000
load_ma = (Vs - volts) / R * 1000
ax1.plot(volts, diode_ma, color="steelblue", label="Diode current")
ax1.plot(volts, load_ma, color="darkorange", label="Resistor current (load line)")
ax1.plot(V, I * 1000, "o", color="firebrick", label=f"Solution: {V:.3f} V, {I * 1000:.2f} mA")
ax1.set_ylim(0, 6)
ax1.set_xlabel("Diode voltage (V)")
ax1.set_ylabel("Current (mA)")
ax1.set_title("Where the two currents balance")
ax1.legend()
ax1.grid(True)

for name, (value, it, ok, hist) in runs.items():
    err = np.maximum(np.abs(np.array(hist) - V_ref), 1e-16)
    ax2.semilogy(err, label=name)
ax2.set_xlabel("Iteration")
ax2.set_ylabel("Error in the voltage (V)")
ax2.set_title("Convergence of the methods")
ax2.legend(fontsize=8)
ax2.grid(True)

plt.tight_layout()
plt.savefig("docs/Task_11_variation_plot.png", dpi=150)
plt.show()