"""Test the grid mesh class and its functions."""
from unittest import TestCase

import numpy as np
from mesh_data import (
    linear_quadrilateral_cell_sets,
    linear_quadrilateral_cells,
    linear_quadrilateral_vertices,
    linear_triangle_cell_sets,
    linear_triangle_cells,
    linear_triangle_vertices,
    pin_1_cells,
    pin_1_vertices,
    pin_2_cells,
    pin_2_vertices,
    quadratic_quadrilateral_cell_sets,
    quadratic_quadrilateral_cells,
    quadratic_quadrilateral_vertices,
    quadratic_triangle_cell_sets,
    quadratic_triangle_cells,
    quadratic_triangle_vertices,
    two_disks_tri6_quad8_cells,
    two_disks_tri6_quad8_vertices,
)

import mocmg
import mocmg.mesh


class TestGridMesh(TestCase):
    """Test the grid mesh class and its functions."""

    def test_grid_linear_triangle(self):
        """Test the mesh class functions on a linear triangle mesh."""
        ref_vertices = linear_triangle_vertices
        ref_cells = linear_triangle_cells
        ref_cell_sets = linear_triangle_cell_sets
        mocmg.initialize()
        mesh = mocmg.mesh.GridMesh(ref_vertices, ref_cells, ref_cell_sets)
        self.assertEqual(mesh.vertices, ref_vertices)
        self.assertEqual(mesh.cells, ref_cells)
        self.assertEqual(mesh.cell_sets, ref_cell_sets)
        # get_cells
        cell_set = mesh.get_cells("DISK")
        self.assertTrue(np.array_equal(cell_set, linear_triangle_cell_sets["DISK"]))
        # Try w/ name that doesnt exist.
        with self.assertRaises(SystemExit):
            cell_set = mesh.get_cells("BAD NAME")
        # get_cell_area
        cell_area_ref = 0.210453
        cell_area = mesh.get_cell_area(1)
        self.assertAlmostEqual(cell_area, cell_area_ref, 6)
        # Try will cell that doesnt exist
        with self.assertRaises(SystemExit):
            cell_area = mesh.get_cell_area(-1)
        # get_set_area
        set_area_ref = 2.828427
        set_area = mesh.get_set_area("DISK")
        self.assertAlmostEqual(set_area, set_area_ref, 6)
        # get_vertices_for_cells
        verts_from_cells = mesh.get_vertices_for_cells([1, 2, 3])
        verts_from_cells_ref = [[1, 16, 13], [9, 16, 1], [12, 15, 4]]
        for i, vset in enumerate(verts_from_cells_ref):
            for j, v in enumerate(vset):
                self.assertEqual(v, verts_from_cells[i][j])
        # cell that doesnt exist
        with self.assertRaises(SystemExit):
            verts_from_cells = mesh.get_vertices_for_cells([1111111])
        # get_vertices for cell set
        verts_from_cell_set_name = mesh.get_vertices("DISK")
        verts_from_cell_set_name_ref = [1, 3, 4, 7, 9, 10, 11, 12, 13, 14, 15, 16]
        for i, vert in enumerate(verts_from_cell_set_name_ref):
            self.assertEqual(vert, verts_from_cell_set_name[i])
        # cell set that doesnt exist
        with self.assertRaises(SystemExit):
            verts_from_cell_set_name = mesh.get_vertices("NO_NAME")

    def test_grid_quadratic_triangle(self):
        """Test the mesh class functions on a quadratic triangle mesh."""
        ref_vertices = quadratic_triangle_vertices
        ref_cells = quadratic_triangle_cells
        ref_cell_sets = quadratic_triangle_cell_sets
        mocmg.initialize()
        mesh = mocmg.mesh.GridMesh(ref_vertices, ref_cells, ref_cell_sets, name="quad_tri_name")
        self.assertEqual(mesh.vertices, ref_vertices)
        self.assertEqual(mesh.cells, ref_cells)
        self.assertEqual(mesh.cell_sets, ref_cell_sets)
        # get_cells
        cell_set = mesh.get_cells("DISK")
        self.assertTrue(np.array_equal(cell_set, quadratic_triangle_cell_sets["DISK"]))
        # get_cell_area
        cell_area_ref = 0.261949
        cell_area = mesh.get_cell_area(2)
        self.assertAlmostEqual(cell_area, cell_area_ref, 6)
        # get_set_area
        set_area_ref = 3.1391725
        set_area = mesh.get_set_area("DISK")
        self.assertAlmostEqual(set_area, set_area_ref, 6)
        # name
        self.assertEqual(mesh.name, "quad_tri_name")

    def test_grid_linear_quadrilateral(self):
        """Test the mesh class functions on a linear quadrilateral mesh."""
        ref_vertices = linear_quadrilateral_vertices
        ref_cells = linear_quadrilateral_cells
        ref_cell_sets = linear_quadrilateral_cell_sets
        mocmg.initialize()
        mesh = mocmg.mesh.GridMesh(ref_vertices, ref_cells, ref_cell_sets)
        self.assertEqual(mesh.vertices, ref_vertices)
        self.assertEqual(mesh.cells, ref_cells)
        self.assertEqual(mesh.cell_sets, ref_cell_sets)
        # get_cells
        cell_set = mesh.get_cells("DISK")
        self.assertTrue(np.array_equal(cell_set, linear_quadrilateral_cell_sets["DISK"]))
        # get_cell_area
        cell_area_ref = 0.0874078
        cell_area = mesh.get_cell_area(1)
        self.assertAlmostEqual(cell_area, cell_area_ref, 6)
        # get_set_area
        set_area_ref = 3.0614675
        set_area = mesh.get_set_area("DISK")
        self.assertAlmostEqual(set_area, set_area_ref, 6)

    def test_grid_quadratic_quadrilateral(self):
        """Test the mesh class functions on a quadratic quadrilateral mesh."""
        ref_vertices = quadratic_quadrilateral_vertices
        ref_cells = quadratic_quadrilateral_cells
        ref_cell_sets = quadratic_quadrilateral_cell_sets
        mocmg.initialize()
        mesh = mocmg.mesh.GridMesh(ref_vertices, ref_cells, ref_cell_sets)
        self.assertEqual(mesh.vertices, ref_vertices)
        self.assertEqual(mesh.cells, ref_cells)
        self.assertEqual(mesh.cell_sets, ref_cell_sets)
        # get_cells
        cell_set = mesh.get_cells("DISK")
        self.assertTrue(np.array_equal(cell_set, quadratic_quadrilateral_cell_sets["DISK"]))
        # get_cell_area
        cell_area_ref = 0.7847974
        cell_area = mesh.get_cell_area(1)
        self.assertAlmostEqual(cell_area, cell_area_ref, 6)
        # get_set_area
        set_area_ref = 3.1391907
        set_area = mesh.get_set_area("DISK")
        self.assertAlmostEqual(set_area, set_area_ref, 6)

    def test_grid_get_cell_area(self):
        """Test the get_cell_area function."""
        verts = {
            1: np.array([0.0, 0.0, 0.0]),
            2: np.array([1.0, 0.0, 0.0]),
            3: np.array([1.0, 1.0, 0.0]),
            4: np.array([0.0, 1.0, 0.0]),
            5: np.array([0.5, 0.0, 0.0]),
            6: np.array([1.25, 0.5, 0.0]),
            7: np.array([0.5, 1.0, 0.0]),
            8: np.array([0.25, 0.5, 0.0]),
        }
        cells = {
            "quad8": {
                1: np.array([1, 2, 3, 4, 5, 6, 7, 8]),
            },
        }
        mocmg.initialize()
        mesh = mocmg.mesh.GridMesh(verts, cells)
        cell_area = mesh.get_cell_area(1)
        self.assertAlmostEqual(cell_area, 1.0, 6)

    def test_grid_on_mixed_topology(self):
        """Test the mesh class functions on a mixed topology mesh."""
        mocmg.initialize()
        ref_vertices = two_disks_tri6_quad8_vertices
        ref_cells = two_disks_tri6_quad8_cells
        mesh = mocmg.mesh.GridMesh(ref_vertices, ref_cells)
        self.assertEqual(mesh.vertices, ref_vertices)
        self.assertEqual(mesh.cells, ref_cells)
        # get_vertices_for_cells
        verts_from_cells = mesh.get_vertices_for_cells([1, 8])
        verts_from_cells_ref = [[5, 31, 4, 32, 33, 11], [19, 20, 39, 41, 27, 42, 43, 44]]
        for i, vset in enumerate(verts_from_cells_ref):
            for j, v in enumerate(vset):
                self.assertEqual(v, verts_from_cells[i][j])

    def test_with_subsets(self):
        """Initialize and test a grid mesh with subsets."""
        mocmg.initialize()
        mesh1 = mocmg.mesh.GridMesh(pin_1_vertices, pin_1_cells, name="pin1")
        self.assertEqual(mesh1.vertices, pin_1_vertices)
        self.assertEqual(mesh1.cells, pin_1_cells)
        mesh2 = mocmg.mesh.GridMesh(pin_2_vertices, pin_2_cells, name="pin2")
        self.assertEqual(mesh2.vertices, pin_2_vertices)
        self.assertEqual(mesh2.cells, pin_2_cells)
        # Init with normal data and subset
        with self.assertRaises(SystemExit):
            mocmg.mesh.GridMesh(pin_1_vertices, pin_1_cells, subset_meshes=[mesh1, mesh2])
        # init with subsets
        both_pins_mesh = mocmg.mesh.GridMesh(subset_meshes=[mesh1, mesh2], name="both_pins")
        # Check relationships
        ref_names = ["pin1", "pin2"]
        for i, mesh in enumerate(both_pins_mesh.subset_meshes):
            name = mesh.name
            self.assertEqual(name, ref_names[i])
            self.assertEqual("both_pins", mesh.superset_mesh.name)
