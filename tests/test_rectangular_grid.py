"""Test the rectangular grid function."""
from unittest import TestCase

import gmsh
import pytest

import mocmg

# from mocmg.gmsh_utils import get_entities_for_physical_group_name
from mocmg.grid import rectangular_grid

from .testing_utils import captured_output

bb_11 = [0.0, 0.0, 0.0, 1.0, 1.0, 0.0]
bb_44 = [0.0, 0.0, 0.0, 4.0, 4.0, 0.0]
bb_dz = [0.0, 0.0, 0.0, 1.0, 1.0, 10.0]

# Expected output for generating rectangular grid
reference_out = [
    "INFO      : mocmg.grid - Generating rectangular grid",
]

# Expected error for a bad bounding box that produces negative dx, dy, dz
bad_bb = [
    "ERROR     : mocmg.grid - Invalid bounding box.",
]

# Expected error for argument of incorrect type
bad_type = [
    "ERROR     : mocmg.grid - Arguments should be iterable.",
]

# Expected error for mismatch of x and y size
len_mismatch = [
    "ERROR     : mocmg.grid - Length of arguments differ (2 and 1). "
    + "They should have the same number of levels.",
]

# Expected error for too many arguments
num_args = [
    "ERROR     : mocmg.grid - Incorrect number of arguments given."
    + " Provide one of (x or nx) and one of (ny or y).",
]

# Expected error for overly thick model
thick_dz = [
    "ERROR     : mocmg.grid - Bounding box thickness is greater than 1e-6"
    + " (10.000000). Bounding box expected in 2D x-y plane.",
]

# Expected error for non-int nx elements
nx_type = ["ERROR     : mocmg.grid - nx must contain positive integer elements only."]

# Expected error for non-int nx elements
ny_type = ["ERROR     : mocmg.grid - ny must contain positive integer elements only."]

# Expected error for non-list x elements
x_nonlist_type = ["ERROR     : mocmg.grid - x must have iterable elements."]

# Expected error for non-list y elements
y_nonlist_type = ["ERROR     : mocmg.grid - y must have iterable elements."]

# Expected error when divisions outside of bb
out_of_bb = ["ERROR     : mocmg.grid - Divisions must be within the bounding box."]

"""
For 2 by 2 single level
-------------------------------------- (4,4)
|                 |                  |
|                 |                  |
|                 |                  |
|        3        |         4        |
|                 |                  |
|                 |                  |
|                 |                  |
|------------------------------------- (4,2)
|                 |                  |
|                 |                  |
|                 |                  |
|        1        |         2        |
|                 |                  |
|                 |                  |
|                 |                  |
--------------------------------------
(0,0)           (2,0)              (4,0)
"""
ents_21 = [(2, 1), (2, 2), (2, 3), (2, 4)]
groups_21 = {
    "Grid_L1_1_1": [1],
    "Grid_L1_2_1": [2],
    "Grid_L1_1_2": [3],
    "Grid_L1_2_2": [4],
}
centroids_21 = {
    1: (1.0, 1.0, 0.0),
    2: (3.0, 1.0, 0.0),
    3: (1.0, 3.0, 0.0),
    4: (3.0, 3.0, 0.0),
}

