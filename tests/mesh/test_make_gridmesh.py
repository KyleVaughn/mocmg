"""Test the make_gridmesh function."""
from unittest import TestCase

from mesh_data import pin_1and2_cell_sets, pin_1and2_cells, pin_1and2_vertices

import mocmg
import mocmg.mesh


class TestMakeGridMesh(TestCase):
    """Test the make_gridmesh function."""

    def test_make_gridmesh(self):
        """Test generating a GridMesh hierarchy from a Mesh."""
        # Test that mesh has grid cell sets
        with self.assertRaises(SystemExit):
            mesh = mocmg.mesh.Mesh(pin_1and2_vertices, pin_1and2_cells)
            self.assertEqual(pin_1and2_vertices, mesh.vertices)
            self.assertEqual(pin_1and2_cells, mesh.cells)
            mocmg.mesh.make_gridmesh(mesh)

        mesh = mocmg.mesh.Mesh(
            pin_1and2_vertices, pin_1and2_cells, pin_1and2_cell_sets, name="both_pins"
        )
        self.assertEqual(pin_1and2_vertices, mesh.vertices)
        self.assertEqual(pin_1and2_cells, mesh.cells)
        self.assertEqual(pin_1and2_cell_sets, mesh.cell_sets)
        mocmg.mesh.make_gridmesh(mesh)

        self.assertTrue(False)
