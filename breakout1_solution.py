"""
JTC Program: AISE 25
W2D2 Breakout #1: Simple Decorators

This module demonstrates creating decorators both with and without arguments.
Decorators are a powerful Python feature that allows you to modify or enhance
the behavior of functions without permanently modifying them.

Author: Solution
Date: Oct 7, 2025
"""

import functools
from typing import Callable, Any


# ============================================================================
# Part A: Decorator Without Parameters
# ============================================================================

def shout(func: Callable) -> Callable:
    """
    A decorator that converts a function's return value to uppercase and adds
    three exclamation marks.
    
    This is a simple decorator that doesn't take any arguments. It wraps the
    original function and modifies its return value.
    
    Args:
        func: The function to be decorated (must return a string)
        
    Returns:
        A wrapper function that returns the modified string
        
    Example:
        >>> @shout
        ... def greet(name):
        ...     return f"hello {name}"
        >>> greet("alice")
        'HELLO ALICE!!!'
    """
    # @functools.wraps preserves the original function's metadata
    # (name, docstring, etc.) This is a best practice for decorators
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> str:
        """
        Wrapper function that calls the original function and modifies its result.
        
        Args:
            *args: Positional arguments to pass to the original function
            **kwargs: Keyword arguments to pass to the original function
            
        Returns:
            The uppercase version of the function's return value with "!!!"
        """
        # Call the original function with all its arguments
        result = func(*args, **kwargs)
        
        # Transform the result: convert to uppercase and add exclamation marks
        shouted_result = result.upper() + "!!!"
        
        return shouted_result
    
    # Return the wrapper function (this replaces the original function)
    return wrapper


# ============================================================================
# Part B: Decorator With Arguments
# ============================================================================

def style(prefix: str, suffix: str) -> Callable:
    """
    A decorator factory that creates decorators with custom prefix and suffix.
    
    This is a more advanced decorator that accepts arguments. To do this, we need
    an additional layer of nesting:
    1. Outer function (style) - accepts the decorator arguments
    2. Middle function (decorator) - accepts the function to be decorated
    3. Inner function (wrapper) - accepts the function's arguments and does the work
    
    Args:
        prefix: String to add before the function's return value
        suffix: String to add after the function's return value
        
    Returns:
        A decorator function that can be applied to other functions
        
    Example:
        >>> @style(">>> ", " <<<")
        ... def say_something(message):
        ...     return message
        >>> say_something("Python is awesome")
        '>>> Python is awesome <<<'
    """
    # This is the actual decorator that will be applied to the function
    def decorator(func: Callable) -> Callable:
        """
        The actual decorator that wraps the function.
        
        Args:
            func: The function to be decorated
            
        Returns:
            A wrapper function that adds prefix and suffix
        """
        # Again, preserve the original function's metadata
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> str:
            """
            Wrapper function that adds prefix and suffix to the result.
            
            Args:
                *args: Positional arguments to pass to the original function
                **kwargs: Keyword arguments to pass to the original function
                
            Returns:
                The function's return value with prefix and suffix added
            """
            # Call the original function
            result = func(*args, **kwargs)
            
            # Add the prefix and suffix (captured from outer scope via closure)
            styled_result = f"{prefix}{result}{suffix}"
            
            return styled_result
        
        return wrapper
    
    # Return the decorator (not the wrapper!)
    # This allows the syntax: @style("prefix", "suffix")
    return decorator


# ============================================================================
# Demonstration and Testing
# ============================================================================

