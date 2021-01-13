"""Functions to help with code testing."""
import subprocess
import sys
from contextlib import contextmanager
from io import StringIO


@contextmanager
def captured_output():
    """Capture stdout, stderr using StringIO.

    Example:
        with captured_output() as (out, err):
            some_function()
    """
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


def run_from_shell(cmd):
    """Run a command from shell, return stdout & stderr."""
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = proc.communicate()
    return stdout, stderr
