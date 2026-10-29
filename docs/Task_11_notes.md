# Task 11: Root Finding: Newton-Raphson and Secant Methods

## B. Input values and mathematical operation
**Inputs:**
- Cash flows (initial investment, then four annual inflows): -10,000, 3,000, 3,500, 4,000 and 2,500
- NPV(r) = sum of cash flow / (1 + r)^t, and its derivative d_NPV(r)
- Newton-Raphson starting value r = 0.10
- Secant starting values r = 0.05 and r = 0.20
- Tolerance 1e-12

**Operations:**
- The internal rate of return (IRR) is the rate r where NPV(r) = 0
- Newton-Raphson: r(new) = r - NPV(r) / d_NPV(r), using the tangent line
- Secant method: replaces the derivative with the slope between the two latest points
- Check the answer by calculating NPV at the solution

**Original results:**
- IRR using Newton-Raphson: <...>%
- IRR using the secant method: <...>%
- NPV at the Newton solution: <...>

## C. Changing the inputs
(Program: `code/Task_11_input_variation.py`)

**Table 1: Newton-Raphson on f(x) = x^2 - 2, starting at 1.5**
| k | x | Error vs sqrt(2) |
|---|---|------------------|
| 0 | <...> | <...> |
| 1 | <...> | <...> |
| 2 | <...> | <...> |
| 3 | <...> | <...> |
| 4 | <...> | <...> |
| 5 | <...> | <...> |

**Table 2: Newton-Raphson on the IRR problem, changing the starting value**
| Start | IRR | Iterations | Result |
|-------|-----|------------|--------|
| 0.01 | <...> | <...> | <...> |
| 0.05 | <...> | <...> | <...> |
| 0.10 | <...> | <...> | <...> |
| 0.30 | <...> | <...> | <...> |
| 0.60 | <...> | <...> | <...> |
| 2.0 | <...> | <...> | <...> |

**Table 3: secant method on the IRR problem, changing the starting pair**
| Start pair | IRR | Iterations | Result |
|------------|-----|------------|--------|
| 0.05, 0.2 | <...> | <...> | <...> |
| 0.01, 0.02 | <...> | <...> | <...> |
| 0.1, 0.11 | <...> | <...> | <...> |
| 0.3, 0.6 | <...> | <...> | <...> |
| 0.5, 1.0 | <...> | <...> | <...> |
| 1.0, 2.0 | <...> | <...> | <...> |

**Table 4: error after each iteration**
| k | Newton | Secant | Bisection |
|---|--------|--------|-----------|
| 1 | <...> | <...> | <...> |
| 2 | <...> | <...> | <...> |
| 3 | <...> | <...> | <...> |
| 4 | <...> | <...> | <...> |
| 5 | <...> | <...> | <...> |
| 6 | <...> | <...> | <...> |
| 7 | <...> | <...> | <...> |
| 8 | <...> | <...> | <...> |

**Table 5: cost for different tolerances**
(Evaluations: Newton = 2 per iteration, secant = iterations + 1, bisection = iterations + 2)
| Tolerance | Newton iterations | Newton evaluations | Secant iterations | Secant evaluations | Bisection iterations | Bisection evaluations |
|-----------|-------------------|--------------------|-------------------|--------------------|----------------------|-----------------------|
| 1e-4 | <...> | <...> | <...> | <...> | <...> | <...> |
| 1e-8 | <...> | <...> | <...> | <...> | <...> | <...> |
| 1e-12 | <...> | <...> | <...> | <...> | <...> | <...> |

**Table 6: changing the cash flows**
| Cash flows | Newton IRR (iterations) | Secant IRR (iterations) | Reference |
|------------|-------------------------|-------------------------|-----------|
| Original | <...> | <...> | <...> |
| 3 x 6000 inflows | <...> | <...> | <...> |
| 4 x 2000 inflows | <...> | <...> | <...> |
| Long project 6 x 1000 | <...> | <...> | <...> |
| All inflows positive | <...> | <...> | <...> |

