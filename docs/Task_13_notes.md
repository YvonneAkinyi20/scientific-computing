# Task 13: Interpolation

## B. Input values and mathematical operation
**Inputs:** seven hourly temperature measurements.

| Hour | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|------|---|---|----|----|----|----|----|
| Temp (°C) | 18.0 | 20.0 | 22.5 | 24.0 | 25.0 | 25.5 | 25.0 |

**Operations:**
- `interp1d(kind="linear")` joins neighbouring points with straight lines.
- `CubicSpline` joins them with smooth cubic curves, so the slope and curvature match at every measured point.
- Both functions are evaluated every 10 minutes (1/6 hour, 37 times between 8:00 and 14:00) and at 10:30.

**Check by hand:** the linear estimate at 10:30 is the midpoint of 22.5 and 24.0, which is 23.25 °C.

**Original output:**
- Linear estimate at 10:30: 23.25 °C
- Cubic estimate at 10:30: <...> °C

## C. Changing the inputs

**1. Changing the method (estimate at 10:30)**

| Method | Estimate (°C) |
|--------|---------------|
| nearest | <...> |
| previous | <...> |
| linear | 23.25 |
| quadratic | <...> |
| cubic | <...> |
| CubicSpline | <...> |

Observation: "nearest" and "previous" give step-like values taken from a measured point, linear gives the midpoint, and the smooth methods give a value close to linear but slightly different, because they allow the curve to bend.

**2. A faulty reading: 11:00 changed from 24.0 to 30.0**

| Estimate | Original | With spike |
|----------|----------|------------|
| 10:30 linear | 23.25 | 26.25 |
| 10:30 cubic | <...> | <...> |
| 12:30 linear | 25.25 | 25.25 |
| 12:30 cubic | <...> | <...> |

Observation: a linear estimate depends only on its two neighbouring points, so the 12:30 value is unaffected, while 10:30 rises by 3.0 (half of the 6.0 spike). The cubic spline uses a wider neighbourhood, so its estimates change further from the faulty point as well (write what you saw: <...>). One bad sensor value therefore spreads further with a spline.

**3. Fewer points: keep 8:00, 10:00, 12:00, 14:00 and estimate the removed hours**

| Hour | Actual | Linear | Linear error | Cubic | Cubic error |
|------|--------|--------|--------------|-------|-------------|
| 9 | 20.0 | 20.25 | 0.25 | <...> | <...> |
| 11 | 24.0 | 23.75 | 0.25 | <...> | <...> |
| 13 | 25.5 | 25.00 | 0.50 | <...> | <...> |

Observation: with fewer data points the errors grow. Compare the cubic errors with the linear ones: <...> (write which method was more accurate here and by how much).

**4. Estimating outside the measured range (15:00)**
- `interp1d` raises a `ValueError`, because 15:00 is outside 8:00 to 14:00.
- `CubicSpline` returns <...> °C by extending the curve.

Observation: extrapolation is guessing. The spline returns a number without complaint, but nothing in the data supports it, so it should not be trusted.

## D. Meaning of the output
- Interpolation fills in values **between** known measurements. The estimate at 10:30 (about 23.25 °C) says the temperature was probably between the 10:00 reading (22.5) and the 11:00 reading (24.0).
- The linear estimate is the midpoint. The cubic estimate differs slightly (<...> °C) because the temperature rises quickly in the morning and flattens near the afternoon peak, so the true curve bends, and a straight line ignores that bend.
- **Graph:** the orange cubic curve passes through all seven blue points and is smooth, rising through the morning and levelling off near 13:00 at about 25.5 °C. The blue linear line is made of straight segments with visible corners at each measured hour. The two lines are close together, which shows that for smoothly changing data either method gives similar estimates.
- The experiments show the trade-offs. Linear is simple, never overshoots and isolates faulty values. Cubic gives smoother curves and is usually more accurate for smooth data, but a single bad value affects a wider area. Interpolation should only be used inside the data range.

## E. Related real-world case: soil-moisture sensor calibration
**Problem:** A soil-moisture sensor outputs a raw reading (ADC value), and the farmer needs moisture in percent. Only six calibration points were measured in the lab. Estimate the moisture for any reading, check the accuracy, and find the reading at which moisture drops below the irrigation threshold of 35%.

**Assumptions:**
- The calibration points are accurate and the relationship is smooth and decreasing.
- Calibration was done at one soil temperature and soil type.
- Irrigation is needed when moisture falls below 35%.

**Input data:**

| Reading (ADC) | 250 | 350 | 450 | 550 | 650 | 750 |
|---------------|-----|-----|-----|-----|-----|-----|
| Moisture (%) | 80 | 62 | 45 | 31 | 20 | 12 |

**Operations:** build a linear function and a cubic spline, evaluate them at readings 300, 400, 500, 600 and 700, run a hold-out test (remove the 450 point and estimate it), and search for the reading where the spline drops below 35%.

**Output:**

| Reading | Linear (%) | Cubic (%) |
|---------|-----------|-----------|
| 300 | 71.00 | <...> |
| 400 | 53.50 | <...> |
| 500 | 38.00 | <...> |
| 600 | 25.50 | <...> |
| 700 | 16.00 | <...> |

- Hold-out test at 450 (true value 45.0%): linear 46.50% (error 1.50), cubic <...> (error <...>).
- Moisture falls below 35% at a reading of about <...> (program output). By hand, the linear interpolation puts it near 521.

**Interpretation:** Interpolation turns six lab measurements into a usable conversion for every possible sensor reading. The hold-out test shows how trustworthy it is: the linear method was off by 1.5 percentage points at 450, and the cubic method was off by <...>. Moisture drops quickly at low readings and more slowly at high readings, so the curve is not a straight line, and a smooth method is preferable if its hold-out error is smaller. The graph (`docs/Task_13_variation_plot.png`) shows both curves through the black calibration points and the red irrigation line, with the crossing point at about reading <...>. A farmer would irrigate when the sensor reading goes above that value. The estimates are only valid between readings 250 and 750.