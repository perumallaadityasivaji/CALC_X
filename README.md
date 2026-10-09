# CALC-X — Advanced Terminal Calculator

A menu-driven, terminal-based mathematical calculator written in beginner-friendly,
procedural Python (no custom classes).

## How to Run

Requires Python 3. From inside the `CALC-X` folder:

```
python main.py
```

## Project Structure

```
CALC-X/
│
├── main.py         # Menu, navigation, and all module UI/interaction
├── calculator.py    # Expression validation, tokenizing, and evaluation (Basic + Scientific)
├── algebra.py        # Linear/quadratic equations, polynomial evaluation
├── equations.py       # Simultaneous 2x2 / 3x3 equation solving
├── matrix.py          # Matrix add/subtract/multiply/transpose/determinant/inverse
├── statistics.py       # Mean, median, mode, min, max, range, variance, std. deviation
├── calculus.py         # Polynomial differentiation and integration
├── history.py          # Calculation history: add, view, save, load, clear
└── README.md
```

## Main Menu

```
1. Basic Calculator
2. Scientific Calculator
3. Algebra Solver
4. Equation Solver
5. Matrix Operations
6. Statistics
7. Calculus
8. History
9. Exit
```

## Notes

- The expression evaluator does **not** use Python's `eval()`. Expressions are
  tokenized and evaluated manually via a recursive-descent parser that
  respects BODMAS (brackets → functions → powers → × ÷ % → + −).
- All modules handle invalid input gracefully and never crash the program;
  errors are reported and the user is returned to a prompt to try again.
- History currently records calculations made in the Basic and Scientific
  Calculator modules (see the Design Document's `main.py` function
  signatures — only `basic_calculator` and `scientific_calculator` accept
  a `history` list parameter, alongside `history_menu` itself).
