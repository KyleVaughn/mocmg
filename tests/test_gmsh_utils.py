"""Test the rectangular grid function."""
from unittest import TestCase

import gmsh
import pytest

import mocmg
from mocmg.gmsh_utils import rectangular_grid

from .testing_utils import captured_output

bb_11 = [0.0, 0.0, 0.0, 1.0, 1.0, 0.0]
bb_dz = [0.0, 0.0, 0.0, 1.0, 1.0, 10.0]

# Expected output for generating rectangular grid
reference_out = [
    "INFO      : mocmg.gmsh_utils - Generating rectangular grid",
]


# Expected error for argument of incorrect type
bad_type = [
    "ERROR     : mocmg.gmsh_utils - Arguments should be list type.",
]


# Expected error for mismatch of x and y size
len_mismatch = [
    "ERROR     : mocmg.gmsh_utils - Length of arguments differ (2 and 1). "
    + "They should have the same number of levels.",
]

# Expected error for too many arguments
num_args = [
    "ERROR     : mocmg.gmsh_utils - Incorrect number of arguments given."
    + " Provide one of (x or nx) and one of (ny or y).",
]

# Expected error for overly thick model
thick_dz = [
    "ERROR     : mocmg.gmsh_utils - Bounding box thickness is greater than 1e-6"
    + " (10.000000). Bounding box expected in 2D x-y plane.",
]


class TestRectangularGrid(TestCase):
    """Test the gmsh_utils.rectangular_grid function."""

    def test_bad_arg_type(self):
        """Test rect grid with non-list args."""
        with pytest.raises(SystemExit):
            with captured_output() as (out, err):
                mocmg.initialize(exit_on_error=True)
                gmsh.initialize()
                rectangular_grid(bb_11, x=[[0.5]], y=[[0.5]], nx=4)
                gmsh.clear()
                gmsh.finalize()
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out = [line.split(None, 1)[1] for line in out]
        err = [line.split(None, 1)[1] for line in [err[0]]]  # strip times
        self.assertEqual(out, reference_out)
        self.assertEqual(err, bad_type)
        # check log file
        f = open("mocmg.log", "r")
        lines = f.readlines()
        f.close()
        lines = [line.split(None, 1)[1].rstrip("\n") for line in lines]
        self.assertEqual(lines, reference_out + bad_type)

    def test_too_many_args(self):
        """Test rect grid with too many args."""
        with pytest.raises(SystemExit):
            with captured_output() as (out, err):
                mocmg.initialize(exit_on_error=True)
                gmsh.initialize()
                rectangular_grid(bb_11, x=[[0.5]], y=[[0.5]], nx=[4])
                gmsh.clear()
                gmsh.finalize()
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out = [line.split(None, 1)[1] for line in out]
        err = [line.split(None, 1)[1] for line in [err[0]]]  # strip times
        self.assertEqual(out, reference_out)
        self.assertEqual(err, num_args)
        # check log file
        f = open("mocmg.log", "r")
        lines = f.readlines()
        f.close()
        lines = [line.split(None, 1)[1].rstrip("\n") for line in lines]
        self.assertEqual(lines, reference_out + num_args)

    def test_too_few_args(self):
        """Test rect grid with too few args."""
        with pytest.raises(SystemExit):
            with captured_output() as (out, err):
                mocmg.initialize(exit_on_error=True)
                gmsh.initialize()
                rectangular_grid(bb_11, x=[[0.5]])
                gmsh.clear()
                gmsh.finalize()
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out = [line.split(None, 1)[1] for line in out]
        err = [line.split(None, 1)[1] for line in [err[0]]]  # strip times
        self.assertEqual(out, reference_out)
        self.assertEqual(err, num_args)
        # check log file
        f = open("mocmg.log", "r")
        lines = f.readlines()
        f.close()
        lines = [line.split(None, 1)[1].rstrip("\n") for line in lines]
        self.assertEqual(lines, reference_out + num_args)

    def test_arg_len_mismatch(self):
        """Test rect grid with mismatched arg len."""
        with pytest.raises(SystemExit):
            with captured_output() as (out, err):
                mocmg.initialize(exit_on_error=True)
                gmsh.initialize()
                rectangular_grid(bb_11, x=[[0.5], [0.25]], y=[[0.5]])
                gmsh.clear()
                gmsh.finalize()
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out = [line.split(None, 1)[1] for line in out]
        err = [line.split(None, 1)[1] for line in [err[0]]]  # strip times
        self.assertEqual(out, reference_out)
        self.assertEqual(err, len_mismatch)
        # check log file
        f = open("mocmg.log", "r")
        lines = f.readlines()
        f.close()
        lines = [line.split(None, 1)[1].rstrip("\n") for line in lines]
        self.assertEqual(lines, reference_out + len_mismatch)

    def test_thick_dz(self):
        """Test rect grid with large change in z direction."""
        with pytest.raises(SystemExit):
            with captured_output() as (out, err):
                mocmg.initialize(exit_on_error=True)
                gmsh.initialize()
                rectangular_grid(bb_dz, x=[[0.5]], y=[[0.5]])
                gmsh.clear()
                gmsh.finalize()
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out = [line.split(None, 1)[1] for line in out]
        err = [line.split(None, 1)[1] for line in [err[0]]]  # strip times
        self.assertEqual(out, reference_out)
        self.assertEqual(err, thick_dz)
        # check log file
        f = open("mocmg.log", "r")
        lines = f.readlines()
        f.close()
        lines = [line.split(None, 1)[1].rstrip("\n") for line in lines]
        self.assertEqual(lines, reference_out + thick_dz)
