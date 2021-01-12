"""Test the initialize function."""
import logging
from unittest import TestCase

import mocmg

from .testingUtils import captured_output


def _test_log_messages(logger):
    """Produce messages at each log level."""
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")


# Expected output for stdout and stderr when NOT in debug mode
reference_out = ["INFO      : tests.test_initialize - Info message"]
reference_err = [
    "WARNING   : tests.test_initialize - Warning message",
    "ERROR     : tests.test_initialize - Error message",
    "CRITICAL  : tests.test_initialize - Critical message",
]

# Expected output for stdout and stderr when in debug mode
# NOTE: line numbers correspond to the _test_log_messages function.
reference_debug_out = [
    "DEBUG     : tests.test_initialize - (line: 12) Debug message",
    "INFO      : tests.test_initialize - (line: 13) Info message",
]
reference_debug_err = [
    "WARNING   : tests.test_initialize - (line: 14) Warning message",
    "ERROR     : tests.test_initialize - (line: 15) Error message",
    "CRITICAL  : tests.test_initialize - (line: 16) Critical message",
]

# Expected output when given a bad value for the verbosity
badvalue_err = [
    "Invalid verbosity option 'badvalue'. Defaulting to 'info'. Next time please choose "
    + "from one of: 'silent', 'error', 'warning', 'info', or 'debug'",
    "WARNING   : tests.test_initialize - Warning message",
    "ERROR     : tests.test_initialize - Error message",
    "CRITICAL  : tests.test_initialize - Critical message",
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
            mocmg.initialize()
            log = logging.getLogger(__name__)
            _test_log_messages(log)
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out, err = [line.split(None, 1)[1] for line in out], [
            line.split(None, 1)[1] for line in err
        ]  # strip times
        self.assertEqual(out, reference_out)
        self.assertEqual(err, reference_err)

    def test_verbosity_info(self):
        """Test verbosity='info'."""
        with captured_output() as (out, err):
            mocmg.initialize(verbosity="info")
            log = logging.getLogger(__name__)
            _test_log_messages(log)
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out, err = [line.split(None, 1)[1] for line in out], [
            line.split(None, 1)[1] for line in err
        ]  # strip times
        self.assertEqual(out, reference_out)
        self.assertEqual(err, reference_err)

    def test_verbosity_debug(self):
        """Test verbosity='debug'."""
        with captured_output() as (out, err):
            mocmg.initialize(verbosity="debug")
            log = logging.getLogger(__name__)
            _test_log_messages(log)
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out, err = [line.split(None, 1)[1] for line in out], [
            line.split(None, 1)[1] for line in err
        ]  # strip times
        self.assertEqual(out, reference_debug_out)
        self.assertEqual(err, reference_debug_err)

    def test_verbosity_warning(self):
        """Test verbosity='warning'."""
        with captured_output() as (out, err):
            mocmg.initialize(verbosity="warning")
            log = logging.getLogger(__name__)
            _test_log_messages(log)
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out, err = [line.split(None, 1)[1] for line in out], [
            line.split(None, 1)[1] for line in err
        ]  # strip times
        self.assertEqual(out, [])
        self.assertEqual(err, reference_err)

    def test_verbosity_error(self):
        """Test verbosity='error'."""
        with captured_output() as (out, err):
            mocmg.initialize(verbosity="error")
            log = logging.getLogger(__name__)
            _test_log_messages(log)
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out, err = [line.split(None, 1)[1] for line in out], [
            line.split(None, 1)[1] for line in err
        ]  # strip times
        self.assertEqual(out, [])
        self.assertEqual(err, reference_err[1:])

    def test_verbosity_silent(self):
        """Test verbosity='silent'."""
        with captured_output() as (out, err):
            mocmg.initialize(verbosity="silent")
            log = logging.getLogger(__name__)
            _test_log_messages(log)
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out, err = [line.split(None, 1)[1] for line in out], [
            line.split(None, 1)[1] for line in err
        ]  # strip times
        self.assertEqual(out, [])
        self.assertEqual(err, [])

    def test_verbosity_badvalue(self):
        """Test verbosity='badvalue'."""
        with captured_output() as (out, err):
            mocmg.initialize(verbosity="badvalue")
            log = logging.getLogger(__name__)
            _test_log_messages(log)
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out, err = [line.split(None, 1)[1] for line in out], [
            line.split(None, 1)[1] for line in err
        ]  # strip times
        self.assertEqual(out, reference_out)
        self.assertEqual(err, badvalue_err)
