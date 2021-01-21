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

# Expected error for a bad bounding box that produces negative dx, dy, dz
bad_bb = [
    "ERROR     : mocmg.gmsh_utils - Invalid bounding box.",
]

# Expected error for argument of incorrect type
bad_type = [
    "ERROR     : mocmg.gmsh_utils - Arguments should be iterable.",
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

# Expected error for non-int nx elements
nx_type = ["ERROR     : mocmg.gmsh_utils - nx must be empty or contain integer elements only."]

# Expected error for non-int nx elements
ny_type = ["ERROR     : mocmg.gmsh_utils - ny must be empty or contain integer elements only."]

# Expected error for non-list x elements
x_nonlist_type = ["ERROR     : mocmg.gmsh_utils - x must have iterable elements."]

# Expected error for non-list y elements
y_nonlist_type = ["ERROR     : mocmg.gmsh_utils - y must have iterable elements."]

# Expected error when divisions outside of bb
out_of_bb = ["ERROR     : mocmg.gmsh_utils - Divisions must be within the bounding box."]


class TestRectangularGrid(TestCase):
    """Test the gmsh_utils.rectangular_grid function."""

    def test_bad_bounding_box(self):
        """Test rect grid with non-list args."""
        with pytest.raises(SystemExit):
            with captured_output() as (out, err):
                mocmg.initialize()
                gmsh.initialize()
                rectangular_grid([0, 0, 0, -1, -1, -1], x=[[0.5]], y=[[0.5]])
                gmsh.clear()
                gmsh.finalize()
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out = [line.split(None, 1)[1] for line in out]
        err = [line.split(None, 1)[1] for line in [err[0]]]  # strip times
        self.assertEqual(out, reference_out)
        self.assertEqual(err, bad_bb)
        # check log file
        f = open("mocmg.log", "r")
        lines = f.readlines()
        f.close()
        lines = [line.split(None, 1)[1].rstrip("\n") for line in lines]
        self.assertEqual(lines, reference_out + bad_bb)

    def test_bad_arg_type(self):
        """Test rect grid with non-list args."""
        with pytest.raises(SystemExit):
            with captured_output() as (out, err):
                mocmg.initialize()
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
                mocmg.initialize()
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
                mocmg.initialize()
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
                mocmg.initialize()
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
                mocmg.initialize()
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

    def test_nx_type(self):
        """Test rect grid with non-integer type elements."""
        with pytest.raises(SystemExit):
            with captured_output() as (out, err):
                mocmg.initialize()
                gmsh.initialize()
                rectangular_grid(bb_11, nx=[0.1], y=[[0.5]])
                gmsh.clear()
                gmsh.finalize()
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out = [line.split(None, 1)[1] for line in out]
        err = [line.split(None, 1)[1] for line in [err[0]]]  # strip times
        self.assertEqual(out, reference_out)
        self.assertEqual(err, nx_type)
        # check log file
        f = open("mocmg.log", "r")
        lines = f.readlines()
        f.close()
        lines = [line.split(None, 1)[1].rstrip("\n") for line in lines]
        self.assertEqual(lines, reference_out + nx_type)

    def test_ny_type(self):
        """Test rect grid with non-integer type elements."""
        with pytest.raises(SystemExit):
            with captured_output() as (out, err):
                mocmg.initialize()
                gmsh.initialize()
                rectangular_grid(bb_11, x=[[0.1]], ny=[0.5])
                gmsh.clear()
                gmsh.finalize()
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out = [line.split(None, 1)[1] for line in out]
        err = [line.split(None, 1)[1] for line in [err[0]]]  # strip times
        self.assertEqual(out, reference_out)
        self.assertEqual(err, ny_type)
        # check log file
        f = open("mocmg.log", "r")
        lines = f.readlines()
        f.close()
        lines = [line.split(None, 1)[1].rstrip("\n") for line in lines]
        self.assertEqual(lines, reference_out + ny_type)

    def test_x_nonlist_type(self):
        """Test rect grid with non-integer type elements."""
        with pytest.raises(SystemExit):
            with captured_output() as (out, err):
                mocmg.initialize()
                gmsh.initialize()
                rectangular_grid(bb_11, x=[1], ny=[1])
                gmsh.clear()
                gmsh.finalize()
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out = [line.split(None, 1)[1] for line in out]
        err = [line.split(None, 1)[1] for line in [err[0]]]  # strip times
        self.assertEqual(out, reference_out)
        self.assertEqual(err, x_nonlist_type)
        # check log file
        f = open("mocmg.log", "r")
        lines = f.readlines()
        f.close()
        lines = [line.split(None, 1)[1].rstrip("\n") for line in lines]
        self.assertEqual(lines, reference_out + x_nonlist_type)

    def test_y_nonlist_type(self):
        """Test rect grid with non-integer type elements."""
        with pytest.raises(SystemExit):
            with captured_output() as (out, err):
                mocmg.initialize()
                gmsh.initialize()
                rectangular_grid(bb_11, x=[[1]], y=[1.0])
                gmsh.clear()
                gmsh.finalize()
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out = [line.split(None, 1)[1] for line in out]
        err = [line.split(None, 1)[1] for line in [err[0]]]  # strip times
        self.assertEqual(out, reference_out)
        self.assertEqual(err, y_nonlist_type)
        # check log file
        f = open("mocmg.log", "r")
        lines = f.readlines()
        f.close()
        lines = [line.split(None, 1)[1].rstrip("\n") for line in lines]
        self.assertEqual(lines, reference_out + y_nonlist_type)

    def test_x_out_of_bb(self):
        """Test rect grid with an x-division outside the bb."""
        with pytest.raises(SystemExit):
            with captured_output() as (out, err):
                mocmg.initialize()
                gmsh.initialize()
                rectangular_grid(bb_11, x=[[-1.0]], y=[[1.0]])
                gmsh.clear()
                gmsh.finalize()
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out = [line.split(None, 1)[1] for line in out]
        err = [line.split(None, 1)[1] for line in [err[0]]]  # strip times
        self.assertEqual(out, reference_out)
        self.assertEqual(err, out_of_bb)
        # check log file
        f = open("mocmg.log", "r")
        lines = f.readlines()
        f.close()
        lines = [line.split(None, 1)[1].rstrip("\n") for line in lines]
        self.assertEqual(lines, reference_out + out_of_bb)

    def test_y_out_of_bb(self):
        """Test rect grid with a y-division outside the bb."""
        with pytest.raises(SystemExit):
            with captured_output() as (out, err):
                mocmg.initialize()
                gmsh.initialize()
                rectangular_grid(bb_11, x=[[1.0]], y=[[-1.0]])
                gmsh.clear()
                gmsh.finalize()
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out = [line.split(None, 1)[1] for line in out]
        err = [line.split(None, 1)[1] for line in [err[0]]]  # strip times
        self.assertEqual(out, reference_out)
        self.assertEqual(err, out_of_bb)
        # check log file
        f = open("mocmg.log", "r")
        lines = f.readlines()
        f.close()
        lines = [line.split(None, 1)[1].rstrip("\n") for line in lines]
        self.assertEqual(lines, reference_out + out_of_bb)

    #    def test_nx_0_ny_0(self):
    #        """Test nx=[0]."""
    #        mocmg.initialize()
    #        gmsh.initialize()
    #        rectangular_grid(bb_11, nx=[0], ny=[0])
    #        gmsh.clear()
    #        gmsh.finalize()
    #        self.assertEqual(1,2)
    #
    #    def test_x_0_y_0(self):
    #        """Test x with empty set and divisions=0."""
    #        mocmg.initialize()
    #        gmsh.initialize()
    #        rectangular_grid(bb_11, x=[[]], y=[[0]])
    #        gmsh.clear()
    #        gmsh.finalize()
    #        self.assertEqual(1,2)

    #    def test_n(self):
    #        """Test nx=[0]."""
    #        mocmg.initialize()
    #        gmsh.initialize()
    #        rectangular_grid(bb_11, nx=[2,2,2], ny=[2,2,2])
    #        gmsh.clear()
    #        gmsh.finalize()
    #        self.assertEqual(1,2)


#    def test_n(self):
#        """Test nx=[0]."""
#        mocmg.initialize()
#        gmsh.initialize()
#        rectangular_grid(bb_11, x=[[0.5], [0.25, 0.75]], y=[[0.5], [0.25, 0.75]])
#        gmsh.fltk.run()
#        gmsh.clear()
#        gmsh.finalize()
#        self.assertEqual(1, 2)
