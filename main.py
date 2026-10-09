"""
main.py

CALC-X - Advanced Terminal Calculator

Entry point of the application. Displays the main menu, reads the
user's choice, and calls the corresponding module.

Run with:

    python main.py
"""


import calculator
import algebra
import equations
import matrix
import statistics
import calculus
import database


# ----------------------------------------------------------------------
# Small shared input helpers
# ----------------------------------------------------------------------


def read_float(prompt):
    """Reads a value from the user and converts it to a float, retrying
    on invalid input. Returns None if the user types 'cancel'."""

    while True:
        text = input(prompt).strip()

        if text.lower() == "cancel":
            return None

        try:
            return float(text)

        except ValueError:
            print(
                "Invalid number. Please enter a numeric value "
                "(or 'cancel' to go back)."
            )


def read_int(prompt, minimum=None, maximum=None):
    """Reads an integer from the user, retrying on invalid input."""

    while True:
        text = input(prompt).strip()

        if text == "":
            print("Input cannot be blank. Please try again.")
            continue

        try:
            value = int(text)

        except ValueError:
            print("Invalid input. Please enter a whole number.")
            continue

        if minimum is not None and value < minimum:
            print("Value must be at least " + str(minimum) + ".")
            continue

        if maximum is not None and value > maximum:
            print("Value must be at most " + str(maximum) + ".")
            continue

        return value


def read_number_list(prompt):
    """Reads a line of space-separated numbers and returns a list of floats."""

    while True:
        text = input(prompt).strip()

        if text == "":
            print("Input cannot be blank. Please try again.")
            continue

        parts = text.split()

        try:
            values = [float(p) for p in parts]
            return values

        except ValueError:
            print(
                "Invalid input. Please enter numbers separated by spaces."
            )


# ----------------------------------------------------------------------
# Menu / navigation
# ----------------------------------------------------------------------


def print_menu():
    """Displays the CALC-X main menu."""

    print("\n========================================")
    print("           CALC-X CALCULATOR")
    print("========================================")
    print("1. Basic Calculator")
    print("2. Scientific Calculator")
    print("3. Algebra Solver")
    print("4. Equation Solver")
    print("5. Matrix Operations")
    print("6. Statistics")
    print("7. Calculus")
    print("8. History")
    print("9. Exit")


def get_menu_choice():
    """Reads the user's menu choice and returns it as a string."""

    return input("Enter your choice: ").strip()


# ----------------------------------------------------------------------
# 1. Basic Calculator
# ----------------------------------------------------------------------


def basic_calculator(user_id):
    """Handles the basic calculator interaction."""

    print("\n--- Basic Calculator ---")
    print(
        "Supports + - * / % and parentheses. "
        "Type 'back' to return to the main menu."
    )

    while True:
        expression = input("\nEnter expression: ").strip()

        if expression.lower() == "back":
            break

        if expression == "":
            print("Error: expression cannot be blank. Please try again.")
            continue

        try:
            result = calculator.evaluate_expression(
                expression,
                mode="degree"
            )

            formatted_result = format_result(result)

            print("Result: " + formatted_result)

            # Save successful calculation to MySQL
            database.add_calculation(
                user_id,
                expression,
                formatted_result,
                "Basic"
            )

        except ZeroDivisionError as error:
            print("Error: " + str(error))

        except ValueError as error:
            print("Error: " + str(error))

        except Exception:
            print("Error: could not evaluate the expression.")


# ----------------------------------------------------------------------
# 2. Scientific Calculator
# ----------------------------------------------------------------------


def scientific_calculator(user_id):
    """Handles scientific calculations and angle mode."""

    print("\n--- Scientific Calculator ---")
    print(
        "Supported: ^, pow(), sqrt(), cbrt(), log(), ln(), "
        "logb(x,b), sin(), cos(), tan(),"
    )
    print(
        "asin(), acos(), atan(), pi, e, abs(), floor(), ceil()"
    )

    mode = choose_angle_mode()

    print(
        "Type 'mode' to change the angle mode, "
        "or 'back' to return to the main menu."
    )

    while True:
        expression = input(
            "\nEnter expression (mode: " + mode + "): "
        ).strip()

        if expression.lower() == "back":
            break

        if expression.lower() == "mode":
            mode = choose_angle_mode()
            continue

        if expression == "":
            print("Error: expression cannot be blank. Please try again.")
            continue

        try:
            result = calculator.evaluate_expression(
                expression,
                mode=mode
            )

            formatted_result = format_result(result)

            print("Result: " + formatted_result)

            # Save successful calculation to MySQL
            database.add_calculation(
                user_id,
                expression,
                formatted_result,
                "Scientific"
            )

        except ZeroDivisionError as error:
            print("Error: " + str(error))

        except ValueError as error:
            print("Error: " + str(error))

        except Exception:
            print(
                "Error: could not evaluate the expression. "
                "Please check the syntax."
            )


