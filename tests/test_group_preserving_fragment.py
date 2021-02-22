"""Test the group_preserving_fragment function."""
from unittest import TestCase

import gmsh
import pytest

import mocmg

from .testing_utils import captured_output

# Honestly, just use gmsh.fltk.run() to debug.
ref_out = [
    "INFO      : mocmg.model.group_preserving_fragment - Fragmenting 2 entities",
    "INFO      : mocmg.model.group_preserving_fragment - Synchronizing model",
]
bad_overwrite = [
    "ERROR     : mocmg.model.group_preserving_fragment - Material to be overwritten"
    + " is not in the physical groups of the entities being fragmented."
]

# 2 intersecting rectangles
groups_2_rectangles = {
    "Group 1": [1, 2],
    "Group 2": [2, 3],
    "All": [1, 2, 3],
}
groups_2_rectangles_w_materials = {
    "Material_1": [1],
    "Material_2": [2, 3],
    "All": [1, 2, 3],
}
centroids_2_rectangles = {
    1: (0.83333333, 0.83333333, 0.0),
    2: (1.5, 1.5, 0.0),
    3: (2.16666666, 2.16666666, 0.0),
}
areas_2_rectangles = {
    1: 3.0,
    2: 1.0,
    3: 3.0,
}

# 2 intersecting rectangles, 1 other rectangle off to the side.
groups_3_rectangles_1_not_in_frag = {
    "Group 1": [4, 5],
    "Group 2": [5, 6],
    "Group 3": [3],
    "All": [3, 4, 5, 6],
}
centroids_3_rectangles_1_not_in_frag = {
    3: (5.0, 5.0, 0.0),
    4: (0.83333333, 0.83333333, 0.0),
    5: (1.5, 1.5, 0.0),
    6: (2.16666666, 2.16666666, 0.0),
}
areas_3_rectangles_1_not_in_frag = {
    3: 4.0,
    4: 3.0,
    5: 1.0,
    6: 3.0,
}


