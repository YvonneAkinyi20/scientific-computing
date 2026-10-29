# Task 4: Floating-Point Arithmetic and Numerical Errors

## B. Input values and mathematical operation
**Inputs:**
- The sum 0.1 + 0.2 compared with 0.3
- The true value sqrt(2) and the approximation 1.414
- The values x = 1e-4, 1e-8 and 1e-12 for the formula (sqrt(1 + x) - 1) / x

**Operations:**
- Exact comparison (`==`) versus tolerance-based comparison (`np.isclose`)
- Absolute error = |true value - approximate value|
- Relative error = absolute error / |true value|
- Unstable formula (sqrt(1 + x) - 1) / x compared with the equivalent stable form 1 / (sqrt(1 + x) + 1)

**Original results:**
- 0.1 + 0.2 = <...>; exact comparison: <True/False>; tolerance-based comparison: <True/False>
- Absolute error: <...>; relative error: <...>%
- x = 1e-4: direct = <...>, stable = <...>
- x = 1e-8: direct = <...>, stable = <...>
- x = 1e-12: direct = <...>, stable = <...>

## C. Changing the inputs
(Program: `code/Task_04_input_variation.py`)

**Table 1: approximating sqrt(2) with different numbers of decimals**
| Decimals | Approximation | Absolute error | Relative error (%) |
|----------|---------------|----------------|--------------------|
| 1 | <...> | <...> | <...> |
| 3 | <...> | <...> | <...> |
| 5 | <...> | <...> | <...> |
| 8 | <...> | <...> | <...> |

**Table 2: exact comparison versus np.isclose**
| Sum | Computed value | Exact == | np.isclose |
|-----|----------------|----------|------------|
| 0.1 + 0.2 | <...> | <...> | <...> |
| 0.1 + 0.7 | <...> | <...> | <...> |
| 1.1 + 2.2 | <...> | <...> | <...> |
| 0.5 + 0.25 | <...> | <...> | <...> |

**Table 3: unstable versus stable formula**
| x | Direct | Stable | Relative difference |
|---|--------|--------|---------------------|
| 1e-2 | <...> | <...> | <...> |
| 1e-8 | <...> | <...> | <...> |
| 1e-12 | <...> | <...> | <...> |
| 1e-16 | <...> | <...> | <...> |

**Observations (write what you saw):**
- Each extra decimal made the absolute error about <...> times smaller, so the approximation improved steadily.
- The sums that returned False for exact comparison were <...>, while `np.isclose` returned <True/False> for all of them.
- 0.5 + 0.25 returned <True/False> for exact comparison because 0.5 and 0.25 can be stored exactly in binary.
- The direct formula started to lose accuracy at about x = <...> and gave <...> at x = 1e-16, while the stable formula stayed close to 0.5.

## D. Meaning of the output
- Numbers such as 0.1 and 0.2 cannot be stored exactly in binary, so their sum is a very close approximation and not exactly 0.3. This is round-off error.
- Using 1.414 instead of sqrt(2) is a truncation error. The error is small in absolute terms (about 0.0002) but it is a real, measurable difference.
- Relative error is more useful than absolute error when values have very different sizes, because it shows the error as a fraction of the true value.
- The direct formula subtracts two almost equal numbers when x is tiny, which cancels the correct digits and leaves mostly round-off noise. The stable formula is algebraically identical but avoids the subtraction, so it stays accurate.
- Comparing floating-point numbers should be done with `np.isclose()` or a tolerance, never with `==`.

## E. Related real-world case: mobile-money transaction totals
**Problem:** A mobile-money system adds up 1,000,000 payments of KES 0.10 each. The exact total is KES 100,000.00, but repeated floating-point addition accumulates round-off error. We compare three ways of summing against exact decimal arithmetic.

**Assumptions:** every payment is exactly KES 0.10; the exact total is calculated with Python's `Decimal` type; the three methods are a plain Python loop, `np.sum` and `math.fsum`.

**Input data:** 1,000,000 payments of 0.10 (`code/Task_04_variation.py`).

**Output:**
| Method | Total | Absolute error | Relative error (%) |
|--------|-------|----------------|--------------------|
| Python loop | <...> | <...> | <...> |
| np.sum | <...> | <...> | <...> |
| math.fsum | <...> | <...> | <...> |

Loop total == 100000.0: <True/False>; np.isclose(loop total, 100000.0): <True/False>.

**Interpretation:** The plain loop drifted from the exact total by <...> KES, because each addition adds a tiny round-off error that builds up over a million steps. `np.sum` was more accurate because it adds in pairs, and `math.fsum` was the most accurate because it tracks the lost digits. The error is small here, but in banking, accounting or large simulations it can break exact comparisons, so totals should be checked with a tolerance or calculated with `Decimal`. The chart `docs/Task_04_variation_plot.png` shows the error of each method (left) and how the error of the unstable formula grows as x shrinks (right).