"""

# For 2 by ) with second level 2 by 2
-------------------------------------- (4,4)
|                 |                  |
|                 |                  |
|                 |                  |
|       etc.      |        etc.      |
|                 |                  |
|                 |                  |
|                 |                  |
|------------------------------------- (4,2)
|        |        |        |         |
|   5    |   6    |    7   |    8    |
|        |        |        |         |
|--------|--------|--------|---------|
|        |        |        |         |
|   1    |   2    |    3   |    4    |
|        |        |        |         |
--------------------------------------
(0,0)           (2,0)              (4,0)
"""
ents_22 = [(2, 1), (2, 2), (2, 3), (2, 4)]
groups_22 = {
    "Grid_L1_1_1": [1, 2, 5, 6],
    "Grid_L1_2_1": [3, 4, 7, 8],
    "Grid_L1_1_2": [9, 10, 13, 14],
    "Grid_L1_2_2": [11, 12, 15, 16],
    "Grid_L2_1_1": [1],
    "Grid_L2_2_1": [2],
    "Grid_L2_3_1": [3],
    "Grid_L2_4_1": [4],
    "Grid_L2_1_2": [5],
    "Grid_L2_2_2": [6],
    "Grid_L2_3_2": [7],
    "Grid_L2_4_2": [8],
    "Grid_L2_1_3": [9],
    "Grid_L2_2_3": [10],
    "Grid_L2_3_3": [11],
    "Grid_L2_4_3": [12],
    "Grid_L2_1_4": [13],
    "Grid_L2_2_4": [14],
    "Grid_L2_3_4": [15],
    "Grid_L2_4_4": [16],
}

centroids_22 = {
    1: (0.5, 0.5, 0.0),
    2: (1.5, 0.5, 0.0),
    3: (2.5, 0.5, 0.0),
    4: (3.5, 0.5, 0.0),
    5: (0.5, 1.5, 0.0),
    6: (1.5, 1.5, 0.0),
    7: (2.5, 1.5, 0.0),
    8: (3.5, 1.5, 0.0),
    9: (0.5, 2.5, 0.0),
    10: (1.5, 2.5, 0.0),
    11: (2.5, 2.5, 0.0),
    12: (3.5, 2.5, 0.0),
    13: (0.5, 3.5, 0.0),
    14: (1.5, 3.5, 0.0),
    15: (2.5, 3.5, 0.0),
    16: (3.5, 3.5, 0.0),
}


