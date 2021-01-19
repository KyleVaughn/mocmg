"""Test the initialize function."""
import logging
from unittest import TestCase

import pytest

import mocmg

from .testing_utils import captured_output


def _test_log_messages(logger):
    """Produce messages at each log level."""
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.require(True, "Condition met")
    logger.require(False, "Condition not met")
    logger.critical("Critical message")


# Expected output for stdout and stderr when NOT in debug mode
reference_out = ["INFO      : tests.test_initialize - Info message"]
reference_err = [
    "WARNING   : tests.test_initialize - Warning message",
    "ERROR     : tests.test_initialize - Error message",
    "ERROR     : tests.test_initialize - Condition not met",
    "CRITICAL  : tests.test_initialize - Critical message",
]

# Expected output for stdout and stderr when in debug mode
# NOTE: line numbers correspond to the _test_log_messages function, except for require,
# which corresponds tothe self.log call in the "require" function in initialize.py.
reference_debug_out = [
    "DEBUG     : tests.test_initialize - (line: 14) Debug message",
    "INFO      : tests.test_initialize - (line: 15) Info message",
]
reference_debug_err = [
    "WARNING   : tests.test_initialize - (line: 16) Warning message",
    "ERROR     : tests.test_initialize - (line: 17) Error message",
    "ERROR     : tests.test_initialize - (line: 117) Condition not met",
    "CRITICAL  : tests.test_initialize - (line: 20) Critical message",
]

# Expected warning when given a bad value for the verbosity
# Note the work "Next" is ommited from the second string simply for ease of testing
badvalue_err = [
    "WARNING   : mocmg.initialize - Invalid verbosity option 'badvalue'. Defaulting to 'info'.",
    "time please choose from one of: 'silent', 'error', 'warning', 'info', or 'debug'",
]

# Expected error for the "require" log level given a non-bool condition argument
require_err = [
    "ERROR     : mocmg.initialize - In requre(condition, message), 'condition' argument must be bool.",
]


