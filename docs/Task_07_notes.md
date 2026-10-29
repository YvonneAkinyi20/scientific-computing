# Task 7: Gaussian Elimination and LU Decomposition

## B. Input values and mathematical operation
**Inputs:**
- A fixed 3 x 3 coefficient matrix A with 4 on the diagonal for the first two rows, 3 in the last row, and -1 beside the diagonal
- Three measurement vectors: b1 = [15, 10, 10], b2 = [16, 11, 9], b3 = [14, 12, 11]

**Operations:**
- Factor A once with `lu_factor` (A = PLU)
- Reuse the factors for each b with `lu_solve`
- Calculate the residual b - A @ x for each solution
- Compare the first solution with the direct solution from `np.linalg.solve`

**Original results:**
- Measurement set 1: solution <...>; residual norm <...>
- Measurement set 2: solution <...>; residual norm <...>
- Measurement set 3: solution <...>; residual norm <...>
- Direct solution for the first set: <...>

## C. Changing the inputs
(Program: `code/Task_07_input_variation.py`)

**Table 1: changing the measurement vector b (same matrix)**
| b | Solution | Residual norm | Matches solve |
|---|----------|---------------|---------------|
| [15 10 10] | <...> | <...> | <True/False> |
| [30 20 20] | <...> | <...> | <True/False> |
| [0 0 0] | <...> | <...> | <True/False> |
| [1 0 0] | <...> | <...> | <True/False> |
| [-15 10 5] | <...> | <...> | <True/False> |

**Table 2: the factors of A**
- P: <...>
- L: <...>
- U: <...>
- P @ L @ U equals A: <True/False>

**Table 3: Gaussian elimination written by hand**
| b | Elimination result | Same as np.linalg.solve |
|---|--------------------|--------------------------|
| [15 10 10] | <...> | <True/False> |
| [16 11 9] | <...> | <True/False> |
| [14 12 11] | <...> | <True/False> |

**Table 4: changing the matrix**
| Matrix | Determinant | Rank | Condition number | Result |
|--------|-------------|------|------------------|--------|
| Original (diagonal 4,4,3) | <...> | <...> | <...> | <...> |
| Weaker diagonal (2,2,2) | <...> | <...> | <...> | <...> |
| Very weak diagonal | <...> | <...> | <...> | <...> |
| Singular [[1,2,3],[4,5,6],[7,8,9]] | <...> | <...> | <...> | <...> |

**Table 5: LU reuse versus repeated solving (200 vectors)**
| n | Repeated solve (s) | LU once + reuse (s) | Speed-up |
|---|--------------------|---------------------|----------|
| 100 | <...> | <...> | <...>x |
| 500 | <...> | <...> | <...>x |
| 1000 | <...> | <...> | <...>x |

**Observations (write what you saw):**
- Doubling b to [30 20 20] gave a solution that was <...> times larger, because the system is linear. With b = [0 0 0] the solution was <...>.
- Every residual norm was about <...>, so every solution reproduces its b to within round-off error.
- The hand-written Gaussian elimination agreed with `np.linalg.solve` for all three vectors: <True/False>.
- Weakening the diagonal raised the condition number from <...> to <...>, which means the system became <more/less> sensitive to errors.
- The singular matrix had determinant <...> and rank <...>, so there was no unique solution.
- The speed-up from reusing the LU factors was <...>x at n = 100, <...>x at n = 500 and <...>x at n = 1000.

## D. Meaning of the output
- Gaussian elimination turns A x = b into an upper-triangular system, and back-substitution then finds the unknowns from the last equation upward.
- LU decomposition stores the elimination steps in L and U (with P recording any row swaps), so A = P L U. The expensive factoring is done once, and each new b needs only two cheap triangular solves.
- The solutions for the three measurement sets are <...>, and the residual norms of about <...> show they are accurate.
- The matrix with the strong diagonal (4, 4, 3) is easy to solve, and a small condition number (<...>) confirms this. As the diagonal weakens the condition number grows and the solution becomes more sensitive to errors in b.
- A singular matrix has determinant 0 and rank below 3, so LU factoring cannot give a unique solution.
- The more vectors that share the same matrix, the more factoring once pays off, because the factoring cost is not repeated.

## E. Related real-world case: temperature along a heated metal rod
**Problem:** A metal rod of length 1 m is split into 500 points. Both ends are held at 20 degrees C and a heat source warms the rod. Every minute for 300 minutes the heat source changes, so a new b arrives while the coefficient matrix A stays the same. Find the temperature along the rod at each minute.

**Assumptions:** thermal conductivity 50 W/m.K; heat source rising from 10,000 to 40,000 W/m^3 and uniform along the rod; temperature at steady state at each minute; the rod is modelled by a 500 x 500 tridiagonal matrix.

**Input data:** the matrix A and 300 vectors b (`code/Task_07_variation.py`).

**Output:**
- Repeated solve: <...> s
- LU once + reuse: <...> s
- Speed-up: <...>x
- Largest difference between the two methods: <...>
- Largest residual norm: <...>
- Largest error against the exact formula (last step): <...>

| Minute | Heat source (W/m^3) | Hottest point (C) |
|--------|---------------------|-------------------|
| 1 | <...> | <...> |
| 150 | <...> | <...> |
| 300 | <...> | <...> |

**Interpretation:** Reusing the LU factors was <...>x faster than solving from scratch at every minute, and the two methods gave the same temperatures to within <...>. The numerical answer also agrees with the exact formula to within <...>, so the method is accurate. The hottest point sits in the middle of the rod, because the ends are held at 20 degrees C, and it rises from <...> degrees C to <...> degrees C as the heat source grows, as the left chart in `docs/Task_07_variation_plot.png` shows. The right chart shows the time saved by factoring once. The same approach suits any simulation that repeats the same equations with new measurements.