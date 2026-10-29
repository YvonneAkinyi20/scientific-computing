import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq

# Loan settings
P = 500_000.0      # amount borrowed (KES)
n = 24             # number of monthly payments
pmt = 25_000.0     # monthly payment (KES)


def f(r, payment=pmt):
    """Present value of the payments minus the amount borrowed. f(r) = 0 gives the rate."""
    return payment * (1 - (1 + r) ** -n) / r - P


def g(r):
    """Fixed-point form: r = (payment / P) * (1 - (1 + r)^-n)."""
    return pmt / P * (1 - (1 + r) ** -n)


def bisection(func, a, b, tol=1e-12, max_iter=200):
    fa = func(a)
    mids = []
    for _ in range(max_iter):
        c = (a + b) / 2
        mids.append(c)
        fc = func(c)
        if fc == 0 or (b - a) / 2 < tol:
            break
        if fa * fc < 0:
            b = c
        else:
            a, fa = c, fc
    return mids


def fixed_point(gfunc, r0, tol=1e-12, max_iter=2000):
    r = r0
    history = [r]
    for _ in range(max_iter):
        r_new = gfunc(r)
        history.append(r_new)
        if abs(r_new - r) < tol:
            break
        r = r_new
    return history


r_true = brentq(f, 1e-4, 0.2, xtol=1e-15)       # accurate reference value
mids = bisection(f, 1e-4, 0.2)
history = fixed_point(g, 0.05)

print(f"Bracket: f(0.0001) = {f(1e-4):,.0f}, f(0.2) = {f(0.2):,.0f} (sign change)")
print(f"\n{'Method':<14}{'Monthly rate':>16}{'Iterations':>12}{'|f(r)|':>12}{'Error':>12}")
print(f"{'Bisection':<14}{mids[-1]:>16.10f}{len(mids):>12}{abs(f(mids[-1])):>12.2e}{abs(mids[-1] - r_true):>12.2e}")
print(f"{'Fixed point':<14}{history[-1]:>16.10f}{len(history) - 1:>12}{abs(f(history[-1])):>12.2e}{abs(history[-1] - r_true):>12.2e}")

r = mids[-1]
nominal = 12 * r
effective = (1 + r) ** 12 - 1
total_paid = pmt * n
interest = total_paid - P
flat_rate = interest / P / (n / 12)
print(f"\nMonthly interest rate: {100 * r:.4f}%")
print(f"Nominal annual rate (12 x monthly): {100 * nominal:.2f}%")
print(f"Effective annual rate: {100 * effective:.2f}%")
print(f"Total paid: KES {total_paid:,.0f}, total interest: KES {interest:,.0f}")
print(f"Quoted flat rate: {100 * flat_rate:.2f}% a year")

# Check: run the loan month by month with the rate found
balance = P
for _ in range(n):
    balance = balance * (1 + r) - pmt
print(f"Loan balance after {n} payments: KES {balance:.6f}")

# Different monthly payments
print(f"\n{'Payment (KES)':<15}{'Monthly rate %':>16}{'Nominal annual %':>18}{'Effective annual %':>20}{'Interest (KES)':>16}")
for p_ in [22_000, 25_000, 30_000, 35_000]:
    rr = bisection(lambda x: f(x, p_), 1e-4, 0.5)[-1]
    print(f"{p_:<15,}{100 * rr:>16.4f}{1200 * rr:>18.2f}{100 * ((1 + rr) ** 12 - 1):>20.2f}{p_ * n - P:>16,.0f}")

# Chart
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8))

rates = np.linspace(0.002, 0.05, 300)
ax1.plot(100 * rates, f(rates) / 1000, color="steelblue")
ax1.axhline(0, color="black", linewidth=0.8)
ax1.axvline(100 * r_true, color="firebrick", linestyle="--", label=f"Root: {100 * r_true:.3f}%")
ax1.set_xlabel("Monthly interest rate (%)")
ax1.set_ylabel("f(r) (thousand KES)")
ax1.set_title("Loan equation f(r) = 0")
ax1.legend()
ax1.grid(True)

ax2.semilogy(np.maximum(np.abs(np.array(mids) - r_true), 1e-16), label="Bisection")
ax2.semilogy(np.maximum(np.abs(np.array(history) - r_true), 1e-16), label="Fixed point")
ax2.set_xlabel("Iteration")
ax2.set_ylabel("Error in the rate")
ax2.set_title("Convergence of the two methods")
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.savefig("docs/Task_10_variation_plot.png", dpi=150)
plt.show()