class TestInitialize(TestCase):
    """Test the initialize function.

    Tests the following initialize arguments:

    - initialize()
    - initialize(verbosity="debug")
    - initialize(verbosity="warning")
    - initialize(verbosity="error")
    - initialize(verbosity="silent")
    - initialize(verbosity="badvalue"), expect warning

    color
    """

    def test_verbosity_default(self):
        """Test the default initialize options."""
        with captured_output() as (out, err):
            mocmg.initialize(exit_on_error=False)
            log = logging.getLogger(__name__)
            _test_log_messages(log)
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out, err = [line.split(None, 1)[1] for line in out], [
            line.split(None, 1)[1] for line in err
        ]  # strip times
        self.assertEqual(out, reference_out)
        self.assertEqual(err, reference_err)
        # check log file
        f = open("mocmg.log", "r")
        lines = f.readlines()
        f.close()
        lines = [line.split(None, 1)[1].rstrip("\n") for line in lines]
        self.assertEqual(reference_out + reference_err, lines)

    def test_verbosity_info(self):
        """Test verbosity='info'."""
        with captured_output() as (out, err):
            mocmg.initialize(verbosity="info", exit_on_error=False)
            log = logging.getLogger(__name__)
            _test_log_messages(log)
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out, err = [line.split(None, 1)[1] for line in out], [
            line.split(None, 1)[1] for line in err
        ]  # strip times
        self.assertEqual(out, reference_out)
        self.assertEqual(err, reference_err)
        # check log file
        f = open("mocmg.log", "r")
        lines = f.readlines()
        f.close()
        lines = [line.split(None, 1)[1].rstrip("\n") for line in lines]
        self.assertEqual(out + err, lines)

    def test_verbosity_debug(self):
        """Test verbosity='debug'."""
        with captured_output() as (out, err):
            mocmg.initialize(verbosity="debug", exit_on_error=False)
            log = logging.getLogger(__name__)
            _test_log_messages(log)
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out, err = [line.split(None, 1)[1] for line in out], [
            line.split(None, 1)[1] for line in err
        ]  # strip times
        self.assertEqual(out, reference_debug_out)
        self.assertEqual(err, reference_debug_err)
        # check log file
        f = open("mocmg.log", "r")
        lines = f.readlines()
        f.close()
        lines = [line.split(None, 1)[1].rstrip("\n") for line in lines]
        self.assertEqual(reference_debug_out + reference_debug_err, lines)

    def test_verbosity_warning(self):
        """Test verbosity='warning'."""
        with captured_output() as (out, err):
            mocmg.initialize(verbosity="warning", exit_on_error=False)
            log = logging.getLogger(__name__)
            _test_log_messages(log)
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out, err = [line.split(None, 1)[1] for line in out], [
            line.split(None, 1)[1] for line in err
        ]  # strip times
        self.assertEqual(out, [])
        self.assertEqual(err, reference_err)
        # check log file
        f = open("mocmg.log", "r")
        lines = f.readlines()
        f.close()
        lines = [line.split(None, 1)[1].rstrip("\n") for line in lines]
        self.assertEqual(reference_err, lines)

    def test_verbosity_error(self):
        """Test verbosity='error'."""
        with captured_output() as (out, err):
            mocmg.initialize(verbosity="error", exit_on_error=False)
            log = logging.getLogger(__name__)
            _test_log_messages(log)
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out, err = [line.split(None, 1)[1] for line in out], [
            line.split(None, 1)[1] for line in err
        ]  # strip times
        self.assertEqual(out, [])
        self.assertEqual(err, reference_err[1:])
        # check log file
        f = open("mocmg.log", "r")
        lines = f.readlines()
        f.close()
        lines = [line.split(None, 1)[1].rstrip("\n") for line in lines]
        self.assertEqual(reference_err[1:], lines)

    def test_verbosity_silent(self):
        """Test verbosity='silent'."""
        with captured_output() as (out, err):
            mocmg.initialize(verbosity="silent", exit_on_error=False)
            log = logging.getLogger(__name__)
            _test_log_messages(log)
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out, err = [line.split(None, 1)[1] for line in out], [
            line.split(None, 1)[1] for line in err
        ]  # strip times
        self.assertEqual(out, [])
        self.assertEqual(err, [])
        # check log file
        f = open("mocmg.log", "r")
        lines = f.readlines()
        f.close()
        lines = [line.split(None, 1)[1].rstrip("\n") for line in lines]
        self.assertEqual([], lines)

    def test_verbosity_badvalue(self):
        """Test verbosity='badvalue'."""
        with captured_output() as (out, err):
            mocmg.initialize(verbosity="badvalue", exit_on_error=False)
            log = logging.getLogger(__name__)
            _test_log_messages(log)
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out, err = [line.split(None, 1)[1] for line in out], [
            line.split(None, 1)[1] for line in err
        ]  # strip times
        self.assertEqual(out, reference_out)
        self.assertEqual(err, badvalue_err + reference_err)
        # check log file
        f = open("mocmg.log", "r")
        lines = f.readlines()
        f.close()
        lines = [line.split(None, 1)[1].rstrip("\n") for line in lines]
        self.assertEqual(badvalue_err + reference_out + reference_err, lines)

    def test_exit_on_error_true(self):
        """Test exit_on_error=True."""
        with pytest.raises(SystemExit):
            with captured_output() as (out, err):
                mocmg.initialize(exit_on_error=True)
                log = logging.getLogger(__name__)
                log.debug("Debug message")
                log.info("Info message")
                log.warning("Warning message")
                log.error("Error message")
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out = [line.split(None, 1)[1] for line in out]
        err = [line.split(None, 1)[1] for line in err[0:2]]  # strip times
        self.assertEqual(out, reference_out)
        self.assertEqual(err, reference_err[0:2])
        # check log file
        f = open("mocmg.log", "r")
        lines = f.readlines()
        f.close()
        lines = [line.split(None, 1)[1].rstrip("\n") for line in lines]
        self.assertEqual(reference_out + reference_err[0:2], lines)

    def test_require_exit_on_error_true(self):
        """Test the "require" log level with exit_on_error=True."""
        with pytest.raises(SystemExit):
            with captured_output() as (out, err):
                mocmg.initialize(exit_on_error=True)
                log = logging.getLogger(__name__)
                log.debug("Debug message")
                log.info("Info message")
                log.warning("Warning message")
                log.require(True, "Condition met")
                log.require(False, "Condition not met")
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out = [line.split(None, 1)[1] for line in out]
        err = [line.split(None, 1)[1] for line in err[0:2]]  # strip times
        self.assertEqual(out, reference_out)
        self.assertEqual(err, [reference_err[0], reference_err[2]])
        # check log file
        f = open("mocmg.log", "r")
        lines = f.readlines()
        f.close()
        lines = [line.split(None, 1)[1].rstrip("\n") for line in lines]
        self.assertEqual(reference_out + [reference_err[0], reference_err[2]], lines)

    def test_require_condition_not_bool(self):
        """Test the "require" log level with not isinstance(condition, bool)."""
        with pytest.raises(SystemExit):
            with captured_output() as (out, err):
                mocmg.initialize(exit_on_error=True)
                log = logging.getLogger(__name__)
                log.debug("Debug message")
                log.info("Info message")
                log.warning("Warning message")
                log.require("not a bool", "Condition met")
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out = [line.split(None, 1)[1] for line in out]
        err = [line.split(None, 1)[1] for line in err[0:2]]  # strip times
        self.assertEqual(out, reference_out)
        self.assertEqual(err, [reference_err[0], require_err[0]])
        # check log file
        f = open("mocmg.log", "r")
        lines = f.readlines()
        f.close()
        lines = [line.split(None, 1)[1].rstrip("\n") for line in lines]
        self.assertEqual(reference_out + [reference_err[0], require_err[0]], lines)

    def test_double_init(self):
        """Test behavior if initialize is called twice."""
        with captured_output() as (out, err):
            mocmg.initialize(exit_on_error=False)
            mocmg.initialize(exit_on_error=False)
            log = logging.getLogger(__name__)
            _test_log_messages(log)
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out, err = [line.split(None, 1)[1] for line in out], [
            line.split(None, 1)[1] for line in err
        ]  # strip times
        self.assertEqual(out, reference_out)
        self.assertEqual(err, reference_err)
        # check log file
        f = open("mocmg.log", "r")
        lines = f.readlines()
        f.close()
        lines = [line.split(None, 1)[1].rstrip("\n") for line in lines]
        self.assertEqual(reference_out + reference_err, lines)
