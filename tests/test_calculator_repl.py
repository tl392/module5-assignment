# tests/test_calculator_repl.py

import pytest
from decimal import Decimal

import app.calculator_repl as repl
from app.calculator import Calculator
from app.exceptions import OperationError, ValidationError


def _feed_inputs(monkeypatch, seq):
    """
    Feed a sequence of inputs to builtins.input. When exhausted, raise EOFError.
    """
    it = iter(seq)

    def fake_input(_prompt=""):
        try:
            return next(it)
        except StopIteration:
            raise EOFError

    monkeypatch.setattr("builtins.input", fake_input)


def _make_real_calculator(monkeypatch, tmp_path):
    """
    Create a REAL Calculator configured to write only inside tmp_path.
    Also disables auto-save to avoid extra file writes during tests.
    """
    monkeypatch.setenv("CALCULATOR_BASE_DIR", str(tmp_path))
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "false")
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "100")

    return Calculator()


def test_help_then_exit_saves_history(monkeypatch, tmp_path, capsys):
    calc = _make_real_calculator(monkeypatch, tmp_path)
    monkeypatch.setattr(repl, "Calculator", lambda: calc)

    _feed_inputs(monkeypatch, ["help", "exit"])

    repl.calculator_repl()

    out = capsys.readouterr().out
    assert "Calculator started" in out
    assert "Available commands:" in out
    assert "History saved successfully." in out
    assert "Goodbye!" in out


def test_exit_save_warning_when_save_fails(monkeypatch, tmp_path, capsys):
    calc = _make_real_calculator(monkeypatch, tmp_path)
    monkeypatch.setattr(repl, "Calculator", lambda: calc)

    def boom():
        raise RuntimeError("disk full")

    monkeypatch.setattr(calc, "save_history", boom)

    _feed_inputs(monkeypatch, ["exit"])
    repl.calculator_repl()

    out = capsys.readouterr().out
    assert "Warning: Could not save history" in out
    assert "Goodbye!" in out


def test_add_then_history_lists_entry(monkeypatch, tmp_path, capsys):
    calc = _make_real_calculator(monkeypatch, tmp_path)
    monkeypatch.setattr(repl, "Calculator", lambda: calc)

    _feed_inputs(monkeypatch, ["add", "1", "1", "history", "exit"])
    repl.calculator_repl()

    out = capsys.readouterr().out
    assert "Result:" in out
    assert "Calculation History:" in out
    assert "1." in out  # numbered entry


def test_clear_then_history_empty(monkeypatch, tmp_path, capsys):
    calc = _make_real_calculator(monkeypatch, tmp_path)
    monkeypatch.setattr(repl, "Calculator", lambda: calc)

    _feed_inputs(monkeypatch, ["add", "2", "3", "clear", "history", "exit"])
    repl.calculator_repl()

    out = capsys.readouterr().out
    assert "History cleared" in out
    assert "No calculations in history" in out


def test_undo_redo_paths_true_and_false(monkeypatch, tmp_path, capsys):
    calc = _make_real_calculator(monkeypatch, tmp_path)
    monkeypatch.setattr(repl, "Calculator", lambda: calc)

    # First undo/redo should be "Nothing ..." (no operations yet)
    # After an add, undo and redo should succeed.
    _feed_inputs(monkeypatch, ["undo", "redo", "add", "5", "6", "undo", "redo", "exit"])
    repl.calculator_repl()

    out = capsys.readouterr().out
    assert "Nothing to undo" in out
    assert "Nothing to redo" in out
    assert "Operation undone" in out
    assert "Operation redone" in out


def test_save_and_load_success(monkeypatch, tmp_path, capsys):
    calc = _make_real_calculator(monkeypatch, tmp_path)
    monkeypatch.setattr(repl, "Calculator", lambda: calc)

    _feed_inputs(monkeypatch, ["add", "10", "2", "save", "load", "exit"])
    repl.calculator_repl()

    out = capsys.readouterr().out
    assert "History saved successfully" in out  # from save command
    assert "History loaded successfully" in out


def test_save_and_load_fail(monkeypatch, tmp_path, capsys):
    calc = _make_real_calculator(monkeypatch, tmp_path)
    monkeypatch.setattr(repl, "Calculator", lambda: calc)

    monkeypatch.setattr(calc, "save_history", lambda: (_ for _ in ()).throw(RuntimeError("no perms")))
    monkeypatch.setattr(calc, "load_history", lambda: (_ for _ in ()).throw(RuntimeError("bad csv")))

    _feed_inputs(monkeypatch, ["save", "load", "exit"])
    repl.calculator_repl()

    out = capsys.readouterr().out
    assert "Error saving history:" in out
    assert "Error loading history:" in out


def test_operation_cancel_paths(monkeypatch, tmp_path, capsys):
    calc = _make_real_calculator(monkeypatch, tmp_path)
    monkeypatch.setattr(repl, "Calculator", lambda: calc)

    _feed_inputs(monkeypatch, ["add", "cancel", "add", "1", "cancel", "exit"])
    repl.calculator_repl()

    out = capsys.readouterr().out
    assert out.count("Operation cancelled") >= 2


