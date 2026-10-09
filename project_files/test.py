"""
CALC-X - Unit Tests for the Current MySQL Version

These tests are aligned with the current CALC-X project structure:
- calculator.py
- algebra.py
- equations.py
- matrix.py
- statistics.py
- calculus.py
- database.py
- main.py

The old file-based history.py tests have been removed because the
current project stores calculation history in MySQL through database.py.

How to run:
    python -m unittest test.py -v
"""

import os
import sys
import math
import unittest
from unittest.mock import patch, MagicMock
from io import StringIO

# Make sure the project's own folder is searched first so the local
# statistics.py module is imported instead of Python's standard module.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import calculator
import algebra
import equations
import matrix
import statistics
import calculus
import database
import main


# ============================================================
# 1. MAIN MENU / NAVIGATION
# ============================================================

class TestMainMenu(unittest.TestCase):

    def test_print_menu_lists_all_nine_options(self):
        captured = StringIO()

        with patch("sys.stdout", captured):
            main.print_menu()

        output = captured.getvalue()

        for option in [
            "1. Basic Calculator",
            "2. Scientific Calculator",
            "3. Algebra Solver",
            "4. Equation Solver",
            "5. Matrix Operations",
            "6. Statistics",
            "7. Calculus",
            "8. History",
            "9. Exit",
        ]:
            self.assertIn(option, output)

    def test_get_menu_choice_strips_whitespace(self):
        with patch("builtins.input", return_value="  5  "):
            choice = main.get_menu_choice()

        self.assertEqual(choice, "5")


# ============================================================
# 2. BASIC CALCULATOR
# ============================================================

class TestBasicCalculator(unittest.TestCase):

    def test_basic_arithmetic_operators(self):
        cases = [
            ("25 + 10", 35.0),
            ("25 - 10", 15.0),
            ("25 * 10", 250.0),
            ("25 / 5", 5.0),
        ]

        for expression, expected in cases:
            with self.subTest(expression=expression):
                self.assertEqual(
                    calculator.evaluate_expression(expression),
                    expected
                )

    def test_modulus(self):
        self.assertEqual(
            calculator.evaluate_expression("25 % 4"),
            1.0
        )

    def test_bodmas_parentheses_precedence(self):
        self.assertEqual(
            calculator.evaluate_expression("2 + 5 * (3 + 4)"),
            37.0
        )

    def test_invalid_expression_unmatched_parenthesis(self):
        with self.assertRaises(ValueError):
            calculator.evaluate_expression("2 + (3")

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            calculator.evaluate_expression("10 / 0")


# ============================================================
# 3. SCIENTIFIC CALCULATOR
# ============================================================

class TestScientificCalculator(unittest.TestCase):

    def test_power_operator(self):
        self.assertEqual(
            calculator.evaluate_expression("2^5"),
            32.0
        )

    def test_square_root(self):
        self.assertEqual(
            calculator.evaluate_expression("sqrt(144)"),
            12.0
        )

    def test_cube_root(self):
        self.assertEqual(
            calculator.evaluate_expression("cbrt(27)"),
            3.0
        )

    def test_log_base_10(self):
        result = calculator.evaluate_expression("log(1000)")
        self.assertTrue(math.isclose(result, 3.0, rel_tol=1e-9))

    def test_natural_log_and_custom_base_log(self):
        ln_result = calculator.evaluate_expression("ln(e)")
        logb_result = calculator.evaluate_expression("logb(81,3)")

        self.assertTrue(math.isclose(ln_result, 1.0, rel_tol=1e-9))
        self.assertTrue(math.isclose(logb_result, 4.0, rel_tol=1e-9))

    def test_trig_degree_and_radian_modes(self):
        degree_result = calculator.evaluate_expression(
            "sin(30)",
            mode="degree"
        )
        radian_result = calculator.evaluate_expression(
            "sin(pi/2)",
            mode="radian"
        )

        self.assertTrue(math.isclose(degree_result, 0.5, rel_tol=1e-9))
        self.assertTrue(math.isclose(radian_result, 1.0, rel_tol=1e-9))

    def test_sqrt_negative_raises_value_error(self):
        with self.assertRaises(ValueError):
            calculator.evaluate_expression("sqrt(-9)")


