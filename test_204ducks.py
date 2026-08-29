"""
Automated test suite for 204ducks (rubber duck return-time distribution
model, numerically integrated via the trapezoidal rule).

Invokes the script as a subprocess, exactly as a real user would run it,
and asserts on stdout / exit code.
"""
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent / "204ducks"


def run(*args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
    )


# ---------------------------------------------------------------------------
# Help / usage
# ---------------------------------------------------------------------------

def test_help_flag_prints_usage_and_exits_zero():
    result = run("-h")
    assert result.returncode == 0
    assert "USAGE" in result.stderr


# ---------------------------------------------------------------------------
# Documented happy-path examples (straight from the README)
# ---------------------------------------------------------------------------

def test_readme_example_a_1_6():
    result = run("1.6")
    assert result.returncode == 0
    out = result.stdout
    assert "Average return time: 1m 21s" in out
    assert "Standard deviation: 1.074" in out
    assert "Time after which 50% of the ducks are back: 1m 04s" in out
    assert "Time after which 99% of the ducks are back: 5m 04s" in out
    assert "Percentage of ducks back after 1 minute: 46.9%" in out
    assert "Percentage of ducks back after 2 minutes: 79.1%" in out


def test_readme_example_a_0_2():
    result = run("0.2")
    assert result.returncode == 0
    out = result.stdout
    assert "Average return time: 0m 50s" in out
    assert "Standard deviation: 0.676" in out
    assert "Time after which 50% of the ducks are back: 0m 39s" in out
    assert "Time after which 99% of the ducks are back: 3m 16s" in out
    assert "Percentage of ducks back after 1 minute: 71.3%" in out
    assert "Percentage of ducks back after 2 minutes: 94.2%" in out


# ---------------------------------------------------------------------------
# Edge cases: boundary values
# ---------------------------------------------------------------------------

def test_boundary_a_zero_is_accepted():
    result = run("0")
    assert result.returncode == 0
    assert "Average return time" in result.stdout


def test_boundary_a_two_point_five_is_accepted():
    result = run("2.5")
    assert result.returncode == 0
    assert "Average return time" in result.stdout


def test_just_above_upper_boundary_is_rejected():
    result = run("2.500001")
    assert result.returncode == 84


def test_just_below_lower_boundary_is_rejected():
    result = run("-0.000001")
    assert result.returncode == 84


# ---------------------------------------------------------------------------
# Bad input: should fail gracefully (exit 84), never an unhandled traceback
# ---------------------------------------------------------------------------

def test_out_of_range_value_fails_gracefully():
    result = run("2.6")
    assert result.returncode == 84
    assert "Traceback" not in result.stderr


def test_negative_value_fails_gracefully():
    result = run("-1")
    assert result.returncode == 84
    assert "Traceback" not in result.stderr


def test_non_numeric_value_fails_gracefully():
    result = run("abc")
    assert result.returncode == 84
    assert "Traceback" not in result.stderr


def test_no_arguments_fail_gracefully():
    result = run()
    assert result.returncode == 84
    assert "Traceback" not in result.stderr


def test_too_many_arguments_fail_gracefully():
    result = run("1", "2")
    assert result.returncode == 84
    assert "Traceback" not in result.stderr