class TestGroupPreservingFragment(TestCase):
    """Test the group_preserving_fragment function."""

    def test_2_rectangles(self):
        """Test a 2 rectangle case."""
        ref_groups = groups_2_rectangles
        ref_centroids = centroids_2_rectangles
        ref_areas = areas_2_rectangles
        # Setup
        with captured_output() as (out, err):
            mocmg.initialize()
            gmsh.initialize()
            gmsh.model.occ.addRectangle(0.0, 0.0, 0.0, 2.0, 2.0)
            gmsh.model.occ.addRectangle(1.0, 1.0, 0.0, 2.0, 2.0)
            gmsh.model.occ.synchronize()
            gmsh.model.addPhysicalGroup(2, [1])
            gmsh.model.addPhysicalGroup(2, [2])
            gmsh.model.addPhysicalGroup(2, [1, 2])
            gmsh.model.setPhysicalName(2, 1, "Group 1")
            gmsh.model.setPhysicalName(2, 2, "Group 2")
            gmsh.model.setPhysicalName(2, 3, "All")
        mocmg.model.group_preserving_fragment([(2, 1)], [(2, 2)])
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out = [line.split(None, 1)[1] for line in out]
        err = [line.split(None, 1)[1] for line in err]  # strip times
        self.assertEqual(out, ref_out)
        self.assertEqual(err, [])
        # Get info
        group_nums = gmsh.model.getPhysicalGroups()
        names = [gmsh.model.getPhysicalName(*grp) for grp in group_nums]
        ref_names = list(ref_groups.keys())
        # Check correct group names/entities
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
            self.assertAlmostEqual(ref_areas[tag], mass, places=5)
            x, y, z = gmsh.model.occ.getCenterOfMass(2, tag)
            centroid = (x, y, z)
            for i in range(3):
                self.assertAlmostEqual(centroid[i], ref_centroids[tag][i])
        # Clean up
        gmsh.clear()
        gmsh.finalize()

    def test_2_rectangles_no_group(self):
        """Test for a 2 rectangle case, where 1 has no groups."""
        ref_groups = groups_2_rectangles
        ref_centroids = centroids_2_rectangles
        ref_areas = areas_2_rectangles
        # Setup
        with captured_output() as (out, err):
            mocmg.initialize()
            gmsh.initialize()
            gmsh.model.occ.addRectangle(0.0, 0.0, 0.0, 2.0, 2.0)
            gmsh.model.occ.addRectangle(1.0, 1.0, 0.0, 2.0, 2.0)
            gmsh.model.occ.synchronize()
            gmsh.model.addPhysicalGroup(2, [1])
            gmsh.model.setPhysicalName(2, 1, "Group 1")
            mocmg.model.group_preserving_fragment([(2, 1)], [(2, 2)])
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out = [line.split(None, 1)[1] for line in out]
        err = [line.split(None, 1)[1] for line in err]  # strip times
        self.assertEqual(out, ref_out)
        self.assertEqual(err, [])
        # Get info
        group_nums = gmsh.model.getPhysicalGroups()
        names = [gmsh.model.getPhysicalName(*grp) for grp in group_nums]
        ref_names = list(ref_groups.keys())
        # Check correct group names/entities
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
            self.assertAlmostEqual(ref_areas[tag], mass, places=5)
            x, y, z = gmsh.model.occ.getCenterOfMass(2, tag)
            centroid = (x, y, z)
            for i in range(3):
                self.assertAlmostEqual(centroid[i], ref_centroids[tag][i])
        # Clean up
        gmsh.clear()
        gmsh.finalize()

    def test_3_rectangles_1_not_in_frag(self):
        """Test 2 rectangles in frag, one off to the side."""
        ref_groups = groups_3_rectangles_1_not_in_frag
        ref_centroids = centroids_3_rectangles_1_not_in_frag
        ref_areas = areas_3_rectangles_1_not_in_frag
        # Setup
        with captured_output() as (out, err):
            mocmg.initialize()
            gmsh.initialize()
            gmsh.model.occ.addRectangle(0.0, 0.0, 0.0, 2.0, 2.0)
            gmsh.model.occ.addRectangle(1.0, 1.0, 0.0, 2.0, 2.0)
            gmsh.model.occ.addRectangle(4.0, 4.0, 0.0, 2.0, 2.0)
            gmsh.model.occ.synchronize()
            gmsh.model.addPhysicalGroup(2, [1])
            gmsh.model.addPhysicalGroup(2, [2])
            gmsh.model.addPhysicalGroup(2, [3])
            gmsh.model.addPhysicalGroup(2, [1, 2, 3])
            gmsh.model.setPhysicalName(2, 1, "Group 1")
            gmsh.model.setPhysicalName(2, 2, "Group 2")
            gmsh.model.setPhysicalName(2, 3, "Group 3")
            gmsh.model.setPhysicalName(2, 4, "All")
            mocmg.model.group_preserving_fragment([(2, 1)], [(2, 2)])
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out = [line.split(None, 1)[1] for line in out]
        err = [line.split(None, 1)[1] for line in err]  # strip times
        self.assertEqual(out, ref_out)
        self.assertEqual(err, [])
        # Get info
        group_nums = gmsh.model.getPhysicalGroups()
        names = [gmsh.model.getPhysicalName(*grp) for grp in group_nums]
        ref_names = list(ref_groups.keys())
        # Check correct group names/entities
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
            self.assertAlmostEqual(ref_areas[tag], mass, places=5)
            x, y, z = gmsh.model.occ.getCenterOfMass(2, tag)
            centroid = (x, y, z)
            for i in range(3):
                self.assertAlmostEqual(centroid[i], ref_centroids[tag][i])
        # Clean up
        gmsh.clear()
        gmsh.finalize()

    def test_2_rectangles_with_overwrite(self):
        """Test a 2 rectangle case, overwriting a material."""
        ref_groups = groups_2_rectangles_w_materials
        ref_centroids = centroids_2_rectangles
        ref_areas = areas_2_rectangles
        # Setup
        with captured_output() as (out, err):
            mocmg.initialize()
            gmsh.initialize()
            gmsh.model.occ.addRectangle(0.0, 0.0, 0.0, 2.0, 2.0)
            gmsh.model.occ.addRectangle(1.0, 1.0, 0.0, 2.0, 2.0)
            gmsh.model.occ.synchronize()
            gmsh.model.addPhysicalGroup(2, [1])
            gmsh.model.addPhysicalGroup(2, [2])
            gmsh.model.addPhysicalGroup(2, [1, 2])
            gmsh.model.setPhysicalName(2, 1, "Material_1")
            gmsh.model.setPhysicalName(2, 2, "Material_2")
            gmsh.model.setPhysicalName(2, 3, "All")
            mocmg.model.group_preserving_fragment(
                [(2, 1)], [(2, 2)], overwrite_material="Material_1"
            )
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out = [line.split(None, 1)[1] for line in out]
        err = [line.split(None, 1)[1] for line in err]  # strip times
        self.assertEqual(out, ref_out)
        self.assertEqual(err, [])
        # Get info
        group_nums = gmsh.model.getPhysicalGroups()
        names = [gmsh.model.getPhysicalName(*grp) for grp in group_nums]
        ref_names = list(ref_groups.keys())
        # Check correct group names/entities
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
            self.assertAlmostEqual(ref_areas[tag], mass, places=5)
            x, y, z = gmsh.model.occ.getCenterOfMass(2, tag)
            centroid = (x, y, z)
            for i in range(3):
                self.assertAlmostEqual(centroid[i], ref_centroids[tag][i])
        # Clean up
        gmsh.clear()
        gmsh.finalize()

    def test_2_rectangles_with_bad_overwrite(self):
        """Test a 2 rectangle case, overwriting a material that doesnt exist."""
        with pytest.raises(SystemExit):
            with captured_output() as (out, err):
                mocmg.initialize()
                gmsh.initialize()
                gmsh.model.occ.addRectangle(0.0, 0.0, 0.0, 2.0, 2.0)
                gmsh.model.occ.addRectangle(1.0, 1.0, 0.0, 2.0, 2.0)
                gmsh.model.occ.synchronize()
                gmsh.model.addPhysicalGroup(2, [1])
                gmsh.model.addPhysicalGroup(2, [2])
                gmsh.model.addPhysicalGroup(2, [1, 2])
                gmsh.model.setPhysicalName(2, 1, "Material_1")
                gmsh.model.setPhysicalName(2, 2, "Material_2")
                gmsh.model.setPhysicalName(2, 3, "All")
                mocmg.model.group_preserving_fragment(
                    [(2, 1)], [(2, 2)], overwrite_material="BAD_MAT"
                )
        gmsh.clear()
        gmsh.finalize()
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out = [line.split(None, 1)[1] for line in out]
        err = [line.split(None, 1)[1] for line in [err[0]]]  # strip times
        self.assertEqual(out, ref_out)
        self.assertEqual(err, bad_overwrite)
