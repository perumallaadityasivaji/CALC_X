"""
matrix.py

Contains the Matrix Operations functionality: addition, subtraction,
multiplication, transpose, determinant, and inverse.

Matrices are represented as nested lists, e.g. [[1, 2], [3, 4]].
"""


def valid_dimensions(A, B):
    """
    Checks whether matrix dimensions are valid for an element-wise
    operation (addition/subtraction): both matrices must have the same
    number of rows and the same number of columns.
    """
    if len(A) != len(B):
        return False
    for row_a, row_b in zip(A, B):
        if len(row_a) != len(row_b):
            return False
    return True


def _is_rectangular(A):
    if not A:
        return False
    width = len(A[0])
    return all(len(row) == width for row in A)


def add_matrices(A, B):
    """Returns the sum of two matrices with matching dimensions."""
    if not _is_rectangular(A) or not _is_rectangular(B):
        raise ValueError("Invalid matrix input.")
    if not valid_dimensions(A, B):
        raise ValueError("Matrix dimensions do not match for addition.")

    result = []
    for i in range(len(A)):
        row = []
        for j in range(len(A[0])):
            row.append(A[i][j] + B[i][j])
        result.append(row)
    return result


def subtract_matrices(A, B):
    """Returns the difference of two matrices with matching dimensions."""
    if not _is_rectangular(A) or not _is_rectangular(B):
        raise ValueError("Invalid matrix input.")
    if not valid_dimensions(A, B):
        raise ValueError("Matrix dimensions do not match for subtraction.")

    result = []
    for i in range(len(A)):
        row = []
        for j in range(len(A[0])):
            row.append(A[i][j] - B[i][j])
        result.append(row)
    return result


def multiply_matrices(A, B):
    """Returns the matrix product when dimensions are compatible."""
    if not _is_rectangular(A) or not _is_rectangular(B):
        raise ValueError("Invalid matrix input.")

    cols_a = len(A[0])
    rows_b = len(B)
    if cols_a != rows_b:
        raise ValueError("Number of columns in the first matrix must equal "
                        "the number of rows in the second matrix.")

    rows_a = len(A)
    cols_b = len(B[0])

    result = []
    for i in range(rows_a):
        row = []
        for j in range(cols_b):
            total = 0
            for k in range(cols_a):
                total += A[i][k] * B[k][j]
            row.append(total)
        result.append(row)
    return result


def transpose_matrix(A):
    """Returns the transpose of a matrix."""
    if not _is_rectangular(A):
        raise ValueError("Invalid matrix input.")

    rows = len(A)
    cols = len(A[0])
    result = []
    for j in range(cols):
        row = []
        for i in range(rows):
            row.append(A[i][j])
        result.append(row)
    return result


def _is_square(A):
    return _is_rectangular(A) and len(A) == len(A[0])


def _minor(A, row_to_remove, col_to_remove):
    return [
        [A[i][j] for j in range(len(A)) if j != col_to_remove]
        for i in range(len(A)) if i != row_to_remove
    ]


def determinant(A):
    """Returns the determinant of a square matrix (recursive expansion)."""
    if not _is_square(A):
        raise ValueError("Determinant can only be calculated for a square matrix.")

    n = len(A)

    if n == 1:
        return A[0][0]

    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]

    total = 0
    sign = 1
    for col in range(n):
        minor = _minor(A, 0, col)
        total += sign * A[0][col] * determinant(minor)
        sign *= -1
    return total


def inverse_matrix(A):
    """Returns the inverse of a non-singular square matrix."""
    if not _is_square(A):
        raise ValueError("Inverse can only be calculated for a square matrix.")

    n = len(A)
    det = determinant(A)
    if det == 0:
        raise ValueError("Matrix is singular; inverse does not exist.")

    if n == 1:
        return [[1 / A[0][0]]]

    # Build the matrix of cofactors.
    cofactors = []
    for i in range(n):
        cofactor_row = []
        for j in range(n):
            minor = _minor(A, i, j)
            sign = 1 if (i + j) % 2 == 0 else -1
            cofactor_row.append(sign * determinant(minor))
        cofactors.append(cofactor_row)

    # Adjugate is the transpose of the cofactor matrix.
    adjugate = transpose_matrix(cofactors)

    result = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(adjugate[i][j] / det)
        result.append(row)
    return result
