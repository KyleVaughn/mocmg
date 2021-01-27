"""Test the group_preserving_fragment function."""
from unittest import TestCase

import gmsh

import mocmg


class TestGroupPreservingFragment(TestCase):
    """Test the group_preserving_fragment function."""

    def test_get_entities_for_physical_group(self):
        """Test the get_entities_for_physical_group_name for a regular use case."""
        mocmg.initialize()
        gmsh.initialize()
        gmsh.model.occ.addDisk(-0.2, 0.0, 0.0, 1.0, 1.0)
        gmsh.model.occ.addDisk(0.2, 0.0, 0.0, 1.0, 1.0)
        gmsh.model.occ.addDisk(0.0, 0.5, 0.0, 1.0, 1.0)
        gmsh.model.occ.synchronize()
        gmsh.model.addPhysicalGroup(2, [1])
        gmsh.model.addPhysicalGroup(2, [2])
        gmsh.model.addPhysicalGroup(2, [3])
        gmsh.model.addPhysicalGroup(2, [1, 2, 3])
        gmsh.model.setPhysicalName(2, 1, "Group 1")
        gmsh.model.setPhysicalName(2, 2, "Group 2")
        gmsh.model.setPhysicalName(2, 3, "Group 3")
        gmsh.model.setPhysicalName(2, 4, "All")
        mocmg.model.group_preserving_fragment([(2, 2), (2, 1)], [(2, 3)])
        gmsh.fltk.run()
        gmsh.clear()
        gmsh.finalize()
        self.assertEqual(1, 2)
