# Task 3: Mathematical Functions and Vectorization

## B. Input values and mathematical operation
**Input:** 1,000,000 simulated network latency readings in milliseconds, drawn uniformly between 5 and 250 (random seed 42).

**Operations:**
- Convert milliseconds to seconds: seconds = ms / 1000
- Square each value: seconds²
- Done twice: once with a Python `for` loop, once with one vectorized NumPy expression for all values.
- `timeit` measures each version, and speed-up = loop time / vectorized time.

**Original results:** first five squared values <...>; loop time <...> s; vectorized time <...> s; speed-up <...>x.

## C. Changing the inputs
| Case | n | Range (ms) | Mean squared (s²) | Loop (s) | Vectorized (s) | Speed-up |
|------|---|------------|-------------------|----------|----------------|----------|
| Original | 1,000,000 | 5-250 | <...> | <...> | <...> | <...>x |
| Range doubled | 1,000,000 | 10-500 | <...> | <...> | <...> | <...>x |
| Fewer readings | 1,000 | 5-250 | <...> | <...> | <...> | <...>x |
| More readings | 5,000,000 | 5-250 | <...> | <...> | <...> | <...>x |

**Observations (write what you saw):**
- Doubling the range changed the mean squared value from <...> to <...>, which is <...> times larger.
- With fewer readings the speed-up was <...>x compared with <...>x originally.
- With more readings the loop time became <...> s while the vectorized time became <...> s.

## D. Meaning of the output
- The squared values are small because latencies of 5 to 250 ms are only 0.005 to 0.25 s.
- Both versions give the same results, so vectorization changes the speed, not the answer.
- The vectorized code was about <...> times faster, because the loop processes one value at a time in Python while NumPy applies the operation to the whole array in compiled code.
- The advantage grows with the amount of data, which matters for systems processing millions of readings in real time.

## E. Related real-world case: solar-power monitoring
**Problem:** A solar installation logs voltage and current once per second (1,000,000 readings). Compute power P = V × I for every reading, then the mean and maximum power and the total energy in kWh.

**Assumptions:** voltage 12 to 22 V and current 100 to 5000 mA, uniformly random (simulated); one reading per second; energy (kWh) = sum of watt-seconds / 3,600,000.

**Input data:** two arrays of 1,000,000 values (`code/Task_03_variation.py`).

**Output:** mean power <...> W; maximum power <...> W; energy <...> kWh; loop time <...> s; vectorized time <...> s; speed-up <...>x; sin² + cos² = 1 check: <True/False>.

**Interpretation:** The installation produced about <...> W on average, or <...> kWh over the period. The vectorized calculation gave the same answer much faster than the loop, as the bar chart `docs/Task_03_variation_plot.png` (log scale) shows. The identity check confirms the vectorized trigonometric functions are accurate for all million values.