**Observations (write what you saw):**
- For f(x) = x^2 - 2, the first Newton step gave <...> (the question's example gives 1.4167). The number of correct digits roughly <doubled> at each step, and the error fell from <...> to <...> in five steps.
- Starting values 0.01, 0.05, 0.10 and 0.30 all reached <...>%, using <...> to <...> iterations. A start of 0.60 needed <...> iterations, and a start of 2.0 <failed / converged> because the first step left the valid range (a rate below -100% is impossible).
- The secant method converged from <...> of the six starting pairs. The pair <...> failed, because <...>.
- Newton-Raphson and the secant method reached an error of <...> after <...> and <...> iterations, while bisection still had an error of <...> after 8 iterations.
- Tightening the tolerance from 1e-4 to 1e-12 added only <...> iterations for Newton and <...> for secant, but <...> for bisection.
- Bisection halves the error at each step, so it needs about <...> iterations for 1e-12. Newton needed <...> iterations but twice as many evaluations per iteration, giving <...> evaluations, while the secant method needed <...> evaluations.
- For the cash flows 3 x 6000 the IRR was <...>%, and for 4 x 2000 the IRR was <...>%, which is <negative> because the inflows (8,000) are smaller than the investment (10,000).
- For "all inflows positive", the reference was <no root>, because the NPV never reaches zero for any valid rate. Newton and secant gave <fails>.

## D. Meaning of the output
- The IRR is the discount rate at which the investment breaks even: the present value of the inflows equals the investment. Here it is about <...>%, and the NPV at that rate is <...>, which is zero to within round-off.
- Newton-Raphson follows the tangent line to where it crosses zero. When it starts close to a root, the number of correct digits roughly doubles at each iteration (quadratic convergence), which Table 1 and Table 4 show.
- The secant method replaces the derivative with a slope calculated from the last two points. It converges a little more slowly than Newton (about 1.6 times more digits per step) but it needs no derivative and only one new function evaluation per step, so it can cost less in total.
- Bisection is slower but safe, because it only needs a sign change. Newton and secant are fast but not guaranteed: a bad starting value can send them outside the valid range, flatten the slope or jump to a different root.
- A root only exists when the cash flows change sign. With all inflows positive no IRR exists, and the methods cannot find one.
- Choosing the method: use Newton when the derivative is easy to write, the secant method when it is not, and bisection (or a combination such as Brent's method) when safety matters more than speed.

## E. Related real-world case: the voltage across a diode
**Problem:** A 5 V supply drives a diode through a 1 kilo-ohm resistor. The diode current grows exponentially with voltage: I = Is (exp(V / Vt) - 1). In the circuit, the diode current must equal the resistor current (5 - V) / 1000. Find the diode voltage V from f(V) = Is (exp(V / Vt) - 1) - (5 - V) / 1000 = 0.

**Assumptions:** saturation current Is = 1e-12 A; thermal voltage Vt = 0.02585 V; the resistor is 1000 ohm; the diode is ideal apart from the exponential equation; steady state.

**Input data:** the function f(V) and its derivative (`code/Task_11_variation.py`). Newton starts at 0.7 V, 1.0 V and 5.0 V, the secant method at 0.5 V and 0.7 V, and bisection on [0, 5] V.

**Output:**
- Reference diode voltage (Brent's method): <...> V

| Method | Voltage (V) | Iterations | Evaluations | \|f(V)\| | Error (V) | Converged |
|--------|-------------|------------|-------------|----------|-----------|-----------|
| Newton, start 0.7 V | <...> | <...> | <...> | <...> | <...> | <...> |
| Newton, start 1.0 V | <...> | <...> | <...> | <...> | <...> | <...> |
| Newton, start 5.0 V | <...> | <...> | <...> | <...> | <...> | <...> |
| Secant, 0.5 and 0.7 V | <...> | <...> | <...> | <...> | <...> | <...> |
| Bisection, [0, 5] V | <...> | <...> | <...> | <...> | <...> | <...> |

- Diode voltage: <...> V; circuit current: <...> mA; voltage across the resistor: <...> V
- Supply - resistor drop - diode voltage: <...> V (should be 0)
- Diode equation current: <...> mA
- Power in the diode: <...> mW; power in the resistor: <...> mW

| Supply (V) | R (ohm) | Diode V | Current (mA) | Iterations | Matches Brent |
|------------|---------|---------|--------------|------------|---------------|
| 3 | 1000 | <...> | <...> | <...> | <...> |
| 5 | 1000 | <...> | <...> | <...> | <...> |
| 9 | 1000 | <...> | <...> | <...> | <...> |
| 12 | 2200 | <...> | <...> | <...> | <...> |
| 5 | 100 | <...> | <...> | <...> | <...> |
| 5 | 10000 | <...> | <...> | <...> | <...> |

**Interpretation:** The diode voltage is about <...> V and the circuit current is about <...> mA. The balance check of <...> V and the matching diode-equation current confirm that the solution satisfies the circuit laws. Newton-Raphson from 0.7 V (close to the answer) needed only <...> iterations, but from 5.0 V it needed <...> iterations, because the exponential is so steep far from the root that each step only lowers the voltage by about <...> V. The secant method needed <...> iterations from its starting pair, and bisection needed <...> iterations but never failed, as the right chart in `docs/Task_11_variation_plot.png` shows. The left chart shows the diode curve crossing the resistor line at the solution. Changing the supply voltage from 3 V to 12 V changed the diode voltage only from <...> V to <...> V, since the diode voltage is nearly fixed by the exponential, and nearly all the extra voltage appears across the resistor. The current is set mostly by the resistor: <...> mA for 100 ohm and <...> mA for 10,000 ohm at 5 V. The same methods solve any nonlinear equation without a direct formula, from loan rates to circuit voltages.