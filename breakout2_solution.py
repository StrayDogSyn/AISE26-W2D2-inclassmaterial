"""
JTC Program: AISE 25
W2D2 Breakout #2: Filtering a data stream with a generator

This module implements a moving average filter using Python generators.
A moving average filter is a signal processing technique used to smooth
time-series data by calculating the average of a sliding window of values.

Generators are memory-efficient because they produce values on-demand rather
than storing entire sequences in memory.

Author: Solution
Date: Oct 7, 2025
"""

import csv
from typing import Iterator, Generator
from collections import deque
from pathlib import Path


# ============================================================================
# Moving Average Generator Implementation
# ============================================================================

def moving_average(stream: Iterator[int], window_size: int) -> Generator[float, None, None]:
    """
    Generator that applies a moving average filter to a data stream.
    
    This implementation uses a sliding window approach with a deque (double-ended queue)
    for efficient O(1) operations when adding and removing elements.
    
    How it works:
    1. Maintain a window (deque) of up to `window_size` elements
    2. For each new value from the stream:
       - Add it to the window
       - If window exceeds window_size, remove the oldest element
       - Calculate and yield the average of current window
    
    Args:
        stream: An iterator that yields numeric values (e.g., stock volumes)
        window_size: The size of the sliding window for averaging
        
    Yields:
        Float values representing the moving average at each position
        
    Example:
        >>> data = [1, 2, 3, 4, 5, 6, 7]
        >>> filtered = moving_average(iter(data), window_size=3)
        >>> list(filtered)
        [1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0]
        
    Note:
        - At the beginning, the window may not be full (window < window_size)
        - The average is calculated using all available values in the window
        - Uses deque for O(1) append and popleft operations
    """
    # Initialize an empty window using deque for efficient operations
    # deque is preferred over list because:
    # - deque.append() is O(1)
    # - deque.popleft() is O(1)
    # - list.pop(0) is O(n)
    window = deque(maxlen=window_size)
    
    # Process each value from the input stream
    for value in stream:
        # Add the new value to the right end of the window
        # If window is at maxlen, this automatically removes the leftmost element
        window.append(value)
        
        # Calculate the average of all values currently in the window
        # At the start, window may have fewer than window_size elements
        # This is intentional - we average whatever we have
        average = sum(window) / len(window)
        
        # Yield the calculated average
        # This makes this function a generator - it produces values lazily
        yield average


# ============================================================================
# Alternative Implementation: Explicit Window Management
# ============================================================================

def moving_average_explicit(stream: Iterator[int], window_size: int) -> Generator[float, None, None]:
    """
    Alternative moving average implementation with explicit window management.
    
    This version doesn't use deque's maxlen feature, instead manually managing
    the window size. This makes the window management logic more explicit.
    
    Args:
        stream: An iterator that yields numeric values
        window_size: The size of the sliding window for averaging
        
    Yields:
        Float values representing the moving average at each position
    """
    # Initialize an empty window (without maxlen)
    window = deque()
    
    for value in stream:
        # Add the new value to the window
        window.append(value)
        
        # If window exceeds the maximum size, remove the oldest element
        if len(window) > window_size:
            window.popleft()
        
        # Calculate and yield the average
        average = sum(window) / len(window)
        yield average


# ============================================================================
# Alternative Implementation: Running Sum Optimization
# ============================================================================

def moving_average_optimized(stream: Iterator[int], window_size: int) -> Generator[float, None, None]:
    """
    Optimized moving average using a running sum to avoid recalculating.
    
    Instead of summing the entire window each time (O(window_size) per iteration),
    we maintain a running sum and just add/subtract values (O(1) per iteration).
    
    This is significantly faster for large window sizes.
    
    Args:
        stream: An iterator that yields numeric values
        window_size: The size of the sliding window for averaging
        
    Yields:
        Float values representing the moving average at each position
    """
    window = deque()
    running_sum = 0  # Keep track of the sum of values in the window
    
    for value in stream:
        # Add new value to window and running sum
        window.append(value)
        running_sum += value
        
        # If window is too large, remove oldest value
        if len(window) > window_size:
            removed_value = window.popleft()
            running_sum -= removed_value
        
        # Calculate average using running sum (O(1) instead of O(n))
        average = running_sum / len(window)
        yield average


# ============================================================================
# CSV Data Processing Functions
# ============================================================================

def get_volume(dictreader: csv.DictReader) -> Generator[int, None, None]:
    """
    Generator that extracts and yields the Volume column from a CSV DictReader.
    
    This is a simple filter generator that:
    1. Takes rows from a CSV file (as dictionaries)
    2. Extracts the 'Volume' field
    3. Converts it to an integer
    4. Yields it to the next stage in the pipeline
    
    Args:
        dictreader: A csv.DictReader object that yields row dictionaries
        
    Yields:
        Integer values representing trading volume
        
    Example:
        >>> with open('data.csv') as f:
        ...     reader = csv.DictReader(f)
        ...     volumes = get_volume(reader)
        ...     for vol in volumes:
        ...         print(vol)
    """
    # Iterate through each row (dictionary) from the CSV
    for row in dictreader:
        # Extract the Volume field and convert to integer
        # The CSV stores it as a string, so we need int() conversion
        yield int(row['Volume'])


