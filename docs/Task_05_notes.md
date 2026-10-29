# Task 5: Matrix Algebra and Matrix Operations

## B. Input values and mathematical operation
**Inputs:**
- The four corners of a unit square: (0,0), (1,0), (1,1), (0,1)
- A rotation of 45 degrees
- A scaling of 2.0 in the x direction and 1.5 in the y direction

**Operations:**
- Build the rotation matrix R and the scaling matrix S
- Combine them with matrix multiplication: T = R @ S
- Transform every point at once: transformed points = points @ T.T
- Calculate the determinant of T with `np.linalg.det`

**Original results:**
- Transformation matrix T: <...>
- Corner (1,1) becomes: <...>
- Determinant: <...>

## C. Changing the inputs
(Program: `code/Task_05_input_variation.py`)

**Table 1: changing the rotation angle (scale fixed at 2.0 and 1.5)**
| Angle | Corner (1,1) becomes | Determinant |
|-------|----------------------|-------------|
| 0 | <...> | <...> |
| 30 | <...> | <...> |
| 45 | <...> | <...> |
| 90 | <...> | <...> |
| 180 | <...> | <...> |

**Table 2: changing the scale factors (rotation fixed at 45 degrees)**
| sx | sy | Determinant | New area |
|----|----|-------------|----------|
| 1 | 1 | <...> | <...> |
| 2 | 1.5 | <...> | <...> |
| 3 | 3 | <...> | <...> |
| 0.5 | 0.5 | <...> | <...> |
| 2 | 0 | <...> | <...> |

**Table 3: order of multiplication**
- rotation @ scale gives: <...>
- scale @ rotation gives: <...>
- Are they equal? <True/False>

**Table 4: determinant and inverse**
| Matrix | Determinant | Invertible? | M @ inverse = identity? |
|--------|-------------|-------------|--------------------------|
| A = [[1,2],[3,4]] | <...> | <Yes/No> | <True/False/not applicable> |
| B = [[2,4],[1,2]] | <...> | <Yes/No> | <True/False/not applicable> |
| Combined transformation | <...> | <Yes/No> | <True/False/not applicable> |

**Observations (write what you saw):**
- Changing the angle moved the corner (1,1) to <...> at 90 degrees, but the determinant stayed at <...> because rotation does not change size.
- The determinant equals sx x sy, so with scale (2, 1.5) it was <...> and the area of the square became <...>.
- With sy = 0 the determinant was <...> and the new area was <...>, which means the square collapsed into a line.
- rotation @ scale and scale @ rotation gave <different/the same> results, so the order of multiplication <does/does not> matter.
- Matrix B had determinant <...>, so <it could not be inverted / the inverse was ...>.

## D. Meaning of the output
- Each row of the output is a point of the square after it has been scaled and rotated. One matrix multiplication transforms all four points in the same way.
- The determinant is the factor by which the area changes. A determinant of <...> means the area becomes <...> times the original area.
- A determinant of 0 means the matrix is singular and has no inverse. The transformation squashes the shape and the original points cannot be recovered.
- Matrix multiplication is not commutative, so rotating then scaling is different from scaling then rotating.
- Using `@` with NumPy applies the operation to all the points in compiled code, which is faster and shorter than transforming each point in a loop.

## E. Related real-world case: solving a three-loop electrical circuit
**Problem:** An electrical circuit has three loops with five resistors (R1 = 10, R2 = 20, R3 = 30, R4 = 15, R5 = 25 ohms) and two voltage sources (12 V and 5 V). Find the current in each loop and the power used by each resistor.

**Assumptions:** the resistor values are fixed; the circuit follows Kirchhoff's voltage law for each loop; the second source opposes the direction of current in loop 3.

**Input data:** the 3 x 3 resistance matrix A and the voltage vector V (`code/Task_05_variation.py`), solved as A I = V.

**Output:**
- Determinant of A: <...>
- A @ inverse is the identity: <True/False>
- Currents using the inverse and using `np.linalg.solve` agree: <True/False>
- Mesh currents: I1 = <...> mA, I2 = <...> mA, I3 = <...> mA

| Resistor | Current (mA) | Power (mW) |
|----------|--------------|------------|
| R1 | <...> | <...> |
| R2 | <...> | <...> |
| R3 | <...> | <...> |
| R4 | <...> | <...> |
| R5 | <...> | <...> |

- Power supplied: <...> mW; power used: <...> mW; power balance holds: <True/False>

**Interpretation:** The determinant of <...> is not zero, so the matrix is invertible and the circuit has exactly one solution. The currents found with the inverse and with `np.linalg.solve` are the same, but `solve` is the preferred method because it is faster and more accurate than calculating the inverse. The power supplied by the sources equals the power used by the resistors, which confirms the solution is correct. The chart `docs/Task_05_variation_plot.png` shows the three loop currents (left) and the power used by each resistor (right). Resistor <...> uses the most power because <...>.