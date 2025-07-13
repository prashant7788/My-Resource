"""
Sample math utilities module.

This module provides basic mathematical operations.
"""

import math
from typing import Union


def add_numbers(a: float, b: float) -> float:
    """
    Add two numbers together.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Sum of the two numbers
    """
    return a + b


def multiply_numbers(x: float, y: float) -> float:
    """Multiply two numbers and return the result."""
    return x * y


class Calculator:
    """A simple calculator class for basic operations."""
    
    def __init__(self):
        """Initialize the calculator."""
        self.history = []
    
    def divide(self, dividend: float, divisor: float) -> float:
        """
        Divide two numbers.
        
        Args:
            dividend: Number to be divided
            divisor: Number to divide by
            
        Returns:
            Result of division
            
        Raises:
            ValueError: If divisor is zero
        """
        if divisor == 0:
            raise ValueError("Cannot divide by zero")
        result = dividend / divisor
        self.history.append(f"{dividend} / {divisor} = {result}")
        return result
    
    def get_history(self) -> list:
        """Get calculation history."""
        return self.history.copy()