"""Test the make_gridmesh function."""
from unittest import TestCase

from mesh_data import (
    pin_1_cell_sets,
    pin_1_cells,
    pin_1_vertices,
    pin_1and2_cell_sets,
    pin_1and2_cells,
    pin_1and2_vertices,
    pin_2_cell_sets,
    pin_2_cells,
    pin_2_vertices,
)

import mocmg
import mocmg.mesh


class TestMakeGridMesh(TestCase):
    """Test the make_gridmesh function."""

    def test_make_gridmesh(self):  # noqa: C901
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
        self.assertEqual("both_pins", mesh.name)
        both_pins_mesh = mocmg.mesh.make_gridmesh(mesh)
        # Root level
        self.assertEqual(None, both_pins_mesh.vertices)
        self.assertEqual(None, both_pins_mesh.cells)
        self.assertEqual(None, both_pins_mesh.cell_sets)
        self.assertEqual("both_pins", both_pins_mesh.name)
        self.assertEqual(len(both_pins_mesh.children), 1)
        # level1
        level1 = both_pins_mesh.children[0]
        self.assertEqual(None, level1.vertices)
        self.assertEqual(None, level1.cells)
        self.assertEqual(None, level1.cell_sets)
        self.assertEqual("GRID_L1_1_1", level1.name)
        self.assertEqual(len(level1.children), 2)
        self.assertEqual(level1.parent.name, "both_pins")
        # level2
        level2_1_1, level2_2_1 = level1.children
        self.assertEqual(level2_1_1.name, "GRID_L2_1_1")
        self.assertEqual(level2_2_1.name, "GRID_L2_2_1")
        # level2_1_1
        # vertices
        vert_keys = list(pin_1_vertices.keys())
        for v in vert_keys:
            for i in range(3):
                self.assertEqual(level2_1_1.vertices[v][i], pin_1_vertices[v][i])
        # cells
        cell_types = list(pin_1_cells.keys())
        for cell_type in cell_types:
            cell_ids = list(pin_1_cells[cell_type].keys())
            for cell_id in cell_ids:
                vert_ids = pin_1_cells[cell_type][cell_id]
                for v in range(len(vert_ids)):
                    self.assertEqual(
                        level2_1_1.cells[cell_type][cell_id][v], pin_1_cells[cell_type][cell_id][v]
                    )
        # cell_sets
        for set_name in list(pin_1_cell_sets.keys()):
            set_cells = pin_1_cell_sets[set_name]
            for cell in range(len(set_cells)):
                self.assertEqual(
                    level2_1_1.cell_sets[set_name][cell], pin_1_cell_sets[set_name][cell]
                )
        # level2_2_1
        # vertices
        vert_keys = list(pin_2_vertices.keys())
        for v in vert_keys:
            for i in range(3):
                self.assertEqual(level2_2_1.vertices[v][i], pin_2_vertices[v][i])
        # cells
        cell_types = list(pin_2_cells.keys())
        for cell_type in cell_types:
            cell_ids = list(pin_2_cells[cell_type].keys())
            for cell_id in cell_ids:
                vert_ids = pin_2_cells[cell_type][cell_id]
                for v in range(len(vert_ids)):
                    self.assertEqual(
                        level2_2_1.cells[cell_type][cell_id][v], pin_2_cells[cell_type][cell_id][v]
                    )
        # cell_sets
        for set_name in list(pin_2_cell_sets.keys()):
            set_cells = pin_2_cell_sets[set_name]
            for cell in range(len(set_cells)):
                self.assertEqual(
                    level2_2_1.cell_sets[set_name][cell], pin_2_cell_sets[set_name][cell]
                )

    def test_make_gridmesh_without_root_name(self):  # noqa: C901
        """Test generating a GridMesh hierarchy from a Mesh with no name."""
        mesh = mocmg.mesh.Mesh(pin_1and2_vertices, pin_1and2_cells, pin_1and2_cell_sets)
        self.assertEqual(pin_1and2_vertices, mesh.vertices)
        self.assertEqual(pin_1and2_cells, mesh.cells)
        self.assertEqual(pin_1and2_cell_sets, mesh.cell_sets)
        self.assertEqual("", mesh.name)
        both_pins_mesh = mocmg.mesh.make_gridmesh(mesh)
        # Root level
        self.assertEqual(None, both_pins_mesh.vertices)
        self.assertEqual(None, both_pins_mesh.cells)
        self.assertEqual(None, both_pins_mesh.cell_sets)
        self.assertEqual("mesh_domain", both_pins_mesh.name)
        self.assertEqual(len(both_pins_mesh.children), 1)
        # level1
        level1 = both_pins_mesh.children[0]
        self.assertEqual(None, level1.vertices)
        self.assertEqual(None, level1.cells)
        self.assertEqual(None, level1.cell_sets)
        self.assertEqual("GRID_L1_1_1", level1.name)
        self.assertEqual(len(level1.children), 2)
        self.assertEqual(level1.parent.name, "mesh_domain")
        # level2
        level2_1_1, level2_2_1 = level1.children
        self.assertEqual(level2_1_1.name, "GRID_L2_1_1")
        self.assertEqual(level2_2_1.name, "GRID_L2_2_1")
        # level2_1_1
        # vertices
        vert_keys = list(pin_1_vertices.keys())
        for v in vert_keys:
            for i in range(3):
                self.assertEqual(level2_1_1.vertices[v][i], pin_1_vertices[v][i])
        # cells
        cell_types = list(pin_1_cells.keys())
        for cell_type in cell_types:
            cell_ids = list(pin_1_cells[cell_type].keys())
            for cell_id in cell_ids:
                vert_ids = pin_1_cells[cell_type][cell_id]
                for v in range(len(vert_ids)):
                    self.assertEqual(
                        level2_1_1.cells[cell_type][cell_id][v], pin_1_cells[cell_type][cell_id][v]
                    )
        # cell_sets
        for set_name in list(pin_1_cell_sets.keys()):
            set_cells = pin_1_cell_sets[set_name]
            for cell in range(len(set_cells)):
                self.assertEqual(
                    level2_1_1.cell_sets[set_name][cell], pin_1_cell_sets[set_name][cell]
                )
        # level2_2_1
        # vertices
        vert_keys = list(pin_2_vertices.keys())
        for v in vert_keys:
            for i in range(3):
                self.assertEqual(level2_2_1.vertices[v][i], pin_2_vertices[v][i])
        # cells
        cell_types = list(pin_2_cells.keys())
        for cell_type in cell_types:
            cell_ids = list(pin_2_cells[cell_type].keys())
            for cell_id in cell_ids:
                vert_ids = pin_2_cells[cell_type][cell_id]
                for v in range(len(vert_ids)):
                    self.assertEqual(
                        level2_2_1.cells[cell_type][cell_id][v], pin_2_cells[cell_type][cell_id][v]
                    )
        # cell_sets
        for set_name in list(pin_2_cell_sets.keys()):
            set_cells = pin_2_cell_sets[set_name]
            for cell in range(len(set_cells)):
                self.assertEqual(
                    level2_2_1.cell_sets[set_name][cell], pin_2_cell_sets[set_name][cell]
                )
