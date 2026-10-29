# Task 6: Solution of Systems of Linear Equations

## B. Input values and mathematical operation
**Inputs:**
- Type A servers use 4 CPU units and 8 GB of memory each
- Type B servers use 2 CPU units and 12 GB of memory each
- Total observed usage: 20 CPU units and 72 GB of memory

**Operations:**
- Write the problem as two equations: 4x + 2y = 20 and 8x + 12y = 72
- Store the coefficients in matrix A and the totals in vector b
- Solve A x = b with `np.linalg.solve`
- Verify the answer with A @ solution and calculate the residual b - A @ solution

**Original results:**
- Type A servers: <...>
- Type B servers: <...>
- Verification A @ solution: <...>
- Residual: <...>; residual norm: <...>

## C. Changing the inputs
(Program: `code/Task_06_input_variation.py`)

**Table 1: changing the observed totals (same server types)**
| CPU | Memory | Type A | Type B | Residual norm |
|-----|--------|--------|--------|---------------|
| 20 | 72 | <...> | <...> | <...> |
| 40 | 144 | <...> | <...> | <...> |
| 10 | 36 | <...> | <...> | <...> |
| 24 | 80 | <...> | <...> | <...> |
| 6 | 100 | <...> | <...> | <...> |

**Table 2: changing the resources used by each server (totals fixed at 20 CPU and 72 GB)**
| Matrix A | Determinant | Result |
|----------|-------------|--------|
| [[4,2],[8,12]] | <...> | <...> |
| [[2,1],[4,6]] | <...> | <...> |
| [[5,3],[7,9]] | <...> | <...> |
| [[4,2],[8,4]] (dependent) | <...> | <...> |

**Table 3: sensitivity to a small error in b (nearly singular matrices)**
| eps | Condition number | x before | x after |
|-----|------------------|----------|---------|
| 1 | <...> | <...> | <...> |
| 1e-2 | <...> | <...> | <...> |
| 1e-4 | <...> | <...> | <...> |
| 1e-8 | <...> | <...> | <...> |

**Observations (write what you saw):**
- Doubling both totals (40 CPU, 144 GB) gave <...> Type A and <...> Type B servers, so the answer <doubled / did not change>, because the system is linear.
- The totals (24, 80) gave <...> and <...>, which are not whole numbers, so they cannot be real server counts.
- The totals (6, 100) gave a negative value of <...>, which is mathematically correct but impossible in practice.
- The matrix [[4,2],[8,4]] has determinant <...>, so `np.linalg.solve` reported <...>. Its second row is exactly twice the first, so the two equations carry the same information.
- As eps shrank from 1 to 1e-8, the condition number grew from <...> to <...>, and the same tiny change of 0.001 in b changed x from <...> to <...>.

## D. Meaning of the output
- The solution is the pair of values that satisfies both equations at the same time. Here it means <...> Type A servers and <...> Type B servers use exactly 20 CPU units and 72 GB of memory.
- The residual is b - A @ solution. A residual norm close to 0 (about <...>) shows the answer reproduces the observed totals. It may be tiny but not exactly 0 because of round-off error.
- A unique solution exists only when the determinant is not zero. A zero determinant means the equations are dependent, so there is no unique answer.
- A large condition number means the system is ill-conditioned: small measurement errors in b produce large changes in the solution. So a solution can be correct for the given numbers and still be unreliable when the data are noisy.
- A mathematical solution must also make sense in the real problem. Server counts must be non-negative whole numbers.
- `np.linalg.solve` is preferred over calculating the inverse, because it is faster and more accurate.

## E. Related real-world case: mixing three fertilizers
**Problem:** A crop needs 30 kg of nitrogen (N), 25 kg of phosphorus (P) and 30 kg of potassium (K) per hectare. Three fertilizers (F1, F2, F3) contain different fractions of N, P and K. Find how many kilograms of each fertilizer give exactly the required nutrients, and what it costs.

**Assumptions:** the nutrient fractions are as given in the matrix (for example F1 is 20% N, 10% P, 10% K); the prices are KES 90, 110 and 80 per kg; the nutrients add linearly; no other source of nutrients.

**Input data:** the 3 x 3 nutrient matrix A and the requirement vector b (`code/Task_06_variation.py`), solved as A x = b.

**Output:**
- Determinant: <...>; condition number: <...>
- F1: <...> kg; F2: <...> kg; F3: <...> kg
- All amounts positive (practical): <True/False>
- Supplied nutrients (A @ x): <...>; residual norm: <...>
- Total fertilizer: <...> kg; total cost: KES <...>

| Change in requirements | F1 | F2 | F3 |
|------------------------|----|----|----|
| Original (kg) | <...> | <...> | <...> |
| After a 1% increase (kg) | <...> | <...> | <...> |
| Change (%) | <...> | <...> | <...> |

**Interpretation:** The determinant is not zero, so there is exactly one mix that meets the nutrient requirements. The residual norm of <...> shows the mix supplies the required N, P and K, as the right-hand chart in `docs/Task_06_variation_plot.png` shows, where the required and supplied bars match. All three amounts are positive, so the answer is practical. A 1% rise in requirements raised every amount by <...>%, which shows the system is well-conditioned (condition number <...>) and the recommendation is stable when the soil test changes slightly. The same method works for any number of nutrients and fertilizers as long as the matrix is square and non-singular.