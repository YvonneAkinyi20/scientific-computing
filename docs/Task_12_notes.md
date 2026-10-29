# Task 12: Polynomial and Nonlinear Equation Solving

## B. Input values and mathematical operation
**Inputs:**
- Circle: x² + y² = 4
- Parabola: y = x² - 1
- Two initial guesses: [1.0, 1.0] and [-1.0, 1.0]

**Operation:** The two equations are rewritten as residuals that must both equal zero:
- r1(x, y) = x² + y² - 4
- r2(x, y) = y - (x² - 1)

`scipy.optimize.root` starts at each guess and adjusts (x, y) until both residuals are close to zero. Each converged answer is an intersection point of the circle and the parabola.

**Check by algebra:** substituting x² = y + 1 into the circle gives y² + y - 3 = 0, so y = (-1 ± √13)/2.
- y = 1.3028 gives x² = 2.3028, so x = ±1.5175. These are two real intersections.
- y = -2.3028 would need x² = -1.3028, which has no real solution.

**Original output:**
- Guess [1, 1] gives (1.5175, 1.3028) with residuals near zero (<...>) and Converged: True.
- Guess [-1, 1] gives (-1.5175, 1.3028) with residuals near zero (<...>) and Converged: True.

## C. Changing the inputs

**1. Different initial guesses** (circle r² = 4, parabola y = x² - 1)

| Guess | Result (x, y) | Converged | Max residual |
|-------|---------------|-----------|--------------|
| [1, 1] | <...> | <...> | <...> |
| [-1, 1] | <...> | <...> | <...> |
| [0, 2] | <...> | <...> | <...> |
| [2, -2] | <...> | <...> | <...> |
| [0, -2] | <...> | <...> | <...> |
| [3, 3] | <...> | <...> | <...> |

Observation: guesses near an intersection converge to it, and the sign of x in the guess usually decides which of the two points is found. A guess such as [0, -2] is close to the algebraic root y = -2.3028, which has no real x. The solver may then fail or move to a real point (write what happened: <...>).

**2. Different circles and parabolas** (parabola y = x² - c)

| r² | c | Intersections (expected from algebra) |
|----|---|----------------------------------------|
| 4 | 1 | 2: (±1.5175, 1.3028) |
| 9 | 1 | 2: (±1.8364, 2.3723) |
| 1 | 1 | 3: (-1, 0), (1, 0), (0, -1) |
| 4 | -1 | 2: (±0.8896, 1.7913) |
| 4 | 5 | none (y² + y + 1 = 0 has no real root) |

Program result: <paste the "real intersections found" lines and state whether they match>.

Observation: changing the radius or moving the parabola changes the **number** of intersections, not just their position. A larger circle gave two points further out. The circle of radius 1 touches the parabola at three points, and moving the parabola down by 4 units (c = 5) removes all intersections.

## D. Meaning of the output
- Each answer pair (x, y) is a point lying on both the circle and the parabola at the same time.
- The residuals are around <...>, essentially zero, so both equations are satisfied. This is the verification step: a solver reporting success should always be checked by substituting the answer back.
- The two solutions are mirror images (x and -x) because both curves are symmetric about the y-axis.
- The solver finds only the root nearest to its starting guess, so a nonlinear system needs more than one initial guess to find all solutions. A single guess can miss an intersection or fail.
- Polynomial-type equations can have complex or no real roots. The numerical solver searches only for real values, which is why the algebraic root y = -2.3028 is never reported.

## E. Related real-world case: radar coverage and an aircraft path
**Problem:** A radar at the origin detects objects within R = 6 km (a circle). An aircraft flies along the curved path y = 0.05x² - 4 (km). Find where it enters and leaves radar coverage, and for how long it is detected.

**Assumptions:**
- The radar is at (0, 0) and its range is a perfect circle of radius 6 km.
- The path is the parabola y = 0.05x² - 4, with distances in km.
- The aircraft's horizontal speed is constant at 600 km/h (assumed).
- The path is taken as a 2-D plane, ignoring altitude.

**Input data:** circle x² + y² - 36 = 0, parabola y - (0.05x² - 4) = 0, initial guesses [5, -2] and [-5, -2].

**Algebra check:** x² = 20(y + 4), so y² + 20y + 44 = 0 and y = -10 ± √56 = -2.5167 or -17.48. The second value lies outside the circle, so the only valid y is -2.5167, giving x = ±5.4467.

**Output:**
- Entry and exit points: (-5.4467, -2.5167) and (5.4467, -2.5167) km. Program output: <...>
- Residuals: <...>, Converged: True for both.
- Horizontal distance inside coverage: 10.893 km (program: <...>)
- Time inside coverage at 600 km/h: 1.09 minutes (program: <...>)

**Interpretation:** The aircraft is detected for about 10.9 km of its path, or roughly 65 seconds at 600 km/h. It enters at the left of the circle, dips to its lowest point inside the radar zone, and leaves at the right at the same height, because the path is symmetric. The graph `docs/Task_12_variation_plot.png` shows the parabola crossing the circle at the two red points. The exact times depend on the assumed speed, so the figure would change if the aircraft's speed were different. The same method applies to other intersection problems, such as a ship's course meeting a coastline's range, or two curves in a design that must touch.