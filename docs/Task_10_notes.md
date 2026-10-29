# Task 10: Root Finding: Bisection and Fixed-Point Methods

## B. Input values and mathematical operation
**Inputs:**
- Heat-balance function f(T) = T - 25 - 10 exp(-T/20), where f(T) = 0 means heat gain equals heat loss
- Bracket [20, 40] for bisection, with f(20) < 0 and f(40) > 0
- Fixed-point form T = g(T) = 25 + 10 exp(-T/20), starting at T = 30
- Tolerance 1e-10 for both methods

**Operations:**
- Bisection: repeatedly halve the interval and keep the half where f changes sign
- Fixed-point iteration: calculate T(new) = g(T) until the change is below the tolerance
- Compare the two answers and count the fixed-point iterations

**Original results:**
- Bisection equilibrium temperature: <...> C
- Fixed-point equilibrium temperature: <...> C
- Fixed-point iterations: <...>

## C. Changing the inputs
(Program: `code/Task_10_input_variation.py`)

**Table 1: changing the tolerance (bracket [20, 40])**
| Tolerance | Iterations | Predicted | Root | \|f(root)\| | Error |
|-----------|------------|-----------|------|-------------|-------|
| 1e-2 | <...> | <...> | <...> | <...> | <...> |
| 1e-4 | <...> | <...> | <...> | <...> | <...> |
| 1e-6 | <...> | <...> | <...> | <...> | <...> |
| 1e-8 | <...> | <...> | <...> | <...> | <...> |
| 1e-10 | <...> | <...> | <...> | <...> | <...> |

**Table 2: changing the bracket (tolerance 1e-10)**
| Bracket | f(a) | f(b) | Result |
|---------|------|------|--------|
| [20, 40] | <...> | <...> | <...> |
| [26, 30] | <...> | <...> | <...> |
| [27, 28] | <...> | <...> | <...> |
| [0, 100] | <...> | <...> | <...> |
| [-100, 100] | <...> | <...> | <...> |
| [30, 40] | <...> | <...> | <...> |
| [0, 20] | <...> | <...> | <...> |

**Table 3: changing the model T - Tamb - Q exp(-T/20) (bracket [0, 100])**
| Tamb | Q | Bisection | Iterations | Fixed point | Iterations | Agree |
|------|---|-----------|------------|-------------|------------|-------|
| 25 | 10 | <...> | <...> | <...> | <...> | <...> |
| 15 | 10 | <...> | <...> | <...> | <...> | <...> |
| 35 | 10 | <...> | <...> | <...> | <...> | <...> |
| 25 | 20 | <...> | <...> | <...> | <...> | <...> |
| 25 | 0 | <...> | <...> | <...> | <...> | <...> |

**Table 4: different ways to write f(T) = 0 as T = g(T) (start 30)**
| Form of g(T) | \|slope\| at the root | Result |
|--------------|-----------------------|--------|
| 25 + 10 exp(-T/20) | <...> | <...> |
| -20 ln((T - 25)/10) | <...> | <...> |
| T - 0.5 f(T) | <...> | <...> |
| T - 2.0 f(T) | <...> | <...> |

**Table 5: changing the starting value for g(T) = 25 + 10 exp(-T/20)**
| Start | Result | Iterations |
|-------|--------|------------|
| -50 | <...> | <...> |
| 0 | <...> | <...> |
| 30 | <...> | <...> |
| 100 | <...> | <...> |
| 1000 | <...> | <...> |

**Observations (write what you saw):**
- Each extra decimal place of accuracy cost about <...> more iterations, and the number of iterations matched the predicted value in every row: <True/False>. A tolerance of 1e-10 needed <...> iterations, because each step halves the interval.
- The error was always smaller than the tolerance, and |f(root)| fell from <...> to <...>.
- The brackets [26, 30], [27, 28], [0, 100] and [-100, 100] all gave the same root of <...>, but needed <...>, <...>, <...> and <...> iterations. A narrower bracket needs fewer iterations, and a wider bracket still works.
- The brackets [30, 40] and [0, 20] could not start, because f(a) and f(b) have the <same> sign, so there is no guarantee of a root inside.
- Changing Tamb to 15 and 35 moved the root to <...> and <...>. With Q = 0 the root was exactly <...>, because the exponential term disappears. Bisection and fixed point agreed in every row: <True/False>.
- The form 25 + 10 exp(-T/20) had a slope of <...> and converged in <...> iterations. The form -20 ln((T - 25)/10) had a slope of <...>, which is above 1, so it <did not converge>. The form T - 2.0 f(T) had a slope of <...> and <did not converge>, while T - 0.5 f(T) had a slope of <...> and converged in <...> iterations.
- Every starting value between -50 and 1000 reached <...>, using between <...> and <...> iterations.

