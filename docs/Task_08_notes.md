# Task 8: Iterative Methods for Linear Systems

## B. Input values and mathematical operation
**Inputs:**
- A 5 x 5 tridiagonal matrix A (2 on the diagonal, -1 beside it) for five interior grid points
- Boundary vector b = [100, 0, 0, 0, 20]: left boundary 100 C, right boundary 20 C
- Starting guess of all zeros, tolerance 1e-8, at most 500 iterations

**Operations:**
- Jacobi: every new value is calculated from the old values of the other unknowns
- Gauss-Seidel: every new value uses the newest values already calculated in the same sweep
- Error at each iteration = largest change between successive estimates
- Compare both results with the direct solution from `np.linalg.solve`

**Original results:**
- Jacobi temperatures: <...>
- Gauss-Seidel temperatures: <...>
- Direct solution: <...>
- Number of iterations (from the chart): Jacobi <...>, Gauss-Seidel <...>

## C. Changing the inputs
(Program: `code/Task_08_input_variation.py`)

**Table 1: changing the tolerance**
| Tolerance | Jacobi iterations | GS iterations | Jacobi error vs direct | GS error vs direct |
|-----------|-------------------|---------------|------------------------|--------------------|
| 1e-2 | <...> | <...> | <...> | <...> |
| 1e-4 | <...> | <...> | <...> | <...> |
| 1e-6 | <...> | <...> | <...> | <...> |
| 1e-8 | <...> | <...> | <...> | <...> |
| 1e-10 | <...> | <...> | <...> | <...> |

**Table 2: changing the boundary temperatures (tolerance 1e-8)**
| b | Jacobi iterations | GS iterations | Temperatures (Gauss-Seidel) |
|---|-------------------|---------------|------------------------------|
| [100 0 0 0 20] | <...> | <...> | <...> |
| [200 0 0 0 40] | <...> | <...> | <...> |
| [0 0 0 0 0] | <...> | <...> | <...> |
| [50 0 0 0 50] | <...> | <...> | <...> |
| [100 0 0 0 -20] | <...> | <...> | <...> |

**Table 3: changing the number of grid points (tolerance 1e-8)**
| n | Jacobi iterations | GS iterations | Ratio | Jacobi radius | GS radius |
|---|-------------------|---------------|-------|---------------|-----------|
| 5 | <...> | <...> | <...> | <...> | <...> |
| 10 | <...> | <...> | <...> | <...> | <...> |
| 20 | <...> | <...> | <...> | <...> | <...> |
| 40 | <...> | <...> | <...> | <...> | <...> |

**Table 4: changing the matrix (maximum 100 iterations)**
| Matrix | Jacobi radius | GS radius | Jacobi | Gauss-Seidel |
|--------|---------------|-----------|--------|--------------|
| Diagonally dominant 3x3 | <...> | <...> | <...> | <...> |
| Weakly dominant 3x3 | <...> | <...> | <...> | <...> |
| [[1,2],[3,1]] (not dominant) | <...> | <...> | <...> | <...> |
| [[3,1],[1,2]] (rows swapped) | <...> | <...> | <...> | <...> |

**Observations (write what you saw):**
- A stricter tolerance needed more iterations: from <...> iterations at 1e-2 to <...> at 1e-10 for Gauss-Seidel. The error against the direct solution became smaller at the same time.
- Doubling the boundary temperatures to [200 0 0 0 40] doubled every temperature, because the system is linear. The iteration count stayed <...>, since it depends on the matrix and not on the size of b.
- With b = [0 0 0 0 0] the answer was <...> after <...> iteration(s), because the starting guess was already the solution.
- With boundaries 50 and 50 the temperatures were <...>, which is <symmetric / not symmetric>.
- As n grew from 5 to 40, Jacobi needed <...> to <...> iterations, and Gauss-Seidel needed about <...> times fewer than Jacobi (ratio <...>).
- The Gauss-Seidel radius was about the <square / double> of the Jacobi radius, which explains why it needed about half the iterations.
- For [[1,2],[3,1]] the radii were <...> and <...>, both above 1, so both methods <diverged>. After swapping the rows to [[3,1],[1,2]] the radii fell to <...> and <...>, and both methods <converged>.

## D. Meaning of the output
- Both methods start from a guess and improve it at every iteration, until the largest change drops below the tolerance. The temperatures settle to <...>, which match the direct solution to within <...>.
- The temperature falls in a straight line from the hot boundary (100 C) to the cold boundary (20 C), because there is no heat source between the ends.
- Gauss-Seidel converged in about half the iterations of Jacobi because it uses the newest values immediately.
- The spectral radius of the iteration matrix decides convergence. A radius below 1 means the error shrinks at every iteration, and a radius above 1 means the error grows. The closer the radius is to 1, the slower the convergence.
- Diagonal dominance (each diagonal entry larger than the sum of the other entries in its row) is a simple condition that guarantees convergence. Reordering the equations can turn a diverging system into a converging one.
- More grid points mean a radius closer to 1, so the iteration count grows quickly with n. This is why plain Jacobi and Gauss-Seidel are slow on fine grids, and why accelerated methods such as SOR are used.
- A tolerance only limits the change between iterations, so the true error can be somewhat larger than the tolerance.

## E. Related real-world case: steady heat on a metal plate
**Problem:** A metal plate is modelled as a 30 x 30 grid of interior points, giving 900 unknown temperatures. The top edge is held at 100 C, the left edge at 50 C, and the right and bottom edges at 0 C. Find the steady temperature at every point.

**Assumptions:** steady state (no change with time); each interior temperature is the average of its four neighbours; no heat source inside the plate; tolerance 1e-6; Gauss-Seidel starts from a zero grid; SOR uses omega = 2 / (1 + sin(pi / 31)).

**Input data:** a 900 x 900 matrix A with only 4 non-zero entries per row at most, and the edge temperatures (`code/Task_08_variation.py`).

**Output:**
- Unknowns: 900; non-zero coefficients: <...> (<...>% of the matrix)

| Method | Iterations | Time (s) | Error vs direct |
|--------|------------|----------|-----------------|
| Jacobi | <...> | <...> | <...> |
| Gauss-Seidel | <...> | <...> | <...> |
| SOR (omega = <...>) | <...> | <...> | <...> |
| Direct sparse solve | - | <...> | - |

| Point | Temperature (C) |
|-------|-----------------|
| Near top edge | <...> |
| Centre | <...> |
| Near left edge | <...> |
| Near bottom edge | <...> |

**Interpretation:** Only <...>% of the coefficients are non-zero, so the system is sparse, and iterative methods only need the four neighbours of each point instead of the whole matrix. Jacobi needed <...> iterations, Gauss-Seidel <...> and SOR only <...>, so SOR was about <...> times faster than Gauss-Seidel. All three methods agree with the direct solution to within <...>, so they are accurate. The plate is hottest near the top edge (<...> C), and the temperature drops towards the cold bottom and right edges, with <...> C at the centre, as the heat map in `docs/Task_08_variation_plot.png` shows. The left chart shows the error of each method falling at a steady rate, and the steeper the line the faster the method converges. For a plate with millions of points, direct factoring would need far more memory than these iterative methods, which is why iterative methods are used for large simulations.