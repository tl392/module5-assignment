"""
Application entry point for the CLI Calculator.

This file exists so the program can be started with:

    python main.py

instead of:

    python -m app.calculator
"""

from app.calculator import Calculator


def main() -> None:
    """Start the calculator REPL."""
    Calculator().repl()


if __name__ == "__main__":
    main()