def main():
    """
    Main function to demonstrate the decorators with various examples.
    """
    print("=" * 70)
    print("W2D2 Breakout #1: Decorator Demonstrations")
    print("=" * 70)
    
    # ========================================================================
    # Part A: Testing @shout decorator
    # ========================================================================
    print("\n" + "=" * 70)
    print("Part A: @shout Decorator (No Parameters)")
    print("=" * 70)
    
    @shout
    def greet(name: str) -> str:
        """Return a greeting message."""
        return f"hello {name}"
    
    @shout
    def introduce(name: str, role: str) -> str:
        """Return an introduction message."""
        return f"my name is {name} and I am a {role}"
    
    # Test cases for @shout
    print("\nTest 1: Simple greeting")
    print(f"  Input: greet('alice')")
    print(f"  Output: {greet('alice')}")
    
    print("\nTest 2: Longer message")
    print(f"  Input: greet('world')")
    print(f"  Output: {greet('world')}")
    
    print("\nTest 3: Multiple arguments")
    print(f"  Input: introduce('Bob', 'developer')")
    print(f"  Output: {introduce('Bob', 'developer')}")
    
    # Demonstrate that metadata is preserved
    print("\nTest 4: Metadata preservation")
    print(f"  Function name: {greet.__name__}")
    print(f"  Function docstring: {greet.__doc__}")
    
    # ========================================================================
    # Part B: Testing @style decorator
    # ========================================================================
    print("\n" + "=" * 70)
    print("Part B: @style Decorator (With Parameters)")
    print("=" * 70)
    
    @style(">>> ", " <<<")
    def say_something(message: str) -> str:
        """Return the message as-is."""
        return message
    
    @style("🎉 ", " 🎉")
    def celebrate(event: str) -> str:
        """Return a celebration message."""
        return event
    
    @style("[INFO] ", "")
    def log_message(msg: str) -> str:
        """Return a log message."""
        return msg
    
    # Test cases for @style
    print("\nTest 1: Basic prefix and suffix")
    print(f"  Input: say_something('Python is awesome')")
    print(f"  Output: {say_something('Python is awesome')}")
    
    print("\nTest 2: Emoji decorators")
    print(f"  Input: celebrate('New Year')")
    print(f"  Output: {celebrate('New Year')}")
    
    print("\nTest 3: Logging style (suffix empty)")
    print(f"  Input: log_message('System starting...')")
    print(f"  Output: {log_message('System starting...')}")
    
    print("\nTest 4: Chaining multiple style decorators")
    
    @style("*** ", " ***")
    @style("=> ", " <=")
    def important_message(msg: str) -> str:
        """Return an important message with multiple decorations."""
        return msg
    
    print(f"  Input: important_message('URGENT')")
    print(f"  Output: {important_message('URGENT')}")
    print("  (Note: Decorators are applied bottom-up)")
    
    # ========================================================================
    # Bonus: Advanced decorator example
    # ========================================================================
    print("\n" + "=" * 70)
    print("Bonus: Combining Both Decorators")
    print("=" * 70)
    
    @shout
    @style("📢 ", " 📢")
    def announce(message: str) -> str:
        """Announce something with style and volume."""
        return message
    
    print("\nTest: Stacked decorators")
    print(f"  Input: announce('meeting at 3pm')")
    print(f"  Output: {announce('meeting at 3pm')}")
    print("  (Applied: style first, then shout)")
    
    print("\n" + "=" * 70)
    print("All tests completed successfully!")
    print("=" * 70)


# ============================================================================
# Discussion Questions - Answers
# ============================================================================
"""
DISCUSSION QUESTIONS AND ANSWERS:

1. Why use a decorator when defining and calling a wrapper function achieves 
   the same thing?

   Answer:
   - **Cleaner syntax**: Decorators provide a clean, declarative way to modify
     function behavior. Instead of:
     ```
     def my_func():
         pass
     my_func = wrapper(my_func)
     ```
     We can write:
     ```
     @wrapper
     def my_func():
         pass
     ```
   
   - **Reusability**: Decorators can be easily applied to multiple functions
     without duplicating wrapper code.
   
   - **Composability**: Multiple decorators can be stacked to combine behaviors.
   
   - **Readability**: The intent is clear at the function definition, making
     code more self-documenting.
   
   - **Framework integration**: Many frameworks (Flask, Django, pytest) use
     decorators for routing, permissions, fixtures, etc.

2. What are some useful applications of decorators you can think of?

   Answer:
   - **Logging**: Log function calls, arguments, and return values
   - **Timing**: Measure function execution time
   - **Caching/Memoization**: Store results of expensive function calls
   - **Authentication/Authorization**: Check user permissions before execution
   - **Rate limiting**: Limit how often a function can be called
   - **Validation**: Validate function arguments before execution
   - **Retry logic**: Automatically retry failed operations
   - **Deprecation warnings**: Notify when old functions are used
   - **Type checking**: Runtime type validation
   - **Database transactions**: Wrap functions in begin/commit/rollback

3. How could a decorator make a function stateful, or able to write to the 
   outer scope (like a logger)?

   Answer:
   Decorators can maintain state through several mechanisms:
   
   a) **Closure variables**: The decorator can create variables in its scope
      that persist across function calls:
      ```python
      def call_counter(func):
          count = 0  # Persists across calls
          def wrapper(*args, **kwargs):
              nonlocal count
              count += 1
              print(f"Called {count} times")
              return func(*args, **kwargs)
          return wrapper
      ```
   
   b) **Function attributes**: Store state as attributes of the wrapper:
      ```python
      def call_counter(func):
          def wrapper(*args, **kwargs):
              wrapper.count += 1
              print(f"Called {wrapper.count} times")
              return func(*args, **kwargs)
          wrapper.count = 0
          return wrapper
      ```
   
   c) **Class-based decorators**: Use a class with __call__ method:
      ```python
      class CallCounter:
          def __init__(self, func):
              self.func = func
              self.count = 0
          
          def __call__(self, *args, **kwargs):
              self.count += 1
              print(f"Called {self.count} times")
              return self.func(*args, **kwargs)
      ```
   
   These approaches allow decorators to:
   - Count function calls
   - Maintain caches
   - Track execution history
   - Log to external systems
   - Implement rate limiting
   - Store metrics and statistics
"""


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    main()