# ============================================================
# 4. ALGEBRA SOLVER
# ============================================================

class TestAlgebraSolver(unittest.TestCase):

    def test_solve_linear(self):
        self.assertEqual(
            algebra.solve_linear(2, -10),
            5.0
        )

    def test_solve_quadratic_two_real_roots(self):
        roots = algebra.solve_quadratic(1, -5, 6)

        self.assertEqual(len(roots), 2)
        self.assertTrue(math.isclose(roots[0], 3.0))
        self.assertTrue(math.isclose(roots[1], 2.0))

    def test_solve_quadratic_repeated_root(self):
        roots = algebra.solve_quadratic(1, -4, 4)

        self.assertEqual(len(roots), 1)
        self.assertTrue(math.isclose(roots[0], 2.0))

    def test_solve_quadratic_negative_discriminant(self):
        result = algebra.solve_quadratic(1, 0, 1)
        self.assertIsNone(result)


# ============================================================
# 5. EQUATION SOLVER
# ============================================================

class TestEquationSolver(unittest.TestCase):

    def test_solve_2x2_known_solution(self):
        x, y = equations.solve_2x2(
            [[2, 3, 13], [4, -1, 5]]
        )

        self.assertTrue(math.isclose(x, 2.0))
        self.assertTrue(math.isclose(y, 3.0))

    def test_solve_2x2_no_unique_solution(self):
        with self.assertRaises(ValueError):
            equations.solve_2x2(
                [[1, 2, 3], [2, 4, 6]]
            )

    def test_solve_3x3_known_solution(self):
        # 2x + y + z = 4
        # x + 3y + 2z = 5
        # x = 6
        # Correct solution: x=6, y=15, z=-23
        x, y, z = equations.solve_3x3(
            [
                [2, 1, 1, 4],
                [1, 3, 2, 5],
                [1, 0, 0, 6],
            ]
        )

        self.assertTrue(math.isclose(x, 6.0))
        self.assertTrue(math.isclose(y, 15.0))
        self.assertTrue(math.isclose(z, -23.0))


# ============================================================
# 6. MATRIX OPERATIONS
# ============================================================

class TestMatrixOperations(unittest.TestCase):

    def test_matrix_addition_and_subtraction(self):
        A = [[1, 2], [3, 4]]
        B = [[5, 6], [7, 8]]

        self.assertEqual(
            matrix.add_matrices(A, B),
            [[6, 8], [10, 12]]
        )

        self.assertEqual(
            matrix.subtract_matrices(B, A),
            [[4, 4], [4, 4]]
        )

    def test_matrix_multiplication(self):
        result = matrix.multiply_matrices(
            [[1, 2], [3, 4]],
            [[5, 6], [7, 8]]
        )

        self.assertEqual(
            result,
            [[19, 22], [43, 50]]
        )

    def test_matrix_transpose(self):
        result = matrix.transpose_matrix(
            [[1, 2], [3, 4]]
        )

        self.assertEqual(
            result,
            [[1, 3], [2, 4]]
        )

    def test_matrix_determinant(self):
        self.assertEqual(
            matrix.determinant([[1, 2], [3, 4]]),
            -2
        )

    def test_matrix_inverse(self):
        result = matrix.inverse_matrix(
            [[1, 2], [3, 4]]
        )

        expected = [
            [-2.0, 1.0],
            [1.5, -0.5]
        ]

        for result_row, expected_row in zip(result, expected):
            for result_value, expected_value in zip(
                result_row,
                expected_row
            ):
                self.assertTrue(
                    math.isclose(result_value, expected_value)
                )

    def test_invalid_dimension_and_singular_matrix(self):
        with self.assertRaises(ValueError):
            matrix.add_matrices(
                [[1, 2]],
                [[1, 2, 3]]
            )

        with self.assertRaises(ValueError):
            matrix.inverse_matrix(
                [[1, 2], [2, 4]]
            )


# ============================================================
# 7. STATISTICS
# ============================================================

