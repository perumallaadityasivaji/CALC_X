"""
calculator.py

This file contains the expression evaluation engine used by both the
Basic Calculator and the Scientific Calculator modules.

It follows the flow described in the CALC-X Design Document:

    INPUT -> VALIDATE -> TOKENIZE -> HANDLE BRACKETS / GROUPED EXPRESSIONS
    -> EVALUATE FUNCTIONS -> POWERS / ROOTS -> * / % -> + -  -> ANSWER

The expression is NOT evaluated using Python's built-in eval(). Instead,
the expression is broken into tokens and then evaluated manually using a
simple, function-based (recursive) approach that respects BODMAS.
"""

import math
import re

# Names of the scientific functions CALC-X supports.
FUNCTIONS = [
    "sqrt", "cbrt", "log", "ln", "logb",
    "sin", "cos", "tan", "asin", "acos", "atan",
    "abs", "floor", "ceil", "pow"
]

# Names of the supported mathematical constants.
CONSTANTS = ["pi", "e"]


def validate_expression(expression):
    """
    Returns True if the expression has valid basic syntax, otherwise False.

    Checks performed:
    - The expression is not empty.
    - Parentheses are correctly matched.
    - Only digits, known function names, known constants, and supported
      operator/parenthesis/comma characters are present.
    """
    if expression is None:
        return False

    expr = expression.strip()
    if expr == "":
        return False

    # Check that parentheses are balanced.
    balance = 0
    for ch in expr:
        if ch == "(":
            balance += 1
        elif ch == ")":
            balance -= 1
        if balance < 0:
            return False
    if balance != 0:
        return False

    # Remove known function names and constants from a working copy.
    temp = expr
    for name in FUNCTIONS + CONSTANTS:
        temp = re.sub(r"\b" + name + r"\b", " ", temp)

    # Remove numbers (integers and decimals).
    temp = re.sub(r"\d+(\.\d+)?", " ", temp)

    # Remove allowed symbols and whitespace.
    temp = re.sub(r"[+\-*/%^(),.\s]", "", temp)

    # Anything left over means an unsupported letter/word/symbol was used.
    if temp != "":
        return False

    return True


def tokenize(expression):
    """
    Converts an expression string into a list of tokens.

    Numbers become floats, operators/parentheses/commas become single
    character strings, and words become strings (function names or
    constants such as 'pi' and 'e').
    """
    expr = expression.replace(" ", "")
    tokens = []
    i = 0
    n = len(expr)

    while i < n:
        ch = expr[i]

        if ch.isdigit() or ch == ".":
            j = i
            dot_seen = False
            while j < n and (expr[j].isdigit() or expr[j] == "."):
                if expr[j] == ".":
                    if dot_seen:
                        raise ValueError("Malformed number in expression.")
                    dot_seen = True
                j += 1
            tokens.append(float(expr[i:j]))
            i = j

        elif ch.isalpha():
            j = i
            while j < n and expr[j].isalpha():
                j += 1
            tokens.append(expr[i:j])
            i = j

        elif ch in "+-*/%^(),":
            tokens.append(ch)
            i += 1

        else:
            raise ValueError("Invalid character in expression: '" + ch + "'")

    return tokens


def calculate_power(base, exponent):
    """Returns the value of a number raised to a power."""
    try:
        result = base ** exponent
    except (ValueError, OverflowError):
        raise ValueError("Invalid power operation.")
    if isinstance(result, complex):
        raise ValueError("Power operation produced a non-real result.")
    return result


def calculate_log(value, base=10):
    """Returns the logarithm of a value using the specified base."""
    if value <= 0:
        raise ValueError("Logarithm is undefined for values less than or equal to 0.")
    if base <= 0 or base == 1:
        raise ValueError("Logarithm base must be positive and cannot be 1.")
    return math.log(value, base)


