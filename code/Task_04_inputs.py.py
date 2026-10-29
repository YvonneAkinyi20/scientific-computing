import numpy as np

# Table 1: different approximations of sqrt(2)
true_value = np.sqrt(2)
print("Table 1: approximating sqrt(2)")
print(f"{'Decimals':<10}{'Approx':>14}{'Absolute error':>18}{'Relative error %':>20}")
for d in range(1, 9):
    approx = round(true_value, d)
    abs_err = abs(true_value - approx)
    rel_err = abs_err / abs(true_value)
    print(f"{d:<10}{approx:>14.8f}{abs_err:>18.10f}{rel_err * 100:>20.10f}")

# Table 2: exact vs tolerance comparison for different sums
print("\nTable 2: comparing sums")
print(f"{'Sum':<14}{'Computed':>24}{'Exact ==':>12}{'isclose':>10}")
pairs = [("0.1 + 0.2", 0.1 + 0.2, 0.3),
         ("0.1 + 0.7", 0.1 + 0.7, 0.8),
         ("1.1 + 2.2", 1.1 + 2.2, 3.3),
         ("0.5 + 0.25", 0.5 + 0.25, 0.75)]
for label, calc, exp in pairs:
    print(f"{label:<14}{calc:>24.17f}{str(calc == exp):>12}{str(np.isclose(calc, exp)):>10}")

# Table 3: unstable vs stable formula for different x
print("\nTable 3: (sqrt(1+x) - 1)/x  vs  1/(sqrt(1+x) + 1)")
print(f"{'x':<10}{'direct':>20}{'stable':>20}{'relative error':>18}")
for x in [1e-2, 1e-4, 1e-8, 1e-10, 1e-12, 1e-14, 1e-16]:
    direct = (np.sqrt(1 + x) - 1) / x
    stable = 1 / (np.sqrt(1 + x) + 1)
    rel = abs(direct - stable) / abs(stable)
    print(f"{x:<10.0e}{direct:>20.12f}{stable:>20.12f}{rel:>18.3e}")