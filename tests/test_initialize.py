import logging
import mocmg
import sys
from contextlib import contextmanager
from io import StringIO
from nose.tools import nottest
from unittest import TestCase

@nottest
def testMessages(logger):
    logger.debug('Debug message')
    logger.info('Info message')
    logger.warning('Warning message')
    logger.error('Error message')
    logger.critical('Critical message')    

@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

referenceOut = ['INFO      : tests.test_initialize - Info message']
referenceErr = ['WARNING   : tests.test_initialize - Warning message', 
                'ERROR     : tests.test_initialize - Error message', 
                'CRITICAL  : tests.test_initialize - Critical message']

# NOTE: line numbers correspond to the testMessages function.
referenceDebugOut = ['DEBUG     : tests.test_initialize - (line: 11) Debug message',
                     'INFO      : tests.test_initialize - (line: 12) Info message']
referenceDebugErr = ['WARNING   : tests.test_initialize - (line: 13) Warning message', 
                     'ERROR     : tests.test_initialize - (line: 14) Error message', 
                     'CRITICAL  : tests.test_initialize - (line: 15) Critical message']

class test_initialize(TestCase):
    # Run with gmshOption='warning' or greater, otherwise gmsh will output
    # 'Info    : No current model available: creating one' 
    # even though gmsh.finalize() has been called. Therefore, it is assumed that gmshOption is being set correctly

    def test_mocmgOptionDefault(self):
        with captured_output() as (out,err):
            mocmg.initialize(gmshOption='warning')
            log = logging.getLogger(__name__)
            testMessages(log)
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines() 
        out, err = [l.split(None,1)[1] for l in out], [l.split(None,1)[1] for l in err] # strip times
        self.assertEqual(out, referenceOut)
        self.assertEqual(err, referenceErr)
        self.assertEqual(gmsh.getNumber('General.Verbosity'), 2)
        mocmg.finalize()

    def test_mocmgOptionDebug(self):
        with captured_output() as (out,err):
            mocmg.initialize(mocmgOption='debug', gmshOption='error')
            log = logging.getLogger(__name__)
            testMessages(log)
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines() 
        out, err = [l.split(None,1)[1] for l in out], [l.split(None,1)[1] for l in err] # strip times
        self.assertEqual(out, referenceDebugOut)
        self.assertEqual(err, referenceDebugErr)
        self.assertEqual(gmsh.getNumber('General.Verbosity'), 1)
        mocmg.finalize()

    def test_mocmgOptionWarning(self):
        with captured_output() as (out,err):
            mocmg.initialize(mocmgOption='warning', gmshOption='silent')
            log = logging.getLogger(__name__)
            testMessages(log)
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines() 
        out, err = [l.split(None,1)[1] for l in out], [l.split(None,1)[1] for l in err] # strip times
        self.assertEqual(out, [])
        self.assertEqual(err, referenceErr)
        self.assertEqual(gmsh.getNumber('General.Verbosity'), 0)
        mocmg.finalize()

    def test_mocmgOptionError(self):
        with captured_output() as (out,err):
            # Defaults = logging.INFO, gmsh=5=info, color=True
            mocmg.initialize(mocmgOption='error', gmshOption='warning')
            log = logging.getLogger(__name__)
            testMessages(log)
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines() 
        out, err = [l.split(None,1)[1] for l in out], [l.split(None,1)[1] for l in err] # strip times
        self.assertEqual(out, [])
        self.assertEqual(err, referenceErr[1:])
        mocmg.finalize()