## D. Meaning of the output
- The root of f(T) is the equilibrium temperature, where the heat gained equals the heat lost. Both methods give <...> C, and f at this value is about <...>, which is as close to zero as the computer can show.
- Bisection always works when f is continuous and f(a) and f(b) have opposite signs. It is slow but safe. It gains one binary digit of accuracy per iteration, so the number of iterations needed is about log2((b - a) / tolerance).
- Fixed-point iteration is not guaranteed to work. It converges when the slope of g at the root is smaller than 1 in size (|g'(root)| < 1), and the smaller the slope, the faster it converges. Here the slope is about <...>, so each iteration cuts the error by about <...> times.
- The same equation can be written as T = g(T) in several ways, and only some of them converge. A form with a slope above 1 pushes the iteration away from the root, so choosing the form of g is important.
- Fixed-point iteration needed <...> iterations for 1e-10, compared with <...> for bisection, so it is faster here because its slope is small. Bisection needs a bracket but no slope condition, and fixed point needs a good form of g but no bracket.
- The result does not depend on the starting value when the method converges, as Table 5 shows.

## E. Related real-world case: the true interest rate of a loan
**Problem:** A shop offers a loan of KES 500,000 repaid with 24 monthly payments of KES 25,000. This sounds like a flat 10% a year, but the real interest rate is higher, because the balance falls every month. Find the monthly interest rate r from the equation payment x (1 - (1 + r)^-24) / r = 500,000.

**Assumptions:** payments are made at the end of each month; the rate is the same every month; the interest is charged on the remaining balance; the bracket for the rate is 0.0001 to 0.2 (0.01% to 20% a month).

**Input data:** loan amount, number of payments and monthly payment (`code/Task_10_variation.py`). The fixed-point form is r = (payment / loan) x (1 - (1 + r)^-24), starting at r = 0.05.

**Output:**
- f(0.0001) = <...>, f(0.2) = <...> (sign change confirmed: <True/False>)

| Method | Monthly rate | Iterations | \|f(r)\| | Error |
|--------|--------------|------------|----------|-------|
| Bisection | <...> | <...> | <...> | <...> |
| Fixed point | <...> | <...> | <...> | <...> |

- Monthly interest rate: <...>%
- Nominal annual rate (12 x monthly): <...>%
- Effective annual rate: <...>%
- Total paid: KES <...>; total interest: KES <...>
- Quoted flat rate: <...>% a year
- Loan balance after 24 payments: KES <...>

| Payment (KES) | Monthly rate % | Nominal annual % | Effective annual % | Interest (KES) |
|---------------|----------------|------------------|--------------------|----------------|
| 22,000 | <...> | <...> | <...> | <...> |
| 25,000 | <...> | <...> | <...> | <...> |
| 30,000 | <...> | <...> | <...> | <...> |
| 35,000 | <...> | <...> | <...> | <...> |

**Interpretation:** The monthly rate is about <...>%, which is an effective annual rate of <...>%, much higher than the flat rate of <...>% the shop quotes. The flat rate looks low because it charges interest on the full KES 500,000 for the whole two years, while in reality the balance falls with every payment. The loan balance after 24 payments is <...>, which confirms the rate is correct. Bisection needed <...> iterations, while fixed-point needed <...>, because the slope of g at the root is close to <...>, so the fixed-point method converges slowly here, as the right chart in `docs/Task_10_variation_plot.png` shows. The left chart shows f(r) crossing zero at the root. A higher monthly payment gives a higher rate and more interest paid, so the borrower can compare offers by their real rate and not by their flat rate. Root finding is used in the same way for break-even points, calibration and any equation without a direct formula.