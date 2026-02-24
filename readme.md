# Module 5 - Advanced Python Calculator (CLI Application)

## Project Overview

This project is a professional command-line calculator application built
using Python. It demonstrates advanced object-oriented programming
(OOP), modular architecture, command-based design patterns, logging,
file handling, history management, undo/redo functionality, and
comprehensive automated testing.

The structure follows real-world software engineering practices and is
designed to be scalable and maintainable.

------------------------------------------------------------------------

## Available Commands

### Arithmetic Operations

-   add -- Perform addition
-   subtract -- Perform subtraction
-   multiply -- Perform multiplication
-   divide -- Perform division
-   power -- Raise a number to a power
-   root -- Calculate square root (or nth root if implemented)

### History Management

-   history -- Show calculation history
-   clear -- Clear calculation history
-   undo -- Undo the last calculation
-   redo -- Redo the last undone calculation

### File Operations

-   save -- Save calculation history to a file
-   load -- Load calculation history from a file

### System Command

-   exit -- Exit the calculator

------------------------------------------------------------------------

## Key Features

-   Command-driven REPL (Read--Eval--Print Loop)
-   Object-oriented implementation of operations
-   Encapsulation of business logic
-   History tracking with undo/redo stack
-   Persistent storage using file handling
-   Error handling for invalid inputs and edge cases
-   Logging for debugging and monitoring
-   Automated unit testing with high coverage

------------------------------------------------------------------------

## Project Structure

app/ calculator.py repl.py history.py commands/ add.py subtract.py
multiply.py divide.py power.py root.py

tests/ test_calculator.py test_commands.py test_history.py test_repl.py

main.py requirements.txt README.md

------------------------------------------------------------------------

## Installation

1.  Clone the repository:

    git clone https://github.com/your-username/module5_is601.git

2.  Navigate into the folder:

    cd module5_is601

3.  Create virtual environment:

    python -m venv venv

4.  Activate virtual environment:

    Windows: venv`\Scripts`{=tex}`\activate`{=tex}

    macOS/Linux: source venv/bin/activate

5.  Install dependencies:

    pip install -r requirements.txt

------------------------------------------------------------------------

## Running the Application

Start the calculator:

    python main.py

Enter a command followed by required numbers. Type exit to close the
application.

------------------------------------------------------------------------

## Running Tests

Run all tests:

    pytest

Run with coverage:

    pytest --cov=app --cov-report=term-missing

------------------------------------------------------------------------

## Git Workflow

Initialize repository:

    git init

Stage files:

    git add .

Commit:

    git commit -m "Initial commit"

Add remote:

    git remote add origin https://github.com/your-username/module5_is601.git

Push:

    git branch -M main
    git push -u origin main

------------------------------------------------------------------------

## Learning Outcomes

-   Applying advanced OOP principles in real applications
-   Implementing command pattern concepts
-   Managing state with undo/redo mechanisms
-   File persistence handling
-   Writing maintainable and testable Python code
-   Achieving high test coverage using pytest

------------------------------------------------------------------------

This project demonstrates how to build a feature-rich CLI application
using professional development standards while remaining clear and
structured.
