JTC Program: AISE 25
Lesson Plan: Python Advanced Features
Type: Breakout Session
W2D2 Breakout #1
Version Date: Oct 7, 2025

## Breakout Session #1:  Simple Decorators

Duration: 30 minutes

Let's practice creating decorators with a simpler example focused on string manipulation. We'll create two decorators: one without arguments and one with arguments.

#### Part A: Decorator with no paramters
Create a decorator called `@shout` that converts the return value of any function to uppercase and adds 3 exclamation marks.

**Requirements:**
- The decorator should take any function that returns a string
- Convert the returned string to uppercase
- Add three exclamation marks at the end
- Use `@functools.wraps` to preserve function metadata

**Example usage:**
```python
@shout
def greet(name):
    return f"hello {name}"

print(greet("alice"))  # Should output: "HELLO ALICE!!!"
```

#### Part B: Decorator with Arguments
Create a decorator called `@style(prefix, suffix)` that adds custom prefix and suffix text to the return value of functions.

**Requirements:**
- The decorator should accept two arguments: `prefix` and `suffix`
- Add the prefix before and suffix after the function's return value
- Use `@functools.wraps` to preserve function metadata

**Example usage:**
```python
@style(">>> ", " <<<")
def say_something(message):
    return message

print(say_something("Python is awesome"))  # Should output: ">>> Python is awesome <<<"
```

**Expected Outcome**: Familiarity with decorator syntax, especially when the decorator should accept parameters.

**Discussion Questions:**
- Why use a decorator when `def`ining and calling a wrapper function achieves the same thing?
- What are some useful applications of decorators you can think of?
- How could a decorator make a function stateful, or able to write to the outer scope (like a logger)?
