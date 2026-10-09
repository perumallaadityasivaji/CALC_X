"""
algebra.py

Contains the Algebra Solver functionality: linear equations, quadratic
equations, and basic polynomial calculations.
"""

import math


def solve_linear(a, b):
    """
    Solves ax + b = 0 and returns x.
    Raises ValueError if a is zero (no unique solution).
    """
    if a == 0:
        raise ValueError("Coefficient 'a' cannot be zero in a linear equation (no unique solution).")
    return -b / a


def solve_quadratic(a, b, c):
    """
    Calculates the real roots of ax^2 + bx + c = 0.

    Returns:
        (root1, root2) if the discriminant is positive,
        (root,)        if the discriminant is zero (repeated root),
        None            if the discriminant is negative (no real roots).
    Raises ValueError if a is zero.
    """
    if a == 0:
        raise ValueError("Coefficient 'a' cannot be zero in a quadratic equation.")

    discriminant = (b ** 2) - (4 * a * c)

    if discriminant > 0:
        root1 = (-b + math.sqrt(discriminant)) / (2 * a)
        root2 = (-b - math.sqrt(discriminant)) / (2 * a)
        return (root1, root2)
    elif discriminant == 0:
        root = -b / (2 * a)
        return (root,)
    else:
        return None


def evaluate_polynomial(coefficients, x):
    """
    Evaluates a polynomial for a given value of x.
    coefficients is a list ordered from the highest degree term to the
    constant term, e.g. [3, 4, 5] represents 3x^2 + 4x + 5.
    """
    if not coefficients:
        raise ValueError("Polynomial coefficient list cannot be empty.")

    degree = len(coefficients) - 1
    result = 0.0
    for coeff in coefficients:
        result += coeff * (x ** degree)
        degree -= 1
    return result


def polynomial_degree(coefficients):
    """Returns the degree of a polynomial from its coefficient list."""
    if not coefficients:
        raise ValueError("Polynomial coefficient list cannot be empty.")
    return len(coefficients) - 1