def print_comparison(csv_path: str, window_size: int = 5, num_samples: int = 15):
    """
    Print side-by-side comparison of unfiltered vs. filtered volume data.
    
    This function demonstrates the effect of the moving average filter by
    showing both the raw data and smoothed data.
    
    Args:
        csv_path: Path to the CSV file containing stock data
        window_size: Size of the moving average window (default: 5)
        num_samples: Number of samples to display (default: 15)
    """
    print("=" * 80)
    print(f"Comparing Unfiltered vs. Filtered Data (Window Size: {window_size})")
    print("=" * 80)
    print(f"{'Sample':<8} {'Unfiltered Volume':<25} {'Filtered Volume (MA)':<25}")
    print("-" * 80)
    
    # Open the file and create two separate readers
    # We need two passes through the data - one for unfiltered, one for filtered
    with open(csv_path, 'r') as f:
        # First pass: collect unfiltered data
        unfiltered_data = []
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i >= num_samples:
                break
            unfiltered_data.append(int(row['Volume']))
    
    # Second pass: get filtered data
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        volume_stream = get_volume(reader)
        filtered_stream = moving_average_optimized(volume_stream, window_size)
        
        # Print both unfiltered and filtered values side by side
        for i, (unfiltered, filtered) in enumerate(zip(unfiltered_data, filtered_stream)):
            if i >= num_samples:
                break
            print(f"{i+1:<8} {unfiltered:<25,} {filtered:<25,.2f}")
    
    print("=" * 80)


# ============================================================================
# Demonstration Functions
# ============================================================================

def demonstrate_simple_example():
    """
    Demonstrate the moving average filter with a simple example.
    
    Shows step-by-step how the window fills up and slides across the data.
    """
    print("\n" + "=" * 80)
    print("Simple Example: Moving Average with Window Size = 3")
    print("=" * 80)
    print("Input data: [1, 2, 3, 4, 5, 6, 7]")
    print("-" * 80)
    
    data = [1, 2, 3, 4, 5, 6, 7]
    window_size = 3
    
    # Create the moving average generator
    ma_filter = moving_average(iter(data), window_size)
    
    print(f"{'Step':<6} {'Value':<8} {'Window':<20} {'Average':<10}")
    print("-" * 80)
    
    for i, (value, avg) in enumerate(zip(data, ma_filter), 1):
        # Reconstruct what the window looks like at each step (for demonstration)
        if i <= window_size:
            window_str = str(data[:i])
        else:
            window_str = str(data[i-window_size:i])
        
        print(f"{i:<6} {value:<8} {window_str:<20} {avg:<10.2f}")
    
    print("=" * 80)


def demonstrate_stock_data():
    """
    Demonstrate the moving average filter on real stock data.
    """
    # Get the script's directory and construct path to data file
    script_dir = Path(__file__).parent
    csv_path = script_dir / 'data' / 'AAPL.csv'
    
    # Check if the file exists
    if not csv_path.exists():
        print(f"\n⚠️  Error: Could not find {csv_path}")
        print("Please ensure the AAPL.csv file is in the 'data' directory.")
        return
    
    print("\n" + "=" * 80)
    print("Demonstration: Apple (AAPL) Stock Volume - Unfiltered")
    print("=" * 80)
    
    # Show unfiltered data
    with open(csv_path, 'r') as f:
        unfiltered_volume = get_volume(csv.DictReader(f))
        for i, v in enumerate(unfiltered_volume, 1):
            print(f"Sample {i:2d}: {v:>15,} shares")
            if i >= 15:
                break
    
    print("\n" + "=" * 80)
    print("Demonstration: Apple (AAPL) Stock Volume - Filtered (Window=5)")
    print("=" * 80)
    
    # Show filtered data with moving average
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        volume_stream = get_volume(reader)
        filtered_stream = moving_average_optimized(volume_stream, window_size=5)
        
        for i, v in enumerate(filtered_stream, 1):
            print(f"Sample {i:2d}: {v:>15,.2f} shares (average)")
            if i >= 15:
                break
    
    # Show side-by-side comparison
    print("\n")
    print_comparison(csv_path, window_size=5, num_samples=15)
    
    # Show effect of different window sizes
    print("\n" + "=" * 80)
    print("Effect of Different Window Sizes")
    print("=" * 80)
    
    for window_size in [3, 5, 10]:
        print(f"\nWindow Size: {window_size}")
        print("-" * 40)
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            volume_stream = get_volume(reader)
            filtered_stream = moving_average_optimized(volume_stream, window_size)
            
            # Just show first 5 values
            for i, v in enumerate(filtered_stream, 1):
                print(f"  Sample {i}: {v:>12,.2f}")
                if i >= 5:
                    break


# ============================================================================
# Main Function
# ============================================================================

def main():
    """
    Main function to run all demonstrations.
    """
    print("=" * 80)
    print("W2D2 Breakout #2: Moving Average Filter with Generators")
    print("=" * 80)
    
    # Run simple example first
    demonstrate_simple_example()
    
    # Run stock data demonstration
    demonstrate_stock_data()
    
    print("\n" + "=" * 80)
    print("All demonstrations completed successfully!")
    print("=" * 80)


# ============================================================================
# Reflection Questions - Answers
# ============================================================================
"""
REFLECTION QUESTIONS AND ANSWERS:

1. What are some issues with the way your window is implemented? 
   (Think about the beginning of the signal and about performance) 
   What are some alternative approaches?

   Answer:
   
   **Issues:**
   
   a) **Beginning of signal** (Warm-up period):
      - The window starts empty and gradually fills up
      - Early averages are calculated with fewer data points
      - This can cause edge effects at the start of the data
      - First value: average of [value1] = value1
      - Second value: average of [value1, value2] = (value1+value2)/2
      - Not a true N-point average until we have N points
   
   b) **Performance considerations**:
      - Basic implementation: O(window_size) per iteration due to sum()
      - For large windows or long streams, this can be slow
      - Recalculating sum for every data point is redundant
   
   **Alternative approaches:**
   
   a) **Discard warm-up period**:
      ```python
      def moving_average_skip_warmup(stream, window_size):
          window = deque(maxlen=window_size)
          for value in stream:
              window.append(value)
              if len(window) == window_size:  # Only yield when full
                  yield sum(window) / window_size
      ```
      Pros: All outputs are true N-point averages
      Cons: Lose the first N-1 data points
   
   b) **Pad with initial value**:
      ```python
      def moving_average_padded(stream, window_size):
          stream_list = list(stream)
          first_val = stream_list[0]
          padded = [first_val] * (window_size - 1) + stream_list
          # Now apply standard moving average
      ```
      Pros: No edge effect, starts with full window
      Cons: Requires loading all data into memory, artificial padding
   
   c) **Running sum optimization** (implemented in moving_average_optimized):
      ```python
      # Instead of sum(window) each time, maintain running_sum
      running_sum += new_value
      running_sum -= removed_value
      average = running_sum / len(window)
      ```
      Pros: O(1) per iteration instead of O(window_size)
      Cons: Slight risk of floating-point accumulation errors over time
   
   d) **NumPy for large datasets**:
      ```python
      import numpy as np
      def moving_average_numpy(data, window_size):
          return np.convolve(data, np.ones(window_size)/window_size, mode='valid')
      ```
      Pros: Highly optimized C implementation, very fast
      Cons: Not a generator (returns full array), requires NumPy dependency
   
   e) **Exponential moving average (EMA)**:
      ```python
      def exponential_moving_average(stream, alpha=0.3):
          ema = None
          for value in stream:
              if ema is None:
                  ema = value
              else:
                  ema = alpha * value + (1 - alpha) * ema
              yield ema
      ```
      Pros: No window management, gives more weight to recent values
      Cons: Different algorithm (not a true moving average), requires tuning alpha

2. What was the most difficult part of this assignment and why?

   Answer:
   
   The most challenging aspects typically include:
   
   a) **Understanding Generator Syntax**:
      - The `yield` keyword is conceptually different from `return`
      - Generators maintain state between yields
      - Understanding lazy evaluation vs. immediate computation
      
   b) **Managing Stateful Iteration**:
      - Keeping track of the window as data flows through
      - Understanding when to add vs. remove elements
      - Ensuring the window doesn't grow unbounded
   
   c) **Edge Cases**:
      - What to do when window isn't full yet?
      - How to handle empty streams?
      - What if window_size > total data length?
   
   d) **Generator Chaining**:
      - Connecting multiple generators (get_volume -> moving_average)
      - Understanding that nothing executes until you iterate
      - Debugging generators is harder (can't print intermediate states easily)
   
   e) **Performance Considerations**:
      - Realizing that sum(window) is inefficient
      - Learning about deque and why it's better than list
      - Understanding O(1) vs. O(n) operations
   
   **Why These Are Difficult:**
   - Generators are a unique Python concept (not common in other languages)
   - They require thinking about data flow rather than data storage
   - Stateful iteration is harder to reason about than stateless functions
   - The lazy evaluation model can be counterintuitive at first
   
   **Learning Points:**
   - Generators are powerful for memory-efficient data processing
   - They enable building data pipelines (Unix pipe philosophy in Python)
   - Understanding trade-offs between simplicity and performance is key
   - Real-world data processing often requires handling edge cases carefully
"""


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    main()
