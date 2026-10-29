import numpy as np
from scipy.optimize import brentq

cash_flows = [-10000, 3000, 3500, 4000, 2500]


def make_npv(cf):
    def npv(rate):
        return sum(c / (1 + rate) ** t for t, c in enumerate(cf))

    def d_npv(rate):
        return sum(-t * c / (1 + rate) ** (t + 1) for t, c in enumerate(cf) if t > 0)

    return npv, d_npv


def valid_rate(r):
    return np.isfinite(r) and r > -1


def newton(f, df, x0, tol=1e-12, max_iter=100, valid=lambda x: True):
    """Returns (value, iterations, converged, history)."""
    x = x0
    hist = [x]
    try:
        for i in range(1, max_iter + 1):
            d = df(x)
            if d == 0:
                return x, i, False, hist
            x_new = x - f(x) / d
            hist.append(x_new)
            if not valid(x_new):
                return x_new, i, False, hist
            if abs(x_new - x) < tol:
                return x_new, i, True, hist
            x = x_new
    except (OverflowError, ZeroDivisionError):
        return x, len(hist), False, hist
    return x, max_iter, False, hist


def secant(f, x0, x1, tol=1e-12, max_iter=100, valid=lambda x: True):
    """Returns (value, iterations, converged, history)."""
    hist = [x0, x1]
    try:
        for i in range(1, max_iter + 1):
            f0, f1 = f(x0), f(x1)
            if f1 == f0:
                return x1, i, False, hist
            x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
            hist.append(x2)
            if not valid(x2):
                return x2, i, False, hist
            if abs(x2 - x1) < tol:
                return x2, i, True, hist
            x0, x1 = x1, x2
    except (OverflowError, ZeroDivisionError):
        return x1, len(hist), False, hist
    return x1, max_iter, False, hist


def bisection(f, a, b, tol=1e-12, max_iter=200):
    """Returns (value, iterations, converged, history of midpoints)."""
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


npv, d_npv = make_npv(cash_flows)
ref = brentq(npv, 0, 0.5, xtol=1e-15)
print(f"Reference IRR (Brent's method): {ref:.8%}\n")

# Table 1: Newton-Raphson on x^2 - 2 (the example in the question)
print("Table 1: Newton-Raphson on f(x) = x^2 - 2, starting at 1.5")
print(f"{'k':<4}{'x':>20}{'Error vs sqrt(2)':>20}")
x = 1.5
print(f"{0:<4}{x:>20.12f}{abs(x - np.sqrt(2)):>20.2e}")
for k in range(1, 6):
    x = x - (x * x - 2) / (2 * x)
    print(f"{k:<4}{x:>20.12f}{abs(x - np.sqrt(2)):>20.2e}")

# Table 2: different starting values for Newton-Raphson
print("\nTable 2: Newton-Raphson on the IRR problem, changing the starting value")
print(f"{'Start':<10}{'IRR':>16}{'Iterations':>12}{'Result':>26}")
for x0 in [0.01, 0.05, 0.10, 0.30, 0.60, 2.0]:
    value, it, ok, hist = newton(npv, d_npv, x0, valid=valid_rate)
    irr = f"{100 * value:.6f}%" if ok else "-"
    result = "converged" if ok else "failed (left valid range)"
    print(f"{x0:<10}{irr:>16}{it:>12}{result:>26}")

# Table 3: different starting pairs for the secant method
print("\nTable 3: Secant method on the IRR problem, changing the starting pair")
print(f"{'Start pair':<14}{'IRR':>16}{'Iterations':>12}{'Result':>26}")
for x0, x1 in [(0.05, 0.20), (0.01, 0.02), (0.10, 0.11), (0.30, 0.60), (0.50, 1.00), (1.0, 2.0)]:
    value, it, ok, hist = secant(npv, x0, x1, valid=valid_rate)
    irr = f"{100 * value:.6f}%" if ok else "-"
    result = "converged" if ok else "failed (left valid range)"
    label = f"{x0}, {x1}"
    print(f"{label:<14}{irr:>16}{it:>12}{result:>26}")

# Table 4: error after each iteration
print("\nTable 4: error after each iteration")
print(f"{'k':<4}{'Newton':>14}{'Secant':>14}{'Bisection':>14}")
_, _, _, hn = newton(npv, d_npv, 0.10, valid=valid_rate)
_, _, _, hs = secant(npv, 0.05, 0.20, valid=valid_rate)
_, _, _, hb = bisection(npv, 0.0, 0.5)
for k in range(1, 9):
    en = f"{abs(hn[k] - ref):.2e}" if k < len(hn) else "-"
    es = f"{abs(hs[k + 1] - ref):.2e}" if k + 1 < len(hs) else "-"
    eb = f"{abs(hb[k - 1] - ref):.2e}" if k - 1 < len(hb) else "-"
    print(f"{k:<4}{en:>14}{es:>14}{eb:>14}")

# Table 5: iterations and function evaluations for different tolerances
print("\nTable 5: cost for different tolerances")
print("(evaluations: Newton = 2 per iteration, Secant = iterations + 1, Bisection = iterations + 2)")
print(f"{'Tolerance':<12}{'Newton it':>11}{'eval':>6}{'Secant it':>11}{'eval':>6}{'Bisect it':>11}{'eval':>6}")
for tol in [1e-4, 1e-8, 1e-12]:
    _, itn, _, _ = newton(npv, d_npv, 0.10, tol, valid=valid_rate)
    _, its, _, _ = secant(npv, 0.05, 0.20, tol, valid=valid_rate)
    _, itb, _, _ = bisection(npv, 0.0, 0.5, tol)
    print(f"{tol:<12.0e}{itn:>11}{2 * itn:>6}{its:>11}{its + 1:>6}{itb:>11}{itb + 2:>6}")

# Table 6: different cash flows
print("\nTable 6: changing the cash flows")
print(f"{'Cash flows':<24}{'Newton IRR':>16}{'Secant IRR':>16}{'Reference':>14}")
sets = {
    "Original": cash_flows,
    "3 x 6000 inflows": [-10000, 6000, 6000, 6000],
    "4 x 2000 inflows": [-10000, 2000, 2000, 2000, 2000],
    "Long project 6 x 1000": [-5000] + [1000] * 6,
    "All inflows positive": [3000, 3500, 4000],
}
for name, cf in sets.items():
    f, df = make_npv(cf)
    vn, itn, okn, _ = newton(f, df, 0.10, valid=valid_rate)
    vs, its, oks, _ = secant(f, 0.05, 0.20, valid=valid_rate)
    try:
        reference = f"{100 * brentq(f, -0.9, 5, xtol=1e-14):.4f}%"
    except ValueError:
        reference = "no root"
    tn = f"{100 * vn:.4f}% ({itn})" if okn else "fails"
    ts = f"{100 * vs:.4f}% ({its})" if oks else "fails"
    print(f"{name:<24}{tn:>16}{ts:>16}{reference:>14}")