class TestStatistics(unittest.TestCase):

    def setUp(self):
        self.data = [10, 20, 20, 30, 40]

    def test_mean(self):
        self.assertEqual(
            statistics.calculate_mean(self.data),
            24.0
        )

    def test_median(self):
        self.assertEqual(
            statistics.calculate_median(self.data),
            20
        )

    def test_mode(self):
        self.assertEqual(
            statistics.calculate_mode(self.data),
            [20]
        )

    def test_range(self):
        self.assertEqual(
            statistics.calculate_range(self.data),
            30
        )

    def test_variance_and_standard_deviation(self):
        variance = statistics.calculate_variance(self.data)
        std_dev = statistics.calculate_standard_deviation(self.data)

        self.assertTrue(math.isclose(variance, 104.0))
        self.assertTrue(
            math.isclose(std_dev, math.sqrt(104.0))
        )

    def test_empty_data_raises_value_error(self):
        with self.assertRaises(ValueError):
            statistics.calculate_mean([])


# ============================================================
# 8. CALCULUS
# ============================================================

class TestCalculus(unittest.TestCase):

    def test_differentiate_polynomial(self):
        # 3x^2 + 4x + 5 -> 6x + 4
        result = calculus.differentiate_polynomial(
            [3, 4, 5]
        )

        self.assertEqual(result, [6, 4])

    def test_integrate_polynomial_and_format(self):
        # 6x + 4 -> 3x^2 + 4x + C
        result = calculus.integrate_polynomial([6, 4])

        self.assertEqual(result, [3.0, 4.0])

        text = calculus.format_polynomial(
            result,
            add_constant=True,
            starting_degree=2
        )

        self.assertEqual(
            text,
            "3x^2 + 4x + C"
        )

    def test_differentiate_empty_polynomial(self):
        with self.assertRaises(ValueError):
            calculus.differentiate_polynomial([])


# ============================================================
# 9. DATABASE FUNCTIONS - MYSQL VERSION
# ============================================================

class TestDatabaseFunctions(unittest.TestCase):

    def setUp(self):
        # Database tests are mocked so running test.py does not modify
        # the user's actual MySQL database.
        self.connection = MagicMock()
        self.cursor = MagicMock()

        self.connection.is_connected.return_value = True
        self.connection.cursor.return_value = self.cursor

    def test_connect_database_success(self):
        with patch(
            "database.mysql.connector.connect",
            return_value=self.connection
        ) as mock_connect:

            result = database.connect_database()

            mock_connect.assert_called_once_with(
                **database.DB_CONFIG
            )
            self.assertIs(result, self.connection)

    def test_connect_database_failure(self):
        with patch(
            "database.mysql.connector.connect",
            side_effect=database.Error("connection failed")
        ):
            result = database.connect_database()
            self.assertIsNone(result)

    def test_create_user_existing_user(self):
        self.cursor.fetchone.return_value = (7,)

        with patch(
            "database.connect_database",
            return_value=self.connection
        ):
            result = database.create_user("RK")

        self.assertEqual(result, 7)
        self.cursor.execute.assert_called_once()

    def test_create_user_new_user(self):
        self.cursor.fetchone.return_value = None
        self.cursor.lastrowid = 12

        with patch(
            "database.connect_database",
            return_value=self.connection
        ):
            result = database.create_user("NewUser")

        self.assertEqual(result, 12)
        self.connection.commit.assert_called_once()

    def test_add_calculation(self):
        with patch(
            "database.connect_database",
            return_value=self.connection
        ):
            result = database.add_calculation(
                1,
                "2 + 5 * 3",
                "17",
                "Basic"
            )

        self.assertIsNone(result)
        self.cursor.execute.assert_called_once()
        self.connection.commit.assert_called_once()

    def test_get_history(self):
        expected = [
            (1, "2 + 2", "4", "Basic", "timestamp")
        ]
        self.cursor.fetchall.return_value = expected

        with patch(
            "database.connect_database",
            return_value=self.connection
        ):
            result = database.get_history(1)

        self.assertEqual(result, expected)

    def test_search_history(self):
        expected = [
            (1, "sqrt(144)", "12", "Scientific", "timestamp")
        ]
        self.cursor.fetchall.return_value = expected

        with patch(
            "database.connect_database",
            return_value=self.connection
        ):
            result = database.search_history(1, "sqrt")

        self.assertEqual(result, expected)

        query, params = self.cursor.execute.call_args[0]
        self.assertIn("LIKE", query.upper())
        self.assertEqual(params, (1, "%sqrt%"))

    def test_delete_calculation_success(self):
        self.cursor.rowcount = 1

        captured = StringIO()

        with patch(
            "database.connect_database",
            return_value=self.connection
        ), patch("sys.stdout", captured):

            database.delete_calculation(1, 5)

        self.connection.commit.assert_called_once()
        self.assertIn(
            "Calculation deleted successfully",
            captured.getvalue()
        )

    def test_delete_calculation_not_found(self):
        self.cursor.rowcount = 0

        captured = StringIO()

        with patch(
            "database.connect_database",
            return_value=self.connection
        ), patch("sys.stdout", captured):

            database.delete_calculation(1, 999)

        self.assertIn(
            "Calculation not found",
            captured.getvalue()
        )

    def test_clear_history(self):
        captured = StringIO()

        with patch(
            "database.connect_database",
            return_value=self.connection
        ), patch("sys.stdout", captured):

            database.clear_history(1)

        self.connection.commit.assert_called_once()
        self.assertIn(
            "History cleared successfully",
            captured.getvalue()
        )

    def test_get_module_statistics(self):
        expected = [
            ("Basic", 5),
            ("Scientific", 2)
        ]
        self.cursor.fetchall.return_value = expected

        with patch(
            "database.connect_database",
            return_value=self.connection
        ):
            result = database.get_module_statistics(1)

        self.assertEqual(result, expected)