def choose_angle_mode():
    """Prompts the user to choose 'degree' or 'radian' mode."""

    while True:
        choice = input(
            "Select angle mode - (D)egree or (R)adian: "
        ).strip().lower()

        if choice in ("d", "degree"):
            return "degree"

        if choice in ("r", "radian"):
            return "radian"

        print("Invalid mode. Please enter D or R.")


def format_result(value):
    """Formats a numeric result, dropping an unnecessary trailing '.0'."""

    try:
        if float(value).is_integer():
            return str(int(value))

        return str(round(value, 6))

    except (TypeError, ValueError):
        return str(value)


# ----------------------------------------------------------------------
# 3. Algebra Solver
# ----------------------------------------------------------------------


def algebra_solver(user_id):
    """Handles linear, quadratic, and polynomial calculations."""

    while True:
        print("\n--- Algebra Solver ---")
        print("1. Linear Equation (ax + b = 0)")
        print("2. Quadratic Equation (ax^2 + bx + c = 0)")
        print("3. Evaluate Polynomial")
        print("4. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        # --------------------------------------------------------------
        # Linear Equation
        # --------------------------------------------------------------

        if choice == "1":

            a = read_float("Enter a: ")

            if a is None:
                continue

            b = read_float("Enter b: ")

            if b is None:
                continue

            try:
                x = algebra.solve_linear(a, b)

                formatted_result = format_result(x)

                print("x = " + formatted_result)

                # Save successful calculation
                database.add_calculation(
                    user_id,
                    f"{a}x + {b} = 0",
                    formatted_result,
                    "Algebra"
                )

            except ValueError as error:
                print("Error: " + str(error))

        # --------------------------------------------------------------
        # Quadratic Equation
        # --------------------------------------------------------------

        elif choice == "2":

            a = read_float("Enter a: ")

            if a is None:
                continue

            b = read_float("Enter b: ")

            if b is None:
                continue

            c = read_float("Enter c: ")

            if c is None:
                continue

            try:
                roots = algebra.solve_quadratic(a, b, c)

                if roots is None:
                    print(
                        "No real roots "
                        "(discriminant is negative)."
                    )

                elif len(roots) == 1:

                    result = (
                        "x = " +
                        format_result(roots[0])
                    )

                    print(
                        "Repeated real root: " +
                        result
                    )

                    database.add_calculation(
                        user_id,
                        f"{a}x^2 + {b}x + {c} = 0",
                        result,
                        "Algebra"
                    )

                else:

                    result = (
                        "x1 = " +
                        format_result(roots[0]) +
                        ", x2 = " +
                        format_result(roots[1])
                    )

                    print(result)

                    database.add_calculation(
                        user_id,
                        f"{a}x^2 + {b}x + {c} = 0",
                        result,
                        "Algebra"
                    )

            except ValueError as error:
                print("Error: " + str(error))

        # --------------------------------------------------------------
        # Polynomial Evaluation
        # --------------------------------------------------------------

        elif choice == "3":

            print(
                "Enter polynomial coefficients "
                "from highest degree to constant term."
            )

            coeffs = read_number_list(
                "Coefficients "
                "(e.g. '3 4 5' for 3x^2+4x+5): "
            )

            x_value = read_float("Enter value of x: ")

            if x_value is None:
                continue

            try:
                result = algebra.evaluate_polynomial(
                    coeffs,
                    x_value
                )

                degree = algebra.polynomial_degree(coeffs)

                formatted_result = format_result(result)

                print(
                    "Polynomial degree: " +
                    str(degree)
                )

                print(
                    "Result: " +
                    formatted_result
                )

                # Save successful calculation
                database.add_calculation(
                    user_id,
                    f"Polynomial {coeffs}, x = {x_value}",
                    formatted_result,
                    "Algebra"
                )

            except ValueError as error:
                print("Error: " + str(error))

        elif choice == "4":
            break

        else:
            print("Invalid choice. Please try again.")


# ----------------------------------------------------------------------
# 4. Equation Solver
# ----------------------------------------------------------------------


def equation_solver(user_id):
    """Handles simultaneous equation solving."""

    while True:
        print("\n--- Equation Solver ---")
        print("1. Solve 2x2 System (2 variables)")
        print("2. Solve 3x3 System (3 variables)")
        print("3. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        # --------------------------------------------------------------
        # 2x2
        # --------------------------------------------------------------

        if choice == "1":

            print(
                "Enter each equation as: a b c "
                "(meaning a*x + b*y = c)"
            )

            try:
                rows = []

                for i in range(2):

                    row = read_number_list(
                        "Equation " +
                        str(i + 1) +
                        ": "
                    )

                    if len(row) != 3:
                        raise ValueError(
                            "Each equation needs exactly "
                            "3 values: a b c."
                        )

                    rows.append(row)

                x, y = equations.solve_2x2(rows)

                result = (
                    "x = " +
                    format_result(x) +
                    ", y = " +
                    format_result(y)
                )

                print(result)

                # Save successful calculation
                database.add_calculation(
                    user_id,
                    f"2x2 system {rows}",
                    result,
                    "Equation"
                )

            except ValueError as error:
                print("Error: " + str(error))

        # --------------------------------------------------------------
        # 3x3
        # --------------------------------------------------------------

        elif choice == "2":

            print(
                "Enter each equation as: a b c d "
                "(meaning a*x + b*y + c*z = d)"
            )

            try:
                rows = []

                for i in range(3):

                    row = read_number_list(
                        "Equation " +
                        str(i + 1) +
                        ": "
                    )

                    if len(row) != 4:
                        raise ValueError(
                            "Each equation needs exactly "
                            "4 values: a b c d."
                        )

                    rows.append(row)

                x, y, z = equations.solve_3x3(rows)

                result = (
                    "x = " +
                    format_result(x) +
                    ", y = " +
                    format_result(y) +
                    ", z = " +
                    format_result(z)
                )

                print(result)

                # Save successful calculation
                database.add_calculation(
                    user_id,
                    f"3x3 system {rows}",
                    result,
                    "Equation"
                )

            except ValueError as error:
                print("Error: " + str(error))

        elif choice == "3":
            break

        else:
            print("Invalid choice. Please try again.")


# ----------------------------------------------------------------------
# 5. Matrix Operations
# ----------------------------------------------------------------------


def read_matrix(label):
    """Reads a matrix from the user, row by row."""

    rows = read_int(
        "Number of rows for " +
        label +
        ": ",
        minimum=1
    )

    cols = read_int(
        "Number of columns for " +
        label +
        ": ",
        minimum=1
    )

    matrix_data = []

    print("Enter each row as space-separated numbers.")

    for i in range(rows):

        row = read_number_list(
            "Row " +
            str(i + 1) +
            ": "
        )

        while len(row) != cols:

            print(
                "Error: row must have exactly " +
                str(cols) +
                " value(s). Please re-enter."
            )

            row = read_number_list(
                "Row " +
                str(i + 1) +
                ": "
            )

        matrix_data.append(row)

    return matrix_data


def print_matrix(A):

    for row in A:
        print(
            "  " +
            str([format_result(v) for v in row])
        )


def matrix_operations(user_id):
    """Handles matrix operations and displays results."""

    while True:
        print("\n--- Matrix Operations ---")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Transpose")
        print("5. Determinant")
        print("6. Inverse")
        print("7. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        try:

            # ----------------------------------------------------------
            # Addition
            # ----------------------------------------------------------

            if choice == "1":

                A = read_matrix("Matrix A")
                B = read_matrix("Matrix B")

                result = matrix.add_matrices(A, B)

                print("Result:")
                print_matrix(result)

                database.add_calculation(
                    user_id,
                    f"{A} + {B}",
                    str(result),
                    "Matrix"
                )

            # ----------------------------------------------------------
            # Subtraction
            # ----------------------------------------------------------

            elif choice == "2":

                A = read_matrix("Matrix A")
                B = read_matrix("Matrix B")

                result = matrix.subtract_matrices(A, B)

                print("Result:")
                print_matrix(result)

                database.add_calculation(
                    user_id,
                    f"{A} - {B}",
                    str(result),
                    "Matrix"
                )

            # ----------------------------------------------------------
            # Multiplication
            # ----------------------------------------------------------

            elif choice == "3":

                A = read_matrix("Matrix A")
                B = read_matrix("Matrix B")

                result = matrix.multiply_matrices(A, B)

                print("Result:")
                print_matrix(result)

                database.add_calculation(
                    user_id,
                    f"{A} * {B}",
                    str(result),
                    "Matrix"
                )

            # ----------------------------------------------------------
            # Transpose
            # ----------------------------------------------------------

            elif choice == "4":

                A = read_matrix("Matrix A")

                result = matrix.transpose_matrix(A)

                print("Result:")
                print_matrix(result)

                database.add_calculation(
                    user_id,
                    f"transpose({A})",
                    str(result),
                    "Matrix"
                )

            # ----------------------------------------------------------
            # Determinant
            # ----------------------------------------------------------

            elif choice == "5":

                A = read_matrix("Matrix A")

                result = matrix.determinant(A)

                formatted_result = format_result(result)

                print(
                    "Determinant: " +
                    formatted_result
                )

                database.add_calculation(
                    user_id,
                    f"determinant({A})",
                    formatted_result,
                    "Matrix"
                )

            # ----------------------------------------------------------
            # Inverse
            # ----------------------------------------------------------

            elif choice == "6":

                A = read_matrix("Matrix A")

                result = matrix.inverse_matrix(A)

                print("Inverse:")
                print_matrix(result)

                database.add_calculation(
                    user_id,
                    f"inverse({A})",
                    str(result),
                    "Matrix"
                )

            elif choice == "7":
                break

            else:
                print("Invalid choice. Please try again.")

        except ValueError as error:
            print("Error: " + str(error))


# ----------------------------------------------------------------------
# 6. Statistics
# ----------------------------------------------------------------------


def statistics_module(user_id):
    """Handles statistical calculations."""

    print("\n--- Statistics ---")

    data = read_number_list(
        "Enter numbers separated by spaces: "
    )

    try:

        mean = statistics.calculate_mean(data)
        median = statistics.calculate_median(data)
        mode = statistics.calculate_mode(data)
        minimum = statistics.calculate_min(data)
        maximum = statistics.calculate_max(data)
        data_range = statistics.calculate_range(data)
        variance = statistics.calculate_variance(data)
        std_dev = statistics.calculate_standard_deviation(data)

        print(
            "Mean: " +
            format_result(mean)
        )

        print(
            "Median: " +
            format_result(median)
        )

        print(
            "Mode: " +
            ", ".join(
                format_result(m)
                for m in mode
            )
        )

        print(
            "Minimum: " +
            format_result(minimum)
        )

        print(
            "Maximum: " +
            format_result(maximum)
        )

        print(
            "Range: " +
            format_result(data_range)
        )

        print(
            "Variance: " +
            format_result(variance)
        )

        print(
            "Standard Deviation: " +
            format_result(std_dev)
        )

        # Store all statistics from this dataset
        result = (
            "Mean=" + format_result(mean) +
            ", Median=" + format_result(median) +
            ", Mode=" +
            ", ".join(
                format_result(m)
                for m in mode
            ) +
            ", Minimum=" + format_result(minimum) +
            ", Maximum=" + format_result(maximum) +
            ", Range=" + format_result(data_range) +
            ", Variance=" + format_result(variance) +
            ", Standard Deviation=" +
            format_result(std_dev)
        )

        database.add_calculation(
            user_id,
            f"Statistics {data}",
            result,
            "Statistics"
        )

    except ValueError as error:
        print("Error: " + str(error))


# ----------------------------------------------------------------------
# 7. Calculus
# ----------------------------------------------------------------------


def calculus_module(user_id):
    """Handles differentiation and integration."""

    while True:
        print("\n--- Calculus ---")
        print("1. Differentiate Polynomial")
        print("2. Integrate Polynomial")
        print("3. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        # --------------------------------------------------------------
        # Differentiation
        # --------------------------------------------------------------

        if choice == "1":

            print(
                "Enter polynomial coefficients "
                "from highest degree to constant term."
            )

            coeffs = read_number_list(
                "Coefficients "
                "(e.g. '3 4 5' for 3x^2+4x+5): "
            )

            try:

                derivative = calculus.differentiate_polynomial(
                    coeffs
                )

                derivative_text = calculus.format_polynomial(
                    derivative
                )

                print(
                    "Derivative: " +
                    derivative_text
                )

                database.add_calculation(
                    user_id,
                    f"differentiate({coeffs})",
                    derivative_text,
                    "Calculus"
                )

            except ValueError as error:
                print("Error: " + str(error))

        # --------------------------------------------------------------
        # Integration
        # --------------------------------------------------------------

        elif choice == "2":

            print(
                "Enter polynomial coefficients "
                "from highest degree to constant term."
            )

            coeffs = read_number_list(
                "Coefficients "
                "(e.g. '6 4' for 6x+4): "
            )

            try:

                original_degree = len(coeffs) - 1

                integral = calculus.integrate_polynomial(
                    coeffs
                )

                integral_text = calculus.format_polynomial(
                    integral,
                    add_constant=True,
                    starting_degree=original_degree + 1
                )

                print(
                    "Integral: " +
                    integral_text
                )

                database.add_calculation(
                    user_id,
                    f"integrate({coeffs})",
                    integral_text,
                    "Calculus"
                )

            except ValueError as error:
                print("Error: " + str(error))

        elif choice == "3":
            break

        else:
            print("Invalid choice. Please try again.")


# ----------------------------------------------------------------------
# 8. History
# ----------------------------------------------------------------------


def history_menu(user_id):
    """Displays and manages calculation history using MySQL."""

    while True:

        print("\n--- History ---")
        print("1. View History")
        print("2. Search History")
        print("3. Delete Calculation")
        print("4. Clear History")
        print("5. Database Statistics")
        print("6. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        # --------------------------------------------------------------
        # View History
        # --------------------------------------------------------------

        if choice == "1":

            records = database.get_history(user_id)

            if not records:

                print("No calculation history found.")

            else:

                print("\n--- Calculation History ---")

                for record in records:

                    calculation_id, expression, result, module, timestamp = record

                    print(
                        f"ID: {calculation_id} | "
                        f"{expression} = {result} | "
                        f"Module: {module} | "
                        f"Time: {timestamp}"
                    )

        # --------------------------------------------------------------
        # Search History
        # --------------------------------------------------------------

        elif choice == "2":

            keyword = input(
                "Enter expression keyword to search: "
            ).strip()

            if not keyword:

                print("Search keyword cannot be empty.")
                continue

            records = database.search_history(
                user_id,
                keyword
            )

            if not records:

                print("No matching calculations found.")

            else:

                print("\n--- Search Results ---")

                for record in records:

                    calculation_id, expression, result, module, timestamp = record

                    print(
                        f"ID: {calculation_id} | "
                        f"{expression} = {result} | "
                        f"Module: {module} | "
                        f"Time: {timestamp}"
                    )

        # --------------------------------------------------------------
        # Delete Calculation
        # --------------------------------------------------------------

        elif choice == "3":

            calculation_id = input(
                "Enter calculation ID to delete: "
            ).strip()

            if not calculation_id.isdigit():

                print(
                    "Please enter a valid calculation ID."
                )
                continue

            database.delete_calculation(
                user_id,
                int(calculation_id)
            )

        # --------------------------------------------------------------
        # Clear History
        # --------------------------------------------------------------

        elif choice == "4":

            confirm = input(
                "Are you sure you want to clear all history? (y/n): "
            ).strip().lower()

            if confirm == "y":

                database.clear_history(user_id)

            else:

                print("Clear operation cancelled.")

        # --------------------------------------------------------------
        # Database Statistics
        # --------------------------------------------------------------

        elif choice == "5":

            records = database.get_module_statistics(
                user_id
            )

            if not records:

                print(
                    "No calculation statistics available."
                )

            else:

                print("\n--- Database Statistics ---")

                for module, count in records:

                    print(
                        f"{module}: "
                        f"{count} calculation(s)"
                    )

        elif choice == "6":
            break

        else:
            print("Invalid choice. Please try again.")


# ----------------------------------------------------------------------
# Main program loop
# ----------------------------------------------------------------------


def main():

    print("========================================")
    print("           CALC-X CALCULATOR")
    print("========================================")

    # --------------------------------------------------------------
    # Get username
    # --------------------------------------------------------------

    username = input(
        "Enter username: "
    ).strip()

    while username == "":

        print("Username cannot be blank.")

        username = input(
            "Enter username: "
        ).strip()

    # --------------------------------------------------------------
    # Create or get user from MySQL
    # --------------------------------------------------------------

    user_id = database.create_user(
        username
    )

    if user_id is None:

        print(
            "Could not connect to the database."
        )

        print(
            "Please check your MySQL configuration."
        )

        return

    print(
        "Welcome, " +
        username +
        "!"
    )

    # --------------------------------------------------------------
    # Main menu loop
    # --------------------------------------------------------------

    while True:

        print_menu()

        choice = get_menu_choice()

        if choice == "1":

            basic_calculator(user_id)

        elif choice == "2":

            scientific_calculator(user_id)

        elif choice == "3":

            algebra_solver(user_id)

        elif choice == "4":

            equation_solver(user_id)

        elif choice == "5":

            matrix_operations(user_id)

        elif choice == "6":

            statistics_module(user_id)

        elif choice == "7":

            calculus_module(user_id)

        elif choice == "8":

            history_menu(user_id)

        elif choice == "9":

            print("Goodbye!")
            break

        else:

            print("Invalid choice. Please try again.")


# ----------------------------------------------------------------------
# Program entry point
# ----------------------------------------------------------------------


if __name__ == "__main__":
    main()