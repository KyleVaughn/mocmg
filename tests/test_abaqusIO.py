import mocmg
import logging
import sys
from contextlib import contextmanager
from io import StringIO
from unittest import TestCase

@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

class test_abaqusIO(TestCase):

    def test_readINP(self):
        # Caputure output since bb will throw warning on purpose
        with captured_output() as (out,err):
            mocmg.initialize(mocmgOption='warning', gmshOption='silent')
            self.assertAlmostEqual(3.5, x, places=5)
            self.assertAlmostEqual(1.5, y, places=5)
            self.assertAlmostEqual(0.0, z, places=5)
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out, err = [l.split(None,1)[1] for l in out], [l.split(None,1)[1] for l in err] # strip times
        self.assertEqual(out, [])
        err_ref = 'WARNING   : mocmg.generateRectGrid - Model thickness is 1.000000 > 1e-6.' +\
                ' Model expected in 2D x-y plane.'
        self.assertEqual(err[0], err_ref)
        mocmg.finalize()
