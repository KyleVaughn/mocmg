"""Test the gmsh utility functions."""
from unittest import TestCase

import gmsh

import mocmg
import mocmg.gmsh_utils


class TestGetEntitiesForPhysicalGroup(TestCase):
    """Test the get_entities_for_physical_group_name function."""

    def test_get_entities_for_physical_group(self):
        """Test the get_entities_for_physical_group_name for a regular use case."""
        mocmg.initialize()
        gmsh.initialize()
        tag = gmsh.model.occ.addDisk(0.0, 0.0, 0.0, 1.0, 1.0)
        gmsh.model.occ.synchronize()
        output_tag = gmsh.model.addPhysicalGroup(2, [tag])
        gmsh.model.setPhysicalName(2, output_tag, "Test Physical Group Name")
        ents = mocmg.gmsh_utils.get_entities_for_physical_group_name("Test Physical Group Name")
        self.assertEqual([1], ents)
        gmsh.clear()
        gmsh.finalize()
