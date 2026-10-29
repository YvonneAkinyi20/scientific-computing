import numpy as np


def estimate_speed(t, x):
    v = np.zeros_like(x)
    v[0] = (x[1] - x[0]) / (t[1] - t[0])
    v[1:-1] = (x[2:] - x[:-2]) / (t[2:] - t[:-2])
    v[-1] = (x[-1] - x[-2]) / (t[-1] - t[-2])
    return v


time = np.array([0, 1, 2, 3, 4, 5, 6], dtype=float)
position = np.array([0.0, 4.8, 10.2, 16.1, 22.7, 30.0, 38.0])

# 1. Change the formula (estimate speed at t = 3 s)
print("=== Forward, backward and central difference at t = 3 s ===")
fwd = (position[4] - position[3]) / 1
bwd = (position[3] - position[2]) / 1
cen = (position[4] - position[2]) / 2
print(f"forward : {fwd:.3f} m/s")
print(f"backward: {bwd:.3f} m/s")
print(f"central : {cen:.3f} m/s")

# 2. Change the step size h on a function with a known derivative
print("\n=== Step size h: f(x) = sin(x) at x = 1 (true derivative cos(1)) ===")
true = np.cos(1.0)
print(f"{'h':>8}{'forward':>14}{'fwd error':>14}{'central':>14}{'cen error':>14}")
for h in [1, 1e-1, 1e-2, 1e-3, 1e-6, 1e-10, 1e-14]:
    f = (np.sin(1 + h) - np.sin(1)) / h
    c = (np.sin(1 + h) - np.sin(1 - h)) / (2 * h)
    print(f"{h:>8.0e}{f:>14.8f}{abs(f - true):>14.2e}{c:>14.8f}{abs(c - true):>14.2e}")

# 3. Change one reading (faulty GPS fix at t = 3 s: 16.1 -> 19.1)
print("\n=== One faulty position (16.1 changed to 19.1) ===")
bad = position.copy()
bad[3] = 19.1
print(f"{'t':>3}{'original':>10}{'faulty':>10}{'change':>10}")
for t, a, b in zip(time, estimate_speed(time, position), estimate_speed(time, bad)):
    print(f"{t:>3.0f}{a:>10.3f}{b:>10.3f}{b - a:>10.3f}")

# 4. Change the sampling interval (keep t = 0, 2, 4, 6 only)
print("\n=== Coarser sampling: every 2 s ===")
keep = [0, 2, 4, 6]
coarse = estimate_speed(time[keep], position[keep])
fine = estimate_speed(time, position)
for t, c, f in zip(time[keep], coarse, fine[keep]):
    print(f"t={t:.0f}s  every 2 s: {c:.3f}  every 1 s: {f:.3f}  difference: {c - f:+.3f}")