# Task 2: NumPy Arrays and Numerical Computation

## B. Input values and mathematical operation
**Input:** 24 hourly temperature readings in °C, stored as one NumPy array, ranging from 17.5 to 29.4.

**Operations:**
- Mean = (x1 + x2 + ... + x24) / 24 = 554.9 / 24 = 23.12 °C
- Minimum (17.5 °C) and maximum (29.4 °C)
- Conversion F = 1.8C + 32 applied to the whole array at once, with no loop (vectorization). For example, 18.5 °C becomes 65.3 °F.

## C. Changing an input
**Change 1: the peak reading 29.4 is replaced by 39.4.** The maximum becomes 39.4 °C and the mean rises by 10/24 = 0.42, to 23.54 °C. The minimum stays 17.5 °C. The mean and maximum react to one extreme value, but the minimum does not.

**Change 2: every reading is increased by 5 °C.** The mean becomes 28.12 °C, the minimum 22.5 °C and the maximum 34.4 °C. The range (max - min = 11.9 °C) stays the same, because adding a constant shifts the data without changing its spread.

## D. Meaning of the output
- The average temperature over the day was about 23.1 °C (73.6 °F).
- The coolest reading (17.5 °C) was in the early morning and the warmest (29.4 °C) around midday, the usual daily cycle.
- The Fahrenheit values are the same readings on a different scale.
- A graph of the readings against the hour would rise to a peak near midday and fall in the evening.

## E. Related real-world case: vaccine cold-room monitoring
**Problem:** A health facility keeps vaccines in a cold room that must stay between 2 °C and 8 °C. Find the daily mean, minimum and maximum, convert to °F and K, and find the unsafe hours.

**Assumptions:** one sensor, one reading per hour (24 per day), safe range 2 to 8 °C, hour 0 is midnight.

**Input data:** 24 readings from 3.8 °C to 8.9 °C (see `code/Task_02_variation.py`).

**New operations:** a vectorized comparison marks unsafe hours, and K = C + 273.15 is applied to the whole array.

**Output:** mean 5.70 °C = 42.27 °F = 278.85 K; minimum 3.8 °C at 2:00; maximum 8.9 °C at 12:00; 3 hours out of range (11:00, 12:00 and 13:00).

**Interpretation:** On average the room was safe, but the temperature rose above 8 °C for three hours around midday. Checking only the daily mean would have hidden this, so the maximum and the number of unsafe hours must be monitored too. The graph (`docs/Task_02_variation_plot.png`) shows the curve rising above the green safe band at midday, with the unsafe readings in red.
