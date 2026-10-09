"""
equations.py

Contains the Equation Solver functionality: simultaneous 2-variable and
3-variable systems of linear equations.

Coefficient format:
    2x2 -> [[a1, b1, c1], [a2, b2, c2]]      for a1*x + b1*y = c1, etc.
    3x3 -> [[a1,b1,c1,d1],[a2,b2,c2,d2],[a3,b3,c3,d3]]  for a*x+b*y+c*z=d
"""


def _determinant_2x2(a, b, c, d):
    return (a * d) - (b * c)


def has_unique_solution(coefficients):
    """
    Checks whether the equation system has a unique solution by
    calculating the determinant of the coefficient matrix (constants
    excluded). Works for 2x2 and 3x3 systems.
    """
    size = len(coefficients)

    if size == 2:
        a1, b1, _ = coefficients[0]
        a2, b2, _ = coefficients[1]
        det = _determinant_2x2(a1, b1, a2, b2)
        return det != 0

    if size == 3:
        matrix = [row[:3] for row in coefficients]
        det = (
            matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
            - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
            + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
        )
        return det != 0

    raise ValueError("Only 2x2 and 3x3 systems are supported.")


def solve_2x2(coefficients):
    """
    Solves a system of two equations with two variables.
    coefficients: [[a1, b1, c1], [a2, b2, c2]]
    Returns (x, y).
    """
    if len(coefficients) != 2 or any(len(row) != 3 for row in coefficients):
        raise ValueError("A 2x2 system requires two rows of three values each (a, b, c).")

    a1, b1, c1 = coefficients[0]
    a2, b2, c2 = coefficients[1]

    det = _determinant_2x2(a1, b1, a2, b2)
    if det == 0:
        raise ValueError("The system does not have a unique solution.")

    x = _determinant_2x2(c1, b1, c2, b2) / det
    y = _determinant_2x2(a1, c1, a2, c2) / det
    return (x, y)


def solve_3x3(coefficients):
    """
    Solves a system of three equations with three variables using
    Cramer's rule.
    coefficients: [[a1,b1,c1,d1], [a2,b2,c2,d2], [a3,b3,c3,d3]]
    Returns (x, y, z).
    """
    if len(coefficients) != 3 or any(len(row) != 4 for row in coefficients):
        raise ValueError("A 3x3 system requires three rows of four values each (a, b, c, d).")

    def det3(m):
        return (
            m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
        )

    main_matrix = [row[:3] for row in coefficients]
    constants = [row[3] for row in coefficients]

    main_det = det3(main_matrix)
    if main_det == 0:
        raise ValueError("The system does not have a unique solution.")

    # Replace each column in turn with the constants column.
    matrix_x = [[constants[i] if j == 0 else main_matrix[i][j] for j in range(3)] for i in range(3)]
    matrix_y = [[constants[i] if j == 1 else main_matrix[i][j] for j in range(3)] for i in range(3)]
    matrix_z = [[constants[i] if j == 2 else main_matrix[i][j] for j in range(3)] for i in range(3)]

    x = det3(matrix_x) / main_det
    y = det3(matrix_y) / main_det
    z = det3(matrix_z) / main_det
    return (x, y, z)
