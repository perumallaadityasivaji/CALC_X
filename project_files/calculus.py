"""
calculus.py

Contains the Calculus functionality: basic polynomial differentiation
and integration.

Polynomial coefficients are represented as a list ordered from the
highest degree term to the constant term, e.g. [3, 4, 5] represents
3x^2 + 4x + 5.
"""


def differentiate_polynomial(coefficients):
    """
    Returns the coefficients of the derivative of a polynomial.
    Example: [3, 4, 5] (3x^2 + 4x + 5) -> [6, 4] (6x + 4)
    """
    if not coefficients:
        raise ValueError("Polynomial coefficient list cannot be empty.")

    degree = len(coefficients) - 1

    if degree == 0:
        # Derivative of a constant is 0.
        return [0]

    result = []
    for coeff in coefficients[:-1]:  # the constant term drops out
        result.append(coeff * degree)
        degree -= 1
    return result


def integrate_polynomial(coefficients):
    """
    Returns the coefficients of the basic integral of a polynomial
    (the integration constant C is not included in the numeric list;
    it is added when the polynomial is formatted for display).
    Example: [6, 4] (6x + 4) -> [3, 4] (3x^2 + 4x [+ C])
    """
    if not coefficients:
        raise ValueError("Polynomial coefficient list cannot be empty.")

    degree = len(coefficients) - 1
    result = []
    for coeff in coefficients:
        new_degree = degree + 1
        result.append(coeff / new_degree)
        degree -= 1
    return result


def _format_number(value):
    """Formats a number without an unnecessary trailing '.0'."""
    if float(value).is_integer():
        return str(int(value))
    return str(round(value, 6))


def format_polynomial(coefficients, add_constant=False, starting_degree=None):
    """
    Converts polynomial coefficients into readable mathematical text.
    If add_constant is True, ' + C' is appended (used for integration
    results).

    starting_degree lets the caller specify the exponent of the first
    coefficient explicitly. This matters for integration results: the
    coefficient list stays the same length as the input, but every term
    has shifted up by one degree (integrate_polynomial() does not add an
    extra placeholder term for the constant, since 'C' is handled here).
    If starting_degree is not given, it defaults to len(coefficients) - 1,
    which is correct for ordinary polynomials and derivatives.
    """
    if not coefficients:
        raise ValueError("Polynomial coefficient list cannot be empty.")

    degree = starting_degree if starting_degree is not None else len(coefficients) - 1
    terms = []

    for coeff in coefficients:
        if coeff != 0:
            if degree == 0:
                terms.append(f"{_format_number(coeff)}")
            elif degree == 1:
                terms.append(f"{_format_number(coeff)}x")
            else:
                terms.append(f"{_format_number(coeff)}x^{degree}")
        degree -= 1

    if not terms:
        text = "0"
    else:
        text = " + ".join(terms).replace("+ -", "- ")

    if add_constant:
        text += " + C"

    return text