def apply_function(name, value, mode="degree"):
    """
    Calculates the requested scientific function using the selected
    angle mode ('degree' or 'radian').
    """
    if name == "sqrt":
        if value < 0:
            raise ValueError("Cannot calculate the square root of a negative number.")
        return math.sqrt(value)

    if name == "cbrt":
        if value < 0:
            return -((-value) ** (1.0 / 3.0))
        return value ** (1.0 / 3.0)

    if name == "log":
        return calculate_log(value, 10)

    if name == "ln":
        if value <= 0:
            raise ValueError("Natural logarithm is undefined for values less than or equal to 0.")
        return math.log(value)

    if name in ("sin", "cos", "tan"):
        if mode not in ("degree", "radian"):
            raise ValueError("Invalid angle mode.")
        angle = math.radians(value) if mode == "degree" else value
        if name == "sin":
            return math.sin(angle)
        if name == "cos":
            return math.cos(angle)
        # tan: check for a near-undefined result before computing.
        if abs(math.cos(angle)) < 1e-10:
            raise ValueError("Tangent is undefined at this angle.")
        return math.tan(angle)

    if name in ("asin", "acos"):
        if value < -1 or value > 1:
            raise ValueError(name + " is undefined outside the range [-1, 1].")
        result = math.asin(value) if name == "asin" else math.acos(value)
        return math.degrees(result) if mode == "degree" else result

    if name == "atan":
        result = math.atan(value)
        return math.degrees(result) if mode == "degree" else result

    if name == "abs":
        return abs(value)

    if name == "floor":
        return float(math.floor(value))

    if name == "ceil":
        return float(math.ceil(value))

    raise ValueError("Unsupported function: " + name)


def evaluate_expression(expression, mode="degree"):
    """
    Evaluates a complete mathematical expression according to BODMAS.

    Order of evaluation (as per the Design Document):
    brackets -> functions -> powers -> * / % -> + -
    """
    if not validate_expression(expression):
        raise ValueError("Invalid expression.")

    tokens = tokenize(expression)
    if not tokens:
        raise ValueError("Empty expression.")

    position = [0]  # Mutable index so nested functions can advance it.

    def peek():
        if position[0] < len(tokens):
            return tokens[position[0]]
        return None

    def advance():
        tok = tokens[position[0]]
        position[0] += 1
        return tok

    def parse_expression_level():
        value = parse_term()
        while peek() in ("+", "-"):
            op = advance()
            right = parse_term()
            value = value + right if op == "+" else value - right
        return value

    def parse_term():
        value = parse_power_level()
        while peek() in ("*", "/", "%"):
            op = advance()
            right = parse_power_level()
            if op == "*":
                value = value * right
            elif op == "/":
                if right == 0:
                    raise ZeroDivisionError("Division by zero is not allowed.")
                value = value / right
            else:
                if right == 0:
                    raise ZeroDivisionError("Modulus by zero is not allowed.")
                value = value % right
        return value

    def parse_power_level():
        value = parse_unary()
        if peek() == "^":
            advance()
            exponent = parse_power_level()  # right-associative
            value = calculate_power(value, exponent)
        return value

    def parse_unary():
        if peek() == "-":
            advance()
            return -parse_unary()
        if peek() == "+":
            advance()
            return parse_unary()
        return parse_primary()

    def parse_primary():
        tok = peek()
        if tok is None:
            raise ValueError("Unexpected end of expression.")

        if isinstance(tok, float):
            advance()
            return tok

        if tok == "(":
            advance()
            value = parse_expression_level()
            if peek() != ")":
                raise ValueError("Unmatched parenthesis in expression.")
            advance()
            return value

        if isinstance(tok, str) and tok.isalpha():
            advance()
            if tok == "pi":
                return math.pi
            if tok == "e":
                return math.e
            if tok in FUNCTIONS:
                if peek() != "(":
                    raise ValueError("Expected '(' after function name '" + tok + "'.")
                advance()
                args = [parse_expression_level()]
                while peek() == ",":
                    advance()
                    args.append(parse_expression_level())
                if peek() != ")":
                    raise ValueError("Unmatched parenthesis in expression.")
                advance()

                if tok == "logb":
                    if len(args) != 2:
                        raise ValueError("logb() requires exactly two arguments.")
                    return calculate_log(args[0], args[1])

                if tok == "pow":
                    if len(args) != 2:
                        raise ValueError("pow() requires exactly two arguments.")
                    return calculate_power(args[0], args[1])

                if len(args) != 1:
                    raise ValueError(tok + "() requires exactly one argument.")
                return apply_function(tok, args[0], mode)

            raise ValueError("Unknown identifier: " + tok)

        raise ValueError("Invalid token in expression.")

    result = parse_expression_level()

    if position[0] != len(tokens):
        raise ValueError("Unexpected token(s) at end of expression.")

    return float(result)
