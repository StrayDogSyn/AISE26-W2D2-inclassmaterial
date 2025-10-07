# 🚀 W2D2 Breakout Solutions - Quick Reference

**Quick commands and key concepts for W2D2 breakout assignments**

---

## ⚡ Quick Start

### Run Solutions

```powershell
# Navigate to directory
cd "c:\Users\EHunt\Repos\AISE\AISE-Curriculum-Weekly\AISE26-W2D2-inclassmaterial"

# Run Breakout 1 (Decorators)
python breakout1_solution.py

# Run Breakout 2 (Generators)
python breakout2_solution.py
```

---

## 📝 Breakout 1: Decorators Cheat Sheet

### Basic Decorator (No Parameters)

```python
import functools

def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Do something before
        result = func(*args, **kwargs)
        # Do something after
        return result
    return wrapper

# Usage
@my_decorator
def my_function():
    pass
```

### Decorator with Parameters

```python
def decorator_with_args(arg1, arg2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Use arg1, arg2
            result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

# Usage
@decorator_with_args("value1", "value2")
def my_function():
    pass
```

### Key Points

- ✅ Always use `@functools.wraps(func)` to preserve metadata
- ✅ Use `*args, **kwargs` for flexibility
- ✅ Remember the three-level nesting for parameterized decorators
- ✅ Decorators are applied bottom-up when stacked

---

## 📝 Breakout 2: Generators Cheat Sheet

### Basic Generator Syntax

```python
def my_generator():
    yield 1
    yield 2
    yield 3

# Usage
for value in my_generator():
    print(value)
```

### Generator with Input Stream

```python
from collections import deque

def moving_average(stream, window_size):
    window = deque(maxlen=window_size)
    for value in stream:
        window.append(value)
        average = sum(window) / len(window)
        yield average

# Usage
data = [1, 2, 3, 4, 5]
filtered = moving_average(iter(data), 3)
for avg in filtered:
    print(avg)
```

### Generator Pipeline

```python
# Chain generators together
csv_reader = csv.DictReader(file)
volume_stream = get_volume(csv_reader)
filtered_stream = moving_average(volume_stream, 5)

# Process the pipeline
for value in filtered_stream:
    print(value)
```

### Generator Key Points

- ✅ Use `yield` instead of `return` to produce values
- ✅ Generators are lazy - values produced on demand
- ✅ Use `deque` for efficient queue operations
- ✅ Chain generators for data pipelines
- ✅ One iteration only (use `itertools.tee()` for multiple)

---

## 🎯 Key Concepts

### Decorators

| Concept | Description |
|---------|-------------|
| **Purpose** | Modify function behavior without changing source |
| **Syntax** | `@decorator` before function definition |
| **Use Cases** | Logging, timing, caching, validation |
| **Best Practice** | Always use `@functools.wraps` |

### Generators

| Concept | Description |
|---------|-------------|
| **Purpose** | Produce values lazily to save memory |
| **Syntax** | Use `yield` instead of `return` |
| **Use Cases** | Large files, streaming data, pipelines |
| **Best Practice** | Use `deque` for efficient windows |

---

## 📊 Performance Comparison

### Moving Average Implementations

| Implementation | Time Complexity | Space Complexity | Notes |
|----------------|-----------------|------------------|-------|
| Basic (with sum()) | O(window_size) per item | O(window_size) | Simple, readable |
| Running sum | O(1) per item | O(window_size) | Best performance |
| NumPy | O(n) total | O(n) | Fastest for arrays |

---

## 💡 Common Patterns

### Decorator Patterns

```python
# Logging decorator
@log_calls
def my_function():
    pass

# Timing decorator
@time_execution
def slow_function():
    pass

# Caching decorator
@cache_result
def expensive_calculation():
    pass

# Multiple decorators
@decorator1
@decorator2
@decorator3
def my_function():
    pass
# Applied order: decorator3 → decorator2 → decorator1
```

### Generator Patterns

