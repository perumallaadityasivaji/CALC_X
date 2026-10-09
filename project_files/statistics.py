"""
statistics.py

Contains the Statistics functionality: mean, median, mode, minimum,
maximum, range, variance, and standard deviation.

Note: this file is intentionally named statistics.py to match the CALC-X
Design Document. It is a local project file, imported using a relative
(same-folder) import in main.py, so it does not conflict with Python's
built-in 'statistics' standard library module in this project.
"""

import math


def _check_not_empty(data):
    if not data:
        raise ValueError("Statistics data cannot be empty.")


def calculate_mean(data):
    """Returns the arithmetic mean."""
    _check_not_empty(data)
    return sum(data) / len(data)


def calculate_median(data):
    """Returns the median."""
    _check_not_empty(data)
    sorted_data = sorted(data)
    n = len(sorted_data)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_data[mid - 1] + sorted_data[mid]) / 2
    return sorted_data[mid]


def calculate_mode(data):
    """Returns the most frequently occurring value or values, as a list."""
    _check_not_empty(data)
    counts = {}
    for value in data:
        counts[value] = counts.get(value, 0) + 1

    highest_frequency = max(counts.values())
    modes = [value for value, count in counts.items() if count == highest_frequency]
    return modes


def calculate_min(data):
    """Returns the smallest value."""
    _check_not_empty(data)
    return min(data)


def calculate_max(data):
    """Returns the largest value."""
    _check_not_empty(data)
    return max(data)


def calculate_range(data):
    """Returns maximum minus minimum."""
    _check_not_empty(data)
    return calculate_max(data) - calculate_min(data)


def calculate_variance(data):
    """Returns the variance: sum((x - mean)^2) / n."""
    _check_not_empty(data)
    mean = calculate_mean(data)
    squared_differences = [(x - mean) ** 2 for x in data]
    return sum(squared_differences) / len(data)


def calculate_standard_deviation(data):
    """Returns the standard deviation: sqrt(variance)."""
    _check_not_empty(data)
    return math.sqrt(calculate_variance(data))
