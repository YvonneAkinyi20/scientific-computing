# Task 14: Curve Fitting and Approximation

## B. Input values and mathematical operation
**Inputs:** seven measurements of server response time at different user loads.

| Concurrent users | 50 | 100 | 150 | 200 | 250 | 300 | 350 |
|------------------|----|-----|-----|-----|-----|-----|-----|
| Response (ms) | 82 | 95 | 115 | 145 | 185 | 238 | 305 |

**Operation:** `scipy.optimize.curve_fit` finds the parameters a, b, c of the quadratic model y = ax² + bx + c that minimise the sum of squared residuals Σ(yᵢ − ŷᵢ)². The program then calculates the RMSE (the typical size of the error) and predicts the response time at 400 users.

**Output:**
- Fitted model: y = 0.002167x² − 0.1345x + 85.00 (program: <...>)
- RMSE: 1.55 ms (program: <...>)
- Predicted response at 400 users: 377.86 ms (program: <...>)

## C. Changing the inputs

**1. Changing the model**

| Model | RMSE (ms) | Prediction at 400 | Prediction at 600 |
|-------|-----------|-------------------|-------------------|
| Linear (y = 0.7321x + 20.0) | 18.83 | 312.9 | 459.3 |
| Quadratic | 1.55 | 377.9 | 784.3 |
| Cubic | <...> | <...> | <...> |
| Exponential | <...> | <...> | <...> |

Observation: the straight line fits poorly (RMSE about 19 ms), because response time rises faster and faster as load grows. The quadratic reduces the error by more than ten times. The extra flexibility of the cubic changes the RMSE only slightly but changes the prediction at 600 (write what you saw: <...>). Models that fit the data equally well can disagree strongly outside the data range.

**2. One faulty measurement (185 ms at 250 users changed to 285 ms)**

| Case | a | b | c | RMSE | Prediction at 400 |
|------|---|---|---|------|-------------------|
| Original | 0.002167 | −0.1345 | 85.00 | 1.55 | 377.9 |
| With outlier | 0.000738 | 0.5083 | 42.14 | 31.17 | 363.6 |

Observation: one bad value changed all three coefficients and increased the RMSE twentyfold. Least squares squares the errors, so a single large error dominates the fit. Faulty readings must be checked before fitting.

**3. Fewer points (only 50, 150, 250 and 350 users)**
- Fitted model: y = 0.002175x² − 0.1310x + 83.76, prediction at 400 users 379.4 ms (original 377.9).
- Errors on the removed points (actual − predicted): 100 users +2.59, 200 users +0.44, 300 users −2.21 ms.

Observation: the quadratic curve is still close to the original with half the data, because the underlying pattern is smooth and the model suits it. The removed points are predicted to within about 2.6 ms.

**4. Changing the prediction load (quadratic model)**

| Users | 250 | 400 | 500 | 800 | 1000 |
|-------|-----|-----|-----|-----|------|
| Predicted (ms) | 186.8 | 377.9 | 559.4 | 1364.0 | 2117.1 |

Observation: 250 users is inside the data and the prediction is reliable (the measured value was 185). From 400 users onward the curve is extrapolating and rises steeply. Nothing was measured beyond 350 users, so these values are an assumption that the same pattern continues.

## D. Meaning of the output
- The fitted curve describes how delay grows with load. The positive x² coefficient (0.0022) means the response time increases faster at higher loads, so each extra user costs more than the previous one. This is typical of a server approaching its capacity.
- An RMSE of 1.55 ms means the model's predictions differ from the measurements by roughly 1.5 ms. The measurements range from 82 to 305 ms, so this is a very close fit. The residuals are about −1.7 to +1.8 ms, with no large errors.
- **Graph:** the fitted curve passes through or very near all seven points and bends upward. Extended to 400 users, it predicts about 378 ms.
- The experiments show that the choice of model matters more than the fit statistic. A line is too simple, the quadratic suits the data, and predictions beyond the measured range depend on the model's assumptions. One faulty value can distort the whole fit.

## E. Related real-world case: growth of a mobile-payment app
**Problem:** A new mobile-payment app recorded its monthly active users (in thousands) for eight months. Choose between a linear and an exponential growth model, measure how well each fits, and forecast months 9 and 12.

**Assumptions:**
- The data are accurate monthly counts.
- Growth continues under the same pattern (no market saturation).
- Two candidate models: linear y = at + b, and exponential y = a·e^(bt).

**Input data:**

| Month | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|-------|---|---|---|---|---|---|---|---|
| Users (thousands) | 12 | 15 | 19 | 24 | 31 | 38 | 48 | 60 |

**Operations:** fit both models with `curve_fit`, compare the RMSE, calculate the growth rate and doubling time, and forecast months 9 and 12.

**Output:**
- Linear: y = 6.726t + 0.61, RMSE = 3.33 (hand calculation: forecast month 9 about 61.1k, month 12 about 81.3k).
- Exponential: y = <...> exp(<...>t), RMSE = <...>. A quick log-linear estimate by hand gives a growth rate of about 26% per month and a doubling time of about 3 months, so month 9 would be about 76k and month 12 about 153k. Use the program values: <...>
- Program forecasts: month 9 linear <...>k, exponential <...>k; month 12 linear <...>k, exponential <...>k.

**Interpretation:** The data are growing faster than a straight line: the monthly increases rise from 3k to 12k. The linear model has systematic residuals (negative in the middle months, positive at the ends), so it is the wrong shape. The exponential model should have a smaller RMSE (<...>) and no pattern in its residuals, as the right-hand plot in `docs/Task_14_variation_plot.png` shows. The two forecasts for month 12 differ by nearly a factor of two (about 81k against about 153k), which shows that choosing the model matters most when forecasting. Exponential growth cannot continue indefinitely, so the exponential forecast is an upper estimate and should be updated as new months are recorded.