class TestRectangularGrid(TestCase):
    """Test the grid.rectangular_grid function."""

    def test_bad_bounding_box(self):
        """Test a bad bounding box that produces negative dx, dy, dz."""
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
        """Test rect grid with non-iterable args."""
        with pytest.raises(SystemExit):
            with captured_output() as (out, err):
                mocmg.initialize()
                gmsh.initialize()
                rectangular_grid(bb_11, x=[[0.5]], ny=4)
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

    def test_arg_len_mismatch_xy(self):
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

    def test_arg_len_mismatch_nxny(self):
        """Test rect grid with mismatched arg len."""
        with pytest.raises(SystemExit):
            with captured_output() as (out, err):
                mocmg.initialize()
                gmsh.initialize()
                rectangular_grid(bb_11, x=[2, 3], y=[1])
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
        """Test rect grid with non-integer type nx elements."""
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
        """Test rect grid with non-integer type ny elements."""
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

    def test_x_noniterable_type(self):
        """Test rect grid with non-iterable type elements."""
        with pytest.raises(SystemExit):
            with captured_output() as (out, err):
                mocmg.initialize()
                gmsh.initialize()
                rectangular_grid(bb_11, x=[1], y=[[1]])
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

    def test_y_noniterable_type(self):
        """Test rect grid with non-iterable type elements."""
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

    def test_nx0(self):
        """Test nx with 0 division."""
        with pytest.raises(SystemExit):
            with captured_output() as (out, err):
                mocmg.initialize()
                gmsh.initialize()
                rectangular_grid(bb_11, nx=[1, 0], ny=[1, 1])
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

    def test_ny0(self):
        """Test ny with 0 division."""
        with pytest.raises(SystemExit):
            with captured_output() as (out, err):
                mocmg.initialize()
                gmsh.initialize()
                rectangular_grid(bb_11, nx=[1, 1], ny=[0, 1])
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

    def test_x_y_21(self):
        """Test xy with 1 division."""
        ref_groups = groups_21
        ref_centroids = centroids_21
        mocmg.initialize()
        gmsh.initialize()
        rectangular_grid(bb_44, x=[[2.0]], y=[[2.0]])
        group_nums = gmsh.model.getPhysicalGroups()
        names = [gmsh.model.getPhysicalName(*grp) for grp in group_nums]
        ref_names = list(ref_groups.keys())
        # Check correct names/entities
        for i, name in enumerate(names):
            self.assertEqual(name, ref_names[i])
            index = names.index(name)
            group_ents = list(gmsh.model.getEntitiesForPhysicalGroup(*group_nums[index]))
            ref_group_ents = ref_groups[name]
            self.assertEqual(group_ents, ref_group_ents)
        # Check correct area/centroid
        for ent in gmsh.model.getEntities(2):
            tag = ent[1]
            mass = gmsh.model.occ.getMass(2, tag)
            self.assertAlmostEqual(4.0, mass, places=5, msg="2 width, 2 height, 4 area")
            x, y, z = gmsh.model.occ.getCenterOfMass(2, tag)
            centroid = (x, y, z)
            for i in range(3):
                self.assertAlmostEqual(centroid[i], ref_centroids[tag][i])
        gmsh.clear()
        gmsh.finalize()

    def test_nx_ny_21(self):
        """Test nx, ny with 1 division."""
        ref_groups = groups_21
        ref_centroids = centroids_21
        mocmg.initialize()
        gmsh.initialize()
        rectangular_grid(bb_44, nx=[2], ny=[2])
        group_nums = gmsh.model.getPhysicalGroups()
        names = [gmsh.model.getPhysicalName(*grp) for grp in group_nums]
        ref_names = list(ref_groups.keys())
        # Check correct names/entities
        for i, name in enumerate(names):
            self.assertEqual(name, ref_names[i])
            index = names.index(name)
            group_ents = list(gmsh.model.getEntitiesForPhysicalGroup(*group_nums[index]))
            ref_group_ents = ref_groups[name]
            self.assertEqual(group_ents, ref_group_ents)
        # Check correct area/centroid
        for ent in gmsh.model.getEntities(2):
            tag = ent[1]
            mass = gmsh.model.occ.getMass(2, tag)
            self.assertAlmostEqual(4.0, mass, places=5, msg="2 width, 2 height, 4 area")
            x, y, z = gmsh.model.occ.getCenterOfMass(2, tag)
            centroid = (x, y, z)
            for i in range(3):
                self.assertAlmostEqual(centroid[i], ref_centroids[tag][i])
        gmsh.clear()
        gmsh.finalize()

    def test_x_ny_21(self):
        """Test x, ny with 1 division."""
        ref_groups = groups_21
        ref_centroids = centroids_21
        mocmg.initialize()
        gmsh.initialize()
        rectangular_grid(bb_44, x=[[2.0]], ny=[2])
        group_nums = gmsh.model.getPhysicalGroups()
        names = [gmsh.model.getPhysicalName(*grp) for grp in group_nums]
        ref_names = list(ref_groups.keys())
        # Check correct names/entities
        for i, name in enumerate(names):
            self.assertEqual(name, ref_names[i])
            index = names.index(name)
            group_ents = list(gmsh.model.getEntitiesForPhysicalGroup(*group_nums[index]))
            ref_group_ents = ref_groups[name]
            self.assertEqual(group_ents, ref_group_ents)
        # Check correct area/centroid
        for ent in gmsh.model.getEntities(2):
            tag = ent[1]
            mass = gmsh.model.occ.getMass(2, tag)
            self.assertAlmostEqual(4.0, mass, places=5, msg="2 width, 2 height, 4 area")
            x, y, z = gmsh.model.occ.getCenterOfMass(2, tag)
            centroid = (x, y, z)
            for i in range(3):
                self.assertAlmostEqual(centroid[i], ref_centroids[tag][i])
        gmsh.clear()
        gmsh.finalize()

    def test_nx_y_21(self):
        """Test nx, y with 1 division."""
        ref_groups = groups_21
        ref_centroids = centroids_21
        mocmg.initialize()
        gmsh.initialize()
        rectangular_grid(bb_44, nx=[2], y=[[2.0]])
        group_nums = gmsh.model.getPhysicalGroups()
        names = [gmsh.model.getPhysicalName(*grp) for grp in group_nums]
        ref_names = list(ref_groups.keys())
        # Check correct names/entities
        for i, name in enumerate(names):
            self.assertEqual(name, ref_names[i])
            index = names.index(name)
            group_ents = list(gmsh.model.getEntitiesForPhysicalGroup(*group_nums[index]))
            ref_group_ents = ref_groups[name]
            self.assertEqual(group_ents, ref_group_ents)
        # Check correct area/centroid
        for ent in gmsh.model.getEntities(2):
            tag = ent[1]
            mass = gmsh.model.occ.getMass(2, tag)
            self.assertAlmostEqual(4.0, mass, places=5, msg="2 width, 2 height, 4 area")
            x, y, z = gmsh.model.occ.getCenterOfMass(2, tag)
            centroid = (x, y, z)
            for i in range(3):
                self.assertAlmostEqual(centroid[i], ref_centroids[tag][i])
        gmsh.clear()
        gmsh.finalize()

    def test_x_y_22(self):
        """Test x, y with 2 levels of 1 division."""
        ref_groups = groups_22
        ref_centroids = centroids_22
        mocmg.initialize()
        gmsh.initialize()
        rectangular_grid(bb_44, x=[[2.0], [1.0, 3.0]], y=[[2.0], [1.0, 3.0]])
        group_nums = gmsh.model.getPhysicalGroups()
        names = [gmsh.model.getPhysicalName(*grp) for grp in group_nums]
        print(names)
        ref_names = list(ref_groups.keys())
        # Check correct names/entities
        for i, name in enumerate(names):
            self.assertEqual(name, ref_names[i])
            index = names.index(name)
            group_ents = list(gmsh.model.getEntitiesForPhysicalGroup(*group_nums[index]))
            ref_group_ents = ref_groups[name]
            self.assertEqual(group_ents, ref_group_ents)
        # Check correct area/centroid
        for ent in gmsh.model.getEntities(2):
            tag = ent[1]
            mass = gmsh.model.occ.getMass(2, tag)
            self.assertAlmostEqual(1.0, mass, places=5, msg="1 width, 1 height, 1 area")
            x, y, z = gmsh.model.occ.getCenterOfMass(2, tag)
            centroid = (x, y, z)
            for i in range(3):
                self.assertAlmostEqual(centroid[i], ref_centroids[tag][i])
        gmsh.clear()
        gmsh.finalize()

    def test_nx_ny_22(self):
        """Test nx, ny with 2 levels of 1 division."""
        ref_groups = groups_22
        ref_centroids = centroids_22
        mocmg.initialize()
        gmsh.initialize()
        rectangular_grid(bb_44, nx=[2, 2], ny=[2, 2])
        group_nums = gmsh.model.getPhysicalGroups()
        names = [gmsh.model.getPhysicalName(*grp) for grp in group_nums]
        print(names)
        ref_names = list(ref_groups.keys())
        # Check correct names/entities
        for i, name in enumerate(names):
            self.assertEqual(name, ref_names[i])
            index = names.index(name)
            group_ents = list(gmsh.model.getEntitiesForPhysicalGroup(*group_nums[index]))
            ref_group_ents = ref_groups[name]
            self.assertEqual(group_ents, ref_group_ents)
        # Check correct area/centroid
        for ent in gmsh.model.getEntities(2):
            tag = ent[1]
            mass = gmsh.model.occ.getMass(2, tag)
            self.assertAlmostEqual(1.0, mass, places=5, msg="1 width, 1 height, 1 area")
            x, y, z = gmsh.model.occ.getCenterOfMass(2, tag)
            centroid = (x, y, z)
            for i in range(3):
                self.assertAlmostEqual(centroid[i], ref_centroids[tag][i])
        gmsh.clear()
        gmsh.finalize()
