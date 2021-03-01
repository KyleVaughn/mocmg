"""Test the gmsh utility functions."""
from unittest import TestCase

import gmsh
import pytest

import mocmg
import mocmg.gmsh_utils

from .testing_utils import captured_output

bad_name = ["ERROR     : mocmg.gmsh_utils - No physical group of name 'Bad name'."]


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

    def test_get_entities_for_physical_group_bad_name(self):
        """Test the get_entities_for_physical_group_name for a regular use case."""
        with pytest.raises(SystemExit):
            with captured_output() as (out, err):
                mocmg.initialize()
                gmsh.initialize()
                tag = gmsh.model.occ.addDisk(0.0, 0.0, 0.0, 1.0, 1.0)
                gmsh.model.occ.synchronize()
                output_tag = gmsh.model.addPhysicalGroup(2, [tag])
                gmsh.model.setPhysicalName(2, output_tag, "Test Physical Group Name")
                mocmg.gmsh_utils.get_entities_for_physical_group_name("Bad name")
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out = [line.split(None, 1)[1] for line in out]
        err = [line.split(None, 1)[1] for line in [err[0]]]  # strip times
        self.assertEqual(out, [])
        self.assertEqual(err, bad_name)
        gmsh.clear()
        gmsh.finalize()
