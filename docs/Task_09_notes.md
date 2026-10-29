# Task 9: Eigenvalues and Eigenvectors

## B. Input values and mathematical operation
**Inputs:**
- The adjacency matrix of a small undirected network with four nodes A, B, C and D
- Connections: A-B, A-C, B-C, B-D and C-D (a 1 means two nodes are connected, a 0 means they are not)

**Operations:**
- Find all eigenvalues and eigenvectors with `np.linalg.eig`
- Pick the dominant (largest) eigenvalue and its eigenvector
- Take the absolute values of the eigenvector and divide by their sum, so the importance scores add up to 1
- Verify the result by checking that A v = lambda v

**Original results:**
- Dominant eigenvalue: <...>
- Importance of A: <...>; B: <...>; C: <...>; D: <...>
- Verification error: <...>

## C. Changing the inputs
(Program: `code/Task_09_input_variation.py`)

**Table 1: eigenvalues of different matrices**
| Matrix | Eigenvalues | Trace = sum of eigenvalues | Determinant = product | Max residual |
|--------|-------------|----------------------------|-----------------------|--------------|
| Diagonal [[2,0],[0,3]] | <...> | <True/False> | <True/False> | <...> |
| [[4,1],[2,3]] | <...> | <True/False> | <True/False> | <...> |
| Symmetric [[2,1],[1,2]] | <...> | <True/False> | <True/False> | <...> |
| Rotation 90 deg | <...> | <True/False> | <True/False> | <...> |
| Singular [[1,2],[2,4]] | <...> | <True/False> | <True/False> | <...> |

**Table 2: changing the network**
| Network | Dominant eigenvalue | Importance of nodes |
|---------|---------------------|---------------------|
| Original (A,B,C,D) | <...> | <...> |
| Add edge A-D | <...> | <...> |
| Remove edge B-C | <...> | <...> |
| Star (hub + 4 nodes) | <...> | <...> |
| Path of 4 nodes | <...> | <...> |

**Table 3: scaling and shifting the original matrix**
| Matrix | Eigenvalues | Same dominant vector |
|--------|-------------|----------------------|
| A | <...> | <True/False> |
| 2A | <...> | <True/False> |
| A + 3I | <...> | <True/False> |
| -A | <...> | <True/False> |

**Table 4: power iteration (start vector 1, 2, 3, ...; tolerance 1e-10)**
| Network | \|l2\|/\|l1\| | On A | On A + I | Eigenvalue found |
|---------|---------------|------|----------|------------------|
| Original (A,B,C,D) | <...> | <...> | <...> | <...> |
| Add edge A-D | <...> | <...> | <...> | <...> |
| Remove edge B-C | <...> | <...> | <...> | <...> |
| Star (hub + 4 nodes) | <...> | <...> | <...> | <...> |
| Path of 4 nodes | <...> | <...> | <...> | <...> |
| Complete graph K4 | <...> | <...> | <...> | <...> |
| Ring of 5 | <...> | <...> | <...> | <...> |

**Observations (write what you saw):**
- For every matrix the trace equalled the sum of the eigenvalues and the determinant equalled their product: <True/False>. The residuals were about <...>, so A v = lambda v holds.
- The rotation matrix has eigenvalues <...>, which are complex numbers, because a rotation changes the direction of every real vector.
- The singular matrix [[1,2],[2,4]] has an eigenvalue of <...>, which matches its determinant of <...>.
- Adding the edge A-D changed the dominant eigenvalue from <...> to <...>, and the importance of the four nodes became <...>, because every node is now connected to every other node.
- In the star network the hub scored <...>, much higher than each outer node (<...>), because the hub is connected to everyone.
- Multiplying A by 2 doubled the eigenvalues to <...> and left the dominant eigenvector unchanged: <True/False>. Adding 3I shifted every eigenvalue up by <...>, again without changing the eigenvectors.
- The matrix -A reversed the eigenvalues, and its dominant eigenvector was <the same / different>.
- Power iteration converged for <...> but gave "no convergence" for <...>. Those networks are bipartite, so their largest and smallest eigenvalues have the same size and the estimate keeps swapping between two vectors. Using A + I fixed this, and the answer was recovered by subtracting 1.
- The closer the ratio |l2|/|l1| was to 1, the more iterations were needed: <...> iterations for the ring of 5 (ratio <...>) compared with <...> for K4 (ratio <...>).

