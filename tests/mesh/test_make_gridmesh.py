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
    three_level_grid_cell_sets,
    three_level_grid_cells,
    three_level_grid_vertices,
    three_level_l3_1_1_cells,
    three_level_l3_1_1_vertices,
    three_level_l3_1_2_cells,
    three_level_l3_1_2_vertices,
    three_level_l3_1_3_cells,
    three_level_l3_1_3_vertices,
    three_level_l3_3_3_cells,
    three_level_l3_3_3_vertices,
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

    def test_make_gridmesh_three_level_grid(self):  # noqa: C901
        """Test generating a GridMesh hierarchy from a Mesh with three grid levels."""
        # Test that mesh has grid cell sets
        ref_vertices = three_level_grid_vertices
        ref_cells = three_level_grid_cells
        ref_cell_sets = three_level_grid_cell_sets
        mesh = mocmg.mesh.Mesh(ref_vertices, ref_cells, ref_cell_sets, name="three_lvl_grid")
        self.assertEqual(ref_vertices, mesh.vertices)
        self.assertEqual(ref_cells, mesh.cells)
        self.assertEqual(ref_cell_sets, mesh.cell_sets)
        self.assertEqual("three_lvl_grid", mesh.name)
        grid_mesh = mocmg.mesh.make_gridmesh(mesh)
        # Root level
        self.assertEqual(None, grid_mesh.vertices)
        self.assertEqual(None, grid_mesh.cells)
        self.assertEqual(None, grid_mesh.cell_sets)
        self.assertEqual("three_lvl_grid", grid_mesh.name)
        self.assertEqual(len(grid_mesh.children), 1)
        # level1
        level1 = grid_mesh.children[0]
        self.assertEqual(None, level1.vertices)
        self.assertEqual(None, level1.cells)
        self.assertEqual(None, level1.cell_sets)
        self.assertEqual("GRID_L1_1_1", level1.name)
        self.assertEqual(len(level1.children), 4)
        self.assertEqual(level1.parent.name, "three_lvl_grid")
        # level2
        level2_1_1, level2_2_1, level2_1_2, level2_2_2 = level1.children
        self.assertEqual(level2_1_1.name, "GRID_L2_1_1")
        self.assertEqual(level2_2_1.name, "GRID_L2_2_1")
        self.assertEqual(level2_1_2.name, "GRID_L2_1_2")
        self.assertEqual(level2_2_2.name, "GRID_L2_2_2")
        # level2_1_1
        self.assertEqual(None, level2_1_1.vertices)
        self.assertEqual(None, level2_1_1.cells)
        self.assertEqual(None, level2_1_1.cell_sets)
        self.assertEqual(len(level2_1_1.children), 4)
        self.assertEqual(level2_1_1.parent.name, "GRID_L1_1_1")
        # level2_2_1
        self.assertEqual(None, level2_2_1.vertices)
        self.assertEqual(None, level2_2_1.cells)
        self.assertEqual(None, level2_2_1.cell_sets)
        self.assertEqual(len(level2_2_1.children), 4)
        self.assertEqual(level2_2_1.parent.name, "GRID_L1_1_1")
        # level2_1_2
        self.assertEqual(None, level2_1_2.vertices)
        self.assertEqual(None, level2_1_2.cells)
        self.assertEqual(None, level2_1_2.cell_sets)
        self.assertEqual(len(level2_1_2.children), 4)
        self.assertEqual(level2_1_2.parent.name, "GRID_L1_1_1")
        # level2_2_2
        self.assertEqual(None, level2_2_2.vertices)
        self.assertEqual(None, level2_2_2.cells)
        self.assertEqual(None, level2_2_2.cell_sets)
        self.assertEqual(len(level2_2_2.children), 4)
        self.assertEqual(level2_2_2.parent.name, "GRID_L1_1_1")
        # level 3
        level3_1_1, level3_2_1, level3_1_2, level3_2_2 = level2_1_1.children
        self.assertEqual(level3_1_1.name, "GRID_L3_1_1")
        self.assertEqual(level3_2_1.name, "GRID_L3_2_1")
        self.assertEqual(level3_1_2.name, "GRID_L3_1_2")
        self.assertEqual(level3_2_2.name, "GRID_L3_2_2")
        level3_3_1, level3_4_1, level3_3_2, level3_4_2 = level2_2_1.children
        self.assertEqual(level3_3_1.name, "GRID_L3_3_1")
        self.assertEqual(level3_4_1.name, "GRID_L3_4_1")
        self.assertEqual(level3_3_2.name, "GRID_L3_3_2")
        self.assertEqual(level3_4_2.name, "GRID_L3_4_2")
        level3_1_3, level3_2_3, level3_1_4, level3_2_4 = level2_1_2.children
        self.assertEqual(level3_1_3.name, "GRID_L3_1_3")
        self.assertEqual(level3_2_4.name, "GRID_L3_2_4")
        self.assertEqual(level3_1_3.name, "GRID_L3_1_3")
        self.assertEqual(level3_2_4.name, "GRID_L3_2_4")
        level3_3_3, level3_4_3, level3_3_4, level3_4_4 = level2_2_2.children
        self.assertEqual(level3_3_3.name, "GRID_L3_3_3")
        self.assertEqual(level3_4_4.name, "GRID_L3_4_4")
        self.assertEqual(level3_3_3.name, "GRID_L3_3_3")
        self.assertEqual(level3_4_4.name, "GRID_L3_4_4")
        # level3_1_1
        test_mesh = level3_1_1
        ref_verts = three_level_l3_1_1_vertices
        ref_cells = three_level_l3_1_1_cells
        test_verts = test_mesh.vertices
        test_cells = test_mesh.cells
        # verts
        for v in list(ref_verts.keys()):
            for i in range(3):
                self.assertEqual(test_verts[v][i], test_verts[v][i])
        # cells
        for cell_type in list(ref_cells.keys()):
            cell_ids = list(ref_cells[cell_type].keys())
            for cell_id in cell_ids:
                vert_ids = ref_cells[cell_type][cell_id]
                for v in range(len(vert_ids)):
                    self.assertEqual(
                        ref_cells[cell_type][cell_id][v], test_cells[cell_type][cell_id][v]
                    )
        # cell_sets
        self.assertEqual(test_mesh.cell_sets, {})

        # level3_1_2
        test_mesh = level3_1_2
        ref_verts = three_level_l3_1_2_vertices
        ref_cells = three_level_l3_1_2_cells
        test_verts = test_mesh.vertices
        test_cells = test_mesh.cells
        # verts
        for v in list(ref_verts.keys()):
            for i in range(3):
                self.assertEqual(test_verts[v][i], test_verts[v][i])
        # cells
        for cell_type in list(ref_cells.keys()):
            cell_ids = list(ref_cells[cell_type].keys())
            for cell_id in cell_ids:
                vert_ids = ref_cells[cell_type][cell_id]
                for v in range(len(vert_ids)):
                    self.assertEqual(
                        ref_cells[cell_type][cell_id][v], test_cells[cell_type][cell_id][v]
                    )
        # cell_sets
        self.assertEqual(test_mesh.cell_sets, {})

        # level3_1_3
        test_mesh = level3_1_3
        ref_verts = three_level_l3_1_3_vertices
        ref_cells = three_level_l3_1_3_cells
        test_verts = test_mesh.vertices
        test_cells = test_mesh.cells
        # verts
        for v in list(ref_verts.keys()):
            for i in range(3):
                self.assertEqual(test_verts[v][i], test_verts[v][i])
        # cells
        for cell_type in list(ref_cells.keys()):
            cell_ids = list(ref_cells[cell_type].keys())
            for cell_id in cell_ids:
                vert_ids = ref_cells[cell_type][cell_id]
                for v in range(len(vert_ids)):
                    self.assertEqual(
                        ref_cells[cell_type][cell_id][v], test_cells[cell_type][cell_id][v]
                    )
        # cell_sets
        self.assertEqual(test_mesh.cell_sets, {})

        # Alright, checking all 16 is too much. One more
        # level3_3_3
        test_mesh = level3_3_3
        ref_verts = three_level_l3_3_3_vertices
        ref_cells = three_level_l3_3_3_cells
        test_verts = test_mesh.vertices
        test_cells = test_mesh.cells
        # verts
        for v in list(ref_verts.keys()):
            for i in range(3):
                self.assertEqual(test_verts[v][i], test_verts[v][i])
        # cells
        for cell_type in list(ref_cells.keys()):
            cell_ids = list(ref_cells[cell_type].keys())
            for cell_id in cell_ids:
                vert_ids = ref_cells[cell_type][cell_id]
                for v in range(len(vert_ids)):
                    self.assertEqual(
                        ref_cells[cell_type][cell_id][v], test_cells[cell_type][cell_id][v]
                    )
        # cell_sets
        self.assertEqual(test_mesh.cell_sets, {})
