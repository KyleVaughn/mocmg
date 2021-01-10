import logging
from unittest import TestCase

import gmsh
import pytest

import mocmg

from .testingUtils import captured_output


@pytest.mark.skip()
def testLogMessages(logger):
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")


referenceOut = ["INFO      : tests.test_initialize - Info message"]
referenceErr = [
    "WARNING   : tests.test_initialize - Warning message",
    "ERROR     : tests.test_initialize - Error message",
    "CRITICAL  : tests.test_initialize - Critical message",
]

# NOTE: line numbers correspond to the testLogMessages function.
referenceDebugOut = [
    "DEBUG     : tests.test_initialize - (line: 11) Debug message",
    "INFO      : tests.test_initialize - (line: 12) Info message",
]
referenceDebugErr = [
    "WARNING   : tests.test_initialize - (line: 13) Warning message",
    "ERROR     : tests.test_initialize - (line: 14) Error message",
    "CRITICAL  : tests.test_initialize - (line: 15) Critical message",
]


class test_initialize(TestCase):
    # Run with gmshOption='warning' or greater, otherwise gmsh will output
    # 'Info    : No current model available: creating one'
    # even though gmsh.finalize() has been called. Therefore, it is assumed that gmshOption is being set correctly

    def test_optionDefault(self):
        with captured_output() as (out, err):
            mocmg.initialize()
            gmshVerbosity = 5
            gmsh.initialize()
            gmsh.option.setNumber("General.Terminal", 1)
            gmsh.option.setNumber("General.Verbosity", gmshVerbosity)
            log = logging.getLogger(__name__)
            testLogMessages(log)
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out, err = [line.split(None, 1)[1] for line in out], [
            line.split(None, 1)[1] for line in err
        ]  # strip times
        self.assertEqual(out, referenceOut)
        self.assertEqual(err, referenceErr)
        self.assertEqual(gmsh.option.getNumber("General.Verbosity"), 5)
        mocmg.finalize()

    def test_optionDebug(self):
        with captured_output() as (out, err):
            mocmg.initialize(verbosity="debug")
            gmshVerbosity = 99
            gmsh.initialize()
            gmsh.option.setNumber("General.Terminal", 1)
            gmsh.option.setNumber("General.Verbosity", gmshVerbosity)

            log = logging.getLogger(__name__)
            testLogMessages(log)
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out, err = [line.split(None, 1)[1] for line in out], [
            line.split(None, 1)[1] for line in err
        ]  # strip times
        self.assertEqual(out, referenceDebugOut)
        self.assertEqual(err, referenceDebugErr)
        self.assertEqual(gmsh.option.getNumber("General.Verbosity"), 99)
        mocmg.finalize()

    def test_optionWarning(self):
        with captured_output() as (out, err):
            mocmg.initialize(verbosity="warning")
            gmshVerbosity = 2
            gmsh.initialize()
            gmsh.option.setNumber("General.Terminal", 1)
            gmsh.option.setNumber("General.Verbosity", gmshVerbosity)
            log = logging.getLogger(__name__)
            testLogMessages(log)
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out, err = [line.split(None, 1)[1] for line in out], [
            line.split(None, 1)[1] for line in err
        ]  # strip times
        self.assertEqual(out, [])
        self.assertEqual(err, referenceErr)
        self.assertEqual(gmsh.option.getNumber("General.Verbosity"), 2)
        mocmg.finalize()

    def test_optionError(self):
        with captured_output() as (out, err):
            mocmg.initialize(verbosity="error")
            gmshVerbosity = 1
            gmsh.initialize()
            gmsh.option.setNumber("General.Terminal", 1)
            gmsh.option.setNumber("General.Verbosity", gmshVerbosity)
            log = logging.getLogger(__name__)
            testLogMessages(log)
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out, err = [line.split(None, 1)[1] for line in out], [
            line.split(None, 1)[1] for line in err
        ]  # strip times
        self.assertEqual(out, [])
        self.assertEqual(err, referenceErr[1:])
        self.assertEqual(gmsh.option.getNumber("General.Verbosity"), 1)
        mocmg.finalize()

    def test_optionSilent(self):
        with captured_output() as (out, err):
            mocmg.initialize(verbosity="silent")
            gmshVerbosity = 0
            gmsh.initialize()
            gmsh.option.setNumber("General.Terminal", 1)
            gmsh.option.setNumber("General.Verbosity", gmshVerbosity)
            log = logging.getLogger(__name__)
            testLogMessages(log)
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out, err = [line.split(None, 1)[1] for line in out], [
            line.split(None, 1)[1] for line in err
        ]  # strip times
        self.assertEqual(out, [])
        self.assertEqual(err, [])
        self.assertEqual(gmsh.option.getNumber("General.Verbosity"), 0)
        mocmg.finalize()
