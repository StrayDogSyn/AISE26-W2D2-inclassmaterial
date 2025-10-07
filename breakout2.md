JTC Program: AISE 25
Lesson Plan: Python Advanced Features
Type: Breakout Session
W2D2 Breakout #2
Version Date: Oct 7, 2025

## Breakout Session #2: Filtering a data stream with a generator

Duration: 30 minutes

Instructions: Implement a moving averaging filter with a generator and chain it to a csv file reader.

**Steps**:
Ensure the provided code runs in your environment and loads AAPL.csv. You may need to change the filepath argument.
Define a generator moving_average which accepts an argument window_size.
Implement a moving average filter and test its output by printing 15 samples of AAPL trade volume, unfiltered vs. filtered, to the console.

See below for details on the moving average filter:
*A moving average filter is a simple and effective way to smooth data by calculating the average of a fixed number of consecutive data points in a sequence. It is commonly used in signal processing, time-series analysis, and data smoothing.*


**How to:**
- Define a window size (n), which determines how many data points are included in the average.
- Slide the window across the data stream, one data point at a time.
- For each position of the window, calculate the mean of the data points within the window. `yield` the result as the smoothed value for the current position.


Example output for generator-based moving average filter, assuming the data stream is `[1, 2, 3, 4, 5, 6, 7, ...]` and the `window_size = 3`:

1. window contains `[1]` → Moving average: 1.0
2. window contains `[1, 2]` → Moving average: 1.5
3. window contains `[1, 2, 3]` → Moving average: 2.0
4. window contains `[2, 3, 4]` (pop the first element) → Moving average: 3.0
5. window contains `[3, 4, 5]` → Moving average: 4.0


**Expected Outcome:**
- A stateful generator which implements a variable moving averaging filter
- Experience implementing a data science pipeline with generators 

**Reflection Questions:**
- What are some issues with the way your window is implemented? (Think about the beginning of the signal and about performance) What are some alternative approaches?
- What was the most difficult part of this assignment and why?

**Provided Code:**

```python
import csv
   
def moving_average(stream, window_size):
    pass  # your code here!


# Generator which filters out the Volume column from a CSV DictReader
def get_volume(dictreader):
    for row in dictreader:
        yield int(row['Volume'])


with open('files/stocks/AAPL.csv', 'r') as f:  # Adjust to the location of your file
    # reader = csv.DictReader(f)
    unfiltered_volume = get_volume(csv.DictReader(f))
    for i, v in enumerate(unfiltered_volume):
        print(f'{v} shares')
        if i > 15:
            break
```