# ============================================================
# 10. CURRENT MYSQL HISTORY MENU
# ============================================================

class TestHistoryMenu(unittest.TestCase):

    def test_history_menu_view_history(self):
        history_rows = [
            (1, "2 + 5", "7", "Basic", "2026-01-01 10:00:00")
        ]

        with patch(
            "builtins.input",
            side_effect=["1", "6"]
        ), patch(
            "database.get_history",
            return_value=history_rows
        ), patch("sys.stdout", new_callable=StringIO) as captured:

            main.history_menu(1)

        output = captured.getvalue()

        self.assertIn("2 + 5", output)
        self.assertIn("7", output)

    def test_history_menu_search(self):
        search_rows = [
            (2, "sqrt(144)", "12", "Scientific", "2026-01-01 10:00:00")
        ]

        with patch(
            "builtins.input",
            side_effect=["2", "sqrt", "6"]
        ), patch(
            "database.search_history",
            return_value=search_rows
        ), patch("sys.stdout", new_callable=StringIO) as captured:

            main.history_menu(1)

        output = captured.getvalue()

        self.assertIn("sqrt(144)", output)
        self.assertIn("12", output)

    def test_history_menu_delete(self):
        with patch(
            "builtins.input",
            side_effect=["3", "5", "6"]
        ), patch(
            "database.delete_calculation"
        ) as mock_delete, patch(
            "sys.stdout",
            new_callable=StringIO
        ):

            main.history_menu(1)

        mock_delete.assert_called_once_with(1, 5)

    def test_history_menu_clear(self):
        # Choice 4 asks for confirmation before clearing history.
        # Then choice 6 exits the History menu.
        with patch(
            "builtins.input",
            side_effect=["4", "y", "6"]
        ), patch(
            "database.clear_history"
        ) as mock_clear, patch(
            "sys.stdout",
            new_callable=StringIO
        ):

            main.history_menu(1)

        mock_clear.assert_called_once_with(1)

    def test_history_menu_database_statistics(self):
        stats_rows = [
            ("Basic", 10),
            ("Scientific", 4)
        ]

        with patch(
            "builtins.input",
            side_effect=["5", "6"]
        ), patch(
            "database.get_module_statistics",
            return_value=stats_rows
        ), patch("sys.stdout", new_callable=StringIO) as captured:

            main.history_menu(1)

        output = captured.getvalue()

        self.assertIn("Basic", output)
        self.assertIn("10", output)
        self.assertIn("Scientific", output)
        self.assertIn("4", output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