## D. Meaning of the output
- An eigenvector is a direction that the matrix does not turn. The matrix only stretches it by the eigenvalue. The verification error of about <...> shows A v = lambda v holds to within round-off.
- In the network, the dominant eigenvalue (<...>) measures the overall connectedness. The dominant eigenvector gives each node a score based on how many connections it has and how important its neighbours are, which is different from simply counting connections.
- Nodes B and C scored <...> each, higher than A and D (<...> each), because B and C are connected to three nodes while A and D are connected to two. The symmetry of the network also gives B and C identical scores, and A and D identical scores.
- The eigenvalues of this network are <...>. Their sum is <...>, which equals the trace of the matrix (0), and this is a useful check.
- The matrix with scaling or shifting keeps the same eigenvectors, so the ranking of nodes does not depend on the units used.
- Power iteration repeatedly multiplies a vector by the matrix, and it settles on the dominant eigenvector. It works well for large sparse matrices (such as PageRank) where computing every eigenvalue would be too expensive, but it needs a dominant eigenvalue that is clearly larger in size than the others.
- Eigenvalues of a symmetric matrix are always real, which is why `np.linalg.eigh` can be used for the networks.

## E. Related real-world case: natural frequencies of a three-storey building
**Problem:** A three-storey building has a mass of 200,000 kg on each floor and a stiffness of 50,000,000 N/m for each storey. Find the natural frequencies and mode shapes of the building, and show what happens when it is pushed at a frequency close to one of them.

**Assumptions:** the floors move sideways only; each floor has the same mass and each storey the same stiffness; damping is 2% of critical damping; the force acts on the top floor.

**Input data:** the stiffness matrix K and the mass matrix M (`code/Task_09_variation.py`). The eigenvalues of M^-1 K are the squares of the natural angular frequencies (omega squared).

**Output:**
- `eigh` and `eig` give the same eigenvalues: <True/False>
- Mode shapes are perpendicular (V.T @ V = I): <True/False>
- Largest verification error: <...>

| Mode | w^2 | w (rad/s) | f (Hz) | Period (s) | Amplification |
|------|-----|-----------|--------|------------|---------------|
| 1 | <...> | <...> | <...> | <...> | <...> |
| 2 | <...> | <...> | <...> | <...> | <...> |
| 3 | <...> | <...> | <...> | <...> | <...> |

| Mode | Floor 1 | Floor 2 | Floor 3 |
|------|---------|---------|---------|
| 1 | <...> | <...> | <...> |
| 2 | <...> | <...> | <...> |
| 3 | <...> | <...> | <...> |

**Interpretation:** The building has three natural frequencies of <...> Hz, <...> Hz and <...> Hz, so the slowest swing takes about <...> seconds. In the first mode all floors move in the same direction and the top floor moves the most (floor 1 moves <...> and floor 2 moves <...> compared with 1 for the top floor). In the second mode the floors move partly in opposite directions, and in the third mode the floors alternate direction, as the left chart in `docs/Task_09_variation_plot.png` shows. The right chart shows resonance: when the forcing frequency matches a natural frequency, the response is about <...> times larger than for a static push, and the first mode gives the strongest peak. This is why engineers calculate these eigenvalues, to make sure that the natural frequencies of a structure are away from the frequencies of the forces it will meet, such as wind, machinery or ground shaking. The same eigenvalue method that ranked the nodes of a network here finds the natural frequencies of a structure.