def test_operation_known_errors_validation_and_operation(monkeypatch, tmp_path, capsys):
    calc = _make_real_calculator(monkeypatch, tmp_path)
    monkeypatch.setattr(repl, "Calculator", lambda: calc)

    # Force ValidationError from real calculator method
    def raise_validation(_a, _b):
        raise ValidationError("bad input")

    monkeypatch.setattr(calc, "perform_operation", raise_validation)
    _feed_inputs(monkeypatch, ["add", "1", "2", "exit"])
    repl.calculator_repl()
    out1 = capsys.readouterr().out
    assert "Error: bad input" in out1

    # Force OperationError
    calc2 = _make_real_calculator(monkeypatch, tmp_path)
    monkeypatch.setattr(repl, "Calculator", lambda: calc2)

    def raise_operation(_a, _b):
        raise OperationError("op failed")

    monkeypatch.setattr(calc2, "perform_operation", raise_operation)
    _feed_inputs(monkeypatch, ["add", "1", "2", "exit"])
    repl.calculator_repl()
    out2 = capsys.readouterr().out
    assert "Error: op failed" in out2


def test_operation_unexpected_error(monkeypatch, tmp_path, capsys):
    calc = _make_real_calculator(monkeypatch, tmp_path)
    monkeypatch.setattr(repl, "Calculator", lambda: calc)

    monkeypatch.setattr(calc, "perform_operation", lambda _a, _b: (_ for _ in ()).throw(RuntimeError("boom")))

    _feed_inputs(monkeypatch, ["add", "1", "2", "exit"])
    repl.calculator_repl()

    out = capsys.readouterr().out
    assert "Unexpected error: boom" in out


def test_unknown_command(monkeypatch, tmp_path, capsys):
    calc = _make_real_calculator(monkeypatch, tmp_path)
    monkeypatch.setattr(repl, "Calculator", lambda: calc)

    _feed_inputs(monkeypatch, ["wat", "exit"])
    repl.calculator_repl()

    out = capsys.readouterr().out
    assert "Unknown command: 'wat'" in out


def test_keyboardinterrupt_is_handled(monkeypatch, tmp_path, capsys):
    calc = _make_real_calculator(monkeypatch, tmp_path)
    monkeypatch.setattr(repl, "Calculator", lambda: calc)

    calls = {"n": 0}

    def fake_input(_prompt=""):
        calls["n"] += 1
        if calls["n"] == 1:
            raise KeyboardInterrupt
        return "exit"

    monkeypatch.setattr("builtins.input", fake_input)

    repl.calculator_repl()

    out = capsys.readouterr().out
    assert "Operation cancelled" in out
    assert "Goodbye!" in out


def test_eoferror_exits_cleanly(monkeypatch, tmp_path, capsys):
    calc = _make_real_calculator(monkeypatch, tmp_path)
    monkeypatch.setattr(repl, "Calculator", lambda: calc)

    def fake_input(_prompt=""):
        raise EOFError

    monkeypatch.setattr("builtins.input", fake_input)

    repl.calculator_repl()

    out = capsys.readouterr().out
    assert "Input terminated. Exiting..." in out


def test_inner_loop_generic_exception_branch(monkeypatch, tmp_path, capsys):
    calc = _make_real_calculator(monkeypatch, tmp_path)
    monkeypatch.setattr(repl, "Calculator", lambda: calc)

    # Make input raise a generic exception once, then exit.
    calls = {"n": 0}

    def fake_input(_prompt=""):
        calls["n"] += 1
        if calls["n"] == 1:
            raise RuntimeError("weird")
        return "exit"

    monkeypatch.setattr("builtins.input", fake_input)

    repl.calculator_repl()

    out = capsys.readouterr().out
    assert "Error: weird" in out
    assert "Goodbye!" in out


def test_fatal_init_error_is_raised(monkeypatch, capsys):
    # Force Calculator() to fail during init
    monkeypatch.setattr(repl, "Calculator", lambda: (_ for _ in ()).throw(RuntimeError("init failed")))

    with pytest.raises(RuntimeError):
        repl.calculator_repl()

    out = capsys.readouterr().out
    assert "Fatal error: init failed" in out

def test_history_empty_then_exit(monkeypatch, tmp_path, capsys):
    # real calculator
    monkeypatch.setenv("CALCULATOR_BASE_DIR", str(tmp_path))
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "false")

    calc = Calculator()
    monkeypatch.setattr(repl, "Calculator", lambda: calc)

    # force empty history branch (still using real Calculator instance)
    monkeypatch.setattr(calc, "show_history", lambda: [])

    _feed_inputs(monkeypatch, ["history", "exit"])
    repl.calculator_repl()

    out = capsys.readouterr().out
    assert "No calculations in history" in out  # exact text from your REPL
    assert "Goodbye!" in out