```python
# Filter generator
def filter_data(stream, condition):
    for item in stream:
        if condition(item):
            yield item

# Transform generator
def transform_data(stream, func):
    for item in stream:
        yield func(item)

# Aggregate generator
def running_sum(stream):
    total = 0
    for item in stream:
        total += item
        yield total
```

---

## 🔧 Troubleshooting

### Decorator Issues

**Problem**: Lost function metadata
```python
# ❌ Wrong
def decorator(func):
    def wrapper():
        return func()
    return wrapper

# ✅ Correct
import functools
def decorator(func):
    @functools.wraps(func)
    def wrapper():
        return func()
    return wrapper
```

**Problem**: Decorator with arguments not working
```python
# ❌ Wrong (missing outer function)
def decorator(func, arg):
    def wrapper():
        return func()
    return wrapper

# ✅ Correct (three levels)
def decorator(arg):
    def actual_decorator(func):
        @functools.wraps(func)
        def wrapper():
            return func()
        return wrapper
    return actual_decorator
```

### Generator Issues

**Problem**: Generator doesn't produce output
```python
# ❌ Generator is created but not consumed
filtered = moving_average(data, 5)
# Nothing happens!

# ✅ Iterate to get values
for value in moving_average(data, 5):
    print(value)
```

**Problem**: Want to iterate multiple times
```python
# ❌ Generator exhausted after first iteration
gen = moving_average(data, 5)
list(gen)  # Works
list(gen)  # Empty! Generator exhausted

# ✅ Use itertools.tee() for multiple iterations
import itertools
gen1, gen2 = itertools.tee(moving_average(data, 5))
list(gen1)  # Works
list(gen2)  # Also works
```

---

## 📚 Quick Reference Tables

### Decorator Syntax

| Type | Syntax | Example |
|------|--------|---------|
| No parameters | `@decorator` | `@shout` |
| With parameters | `@decorator(args)` | `@style(">>", "<<")` |
| Multiple | `@dec1 @dec2` | `@shout @style("*", "*")` |

### Generator Methods

| Method | Description | Example |
|--------|-------------|---------|
| `next()` | Get next value | `next(gen)` |
| `list()` | Consume all | `list(gen)` |
| `for` loop | Iterate | `for x in gen: ...` |

### Useful Imports

```python
# For decorators
import functools
from typing import Callable, Any

# For generators
from collections import deque
from typing import Iterator, Generator
import itertools

# For both
from pathlib import Path
```

---

## ✅ Testing Checklist

### Breakout 1 Tests

- [ ] `@shout` converts to uppercase
- [ ] `@shout` adds three exclamation marks
- [ ] `@style` adds prefix and suffix
- [ ] Metadata is preserved (`__name__`, `__doc__`)
- [ ] Multiple arguments work
- [ ] Stacked decorators work

### Breakout 2 Tests

- [ ] Moving average calculates correctly
- [ ] Window fills up gradually
- [ ] Window slides correctly
- [ ] Works with CSV data
- [ ] Generator chains work
- [ ] Different window sizes work

---

## 🎓 Learning Outcomes

### What You Should Know

**Decorators:**
- How to create simple decorators
- How to create parameterized decorators
- When and why to use `@functools.wraps`
- Common decorator use cases
- How to stack multiple decorators

**Generators:**
- Difference between generators and lists
- How `yield` works
- Generator pipelines and chaining
- Memory efficiency benefits
- When to use generators vs. lists

---

## 📖 Key Takeaways

### Decorator Summary

✅ Decorators wrap functions to modify behavior  
✅ Use `@functools.wraps` to preserve metadata  
✅ Parameterized decorators need three levels  
✅ Great for cross-cutting concerns  
✅ Enable clean, declarative code

### Generator Summary

✅ Generators produce values lazily with `yield`  
✅ Memory-efficient for large datasets  
✅ Perfect for data pipelines  
✅ Use `deque` for efficient windows  
✅ One-time iteration (unless using `itertools.tee()`)

---

**Need more details?** See `README_SOLUTIONS.md` for comprehensive documentation!
