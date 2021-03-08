"""Test reading and writing of XDMF files."""

import os
import sys
from unittest import TestCase

import h5py
import numpy as np
from mesh_data import (
    three_level_grid_cell_sets,
    three_level_grid_cells,
    three_level_grid_vertices,
    two_disks_tri6_quad8_cells,
    two_disks_tri6_quad8_vertices,
)

import mocmg
import mocmg.mesh

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from testing_utils import captured_output

two_disks_tri6_quad8_cells_h5_ref = np.concatenate(
    [
        np.array([36]),
        np.array([5, 31, 4, 32, 33, 11]) - 1,
        np.array([36]),
        np.array([6, 31, 5, 34, 32, 12]) - 1,
        np.array([36]),
        np.array([4, 31, 3, 33, 35, 10]) - 1,
        np.array([36]),
        np.array([7, 31, 6, 36, 34, 13]) - 1,
        np.array([36]),
        np.array([3, 31, 1, 35, 37, 9]) - 1,
        np.array([36]),
        np.array([8, 31, 7, 38, 36, 14]) - 1,
        np.array([36]),
        np.array([1, 31, 8, 37, 38, 15]) - 1,
        np.array([37]),
        np.array([19, 20, 39, 41, 27, 42, 43, 44]) - 1,
        np.array([37]),
        np.array([2, 16, 39, 40, 23, 45, 46, 47]) - 1,
        np.array([37]),
        np.array([40, 39, 20, 21, 46, 42, 28, 48]) - 1,
        np.array([37]),
        np.array([41, 39, 16, 17, 43, 45, 24, 49]) - 1,
        np.array([37]),
        np.array([17, 18, 19, 41, 25, 26, 44, 49]) - 1,
        np.array([37]),
        np.array([21, 22, 2, 40, 29, 30, 47, 48]) - 1,
    ]
)


class TestXDMFIO(TestCase):
    """Test the XDMF IO functions."""

    def test_uniform_grid_triangle_only(self):
        """Test writing file with triangle cells only and no cell sets."""
        filename = "uniform_grid_triangle_only"
        vertices = {
            1: np.array([1.0, 0.0, 0.0]),
            2: np.array([0.62348980185873, 0.78183148246803, 0.0]),
            3: np.array([-0.22252093395631, 0.97492791218182, 0.0]),
            4: np.array([-0.90096886790242, 0.43388373911756, 0.0]),
            5: np.array([-0.90096886790242, -0.43388373911756, 0.0]),
            6: np.array([-0.22252093395631, -0.97492791218182, 0.0]),
            7: np.array([0.62348980185873, -0.78183148246803, 0.0]),
            8: np.array([1.5202888403297e-17, -7.7860210853066e-18, 0.0]),
        }
        cells = {
            "triangle": {
                1: np.array([4, 8, 3]),
                2: np.array([5, 8, 4]),
                3: np.array([3, 8, 2]),
                4: np.array([6, 8, 5]),
                5: np.array([2, 8, 1]),
                6: np.array([7, 8, 6]),
                7: np.array([1, 8, 7]),
            },
        }
        out_ref = [
            "INFO      : mocmg.mesh.xdmf_IO - Writing mesh data to XDMF file '"
            + filename
            + ".xdmf'."
        ]
        err_ref = []
        with captured_output() as (out, err):
            mocmg.initialize()
            mesh = mocmg.mesh.Mesh(vertices, cells)
            mocmg.mesh.write_xdmf_file(filename + ".xdmf", mesh)

        # message
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        # strip times
        out, err = [line.split(None, 1)[1] for line in out], [
            line.split(None, 1)[1] for line in err
        ]
        self.assertEqual(out, out_ref)
        self.assertEqual(err, err_ref)

        # Check xdmf
        ref_file = open("./tests/mesh/xdmf_files/" + filename + ".xdmf", "r")
        test_file = open(filename + ".xdmf", "r")
        ref_lines = ref_file.readlines()
        test_lines = test_file.readlines()
        ref_file.close()
        test_file.close()
        self.assertEqual(len(ref_lines), len(test_lines))
        for i in range(len(ref_lines)):
            self.assertEqual(ref_lines[i], test_lines[i])

        # Check h5
        with h5py.File(filename + ".h5", "r") as f:
            vertices_h5 = np.array(f.get(filename + "/vertices"))
            cells_h5 = np.array(f.get(filename + "/cells"))
        # Vertices
        for i, coord in enumerate(vertices.values()):
            for j in range(len(coord)):
                self.assertEqual(coord[j], vertices_h5[i][j])
        # Cells
        for cell_type in cells.values():
            for j, cell in enumerate(cell_type.values()):
                for k in range(len(cell)):
                    self.assertEqual(cell[k], cells_h5[j][k])

        os.remove(filename + ".xdmf")
        os.remove(filename + ".h5")

    def test_uniform_grid_triangle_only_with_name(self):
        """Test writing file with triangle cells only and no cell sets, with named mesh."""
        filename = "uniform_grid_triangle_only_with_name"
        vertices = {
            1: np.array([1.0, 0.0, 0.0]),
            2: np.array([0.62348980185873, 0.78183148246803, 0.0]),
            3: np.array([-0.22252093395631, 0.97492791218182, 0.0]),
            4: np.array([-0.90096886790242, 0.43388373911756, 0.0]),
            5: np.array([-0.90096886790242, -0.43388373911756, 0.0]),
            6: np.array([-0.22252093395631, -0.97492791218182, 0.0]),
            7: np.array([0.62348980185873, -0.78183148246803, 0.0]),
            8: np.array([1.5202888403297e-17, -7.7860210853066e-18, 0.0]),
        }
        cells = {
            "triangle": {
                1: np.array([4, 8, 3]),
                2: np.array([5, 8, 4]),
                3: np.array([3, 8, 2]),
                4: np.array([6, 8, 5]),
                5: np.array([2, 8, 1]),
                6: np.array([7, 8, 6]),
                7: np.array([1, 8, 7]),
            },
        }
        out_ref = [
            "INFO      : mocmg.mesh.xdmf_IO - Writing mesh data to XDMF file '"
            + filename
            + ".xdmf'."
        ]
        err_ref = []
        with captured_output() as (out, err):
            mocmg.initialize()
            mesh = mocmg.mesh.Mesh(vertices, cells, name="named_mesh")
            mocmg.mesh.write_xdmf_file(filename + ".xdmf", mesh)

        # message
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        # strip times
        out, err = [line.split(None, 1)[1] for line in out], [
            line.split(None, 1)[1] for line in err
        ]
        self.assertEqual(out, out_ref)
        self.assertEqual(err, err_ref)

        # Check xdmf
        ref_file = open("./tests/mesh/xdmf_files/" + filename + ".xdmf", "r")
        test_file = open(filename + ".xdmf", "r")
        ref_lines = ref_file.readlines()
        test_lines = test_file.readlines()
        ref_file.close()
        test_file.close()
        self.assertEqual(len(ref_lines), len(test_lines))
        for i in range(len(ref_lines)):
            self.assertEqual(ref_lines[i], test_lines[i])

        # Check h5
        with h5py.File(filename + ".h5", "r") as f:
            vertices_h5 = np.array(f.get("/named_mesh/vertices"))
            cells_h5 = np.array(f.get("/named_mesh/cells"))
        # Vertices
        for i, coord in enumerate(vertices.values()):
            for j in range(len(coord)):
                self.assertEqual(coord[j], vertices_h5[i][j])
        # Cells
        for cell_type in cells.values():
            for j, cell in enumerate(cell_type.values()):
                for k in range(len(cell)):
                    self.assertEqual(cell[k], cells_h5[j][k])

        os.remove(filename + ".xdmf")
        os.remove(filename + ".h5")

    def test_mixed_topology_no_cell_sets(self):
        """Test writing xdmf file with mixed topology and no cell sets."""
        filename = "mixed_topology"
        vertices = {
            1: np.array([0.0, 0.0, 0.0]),
            2: np.array([1.0, 1.0, 0.0]),
            3: np.array([1.0, 0.0, 0.0]),
            4: np.array([0.0, -1.0, 0.0]),
            5: np.array([1.0, -1.0, 0.0]),
            6: np.array([1.0, -2.0, 0.0]),
            7: np.array([2.0, -2.0, 0.0]),
            8: np.array([3.0, -2.0, 0.0]),
            9: np.array([2.5, -0.5, 0.0]),
        }
        cells = {
            "triangle": {
                1: np.array([1, 3, 2]),
            },
            "quad": {
                2: np.array([4, 5, 3, 1]),
            },
            "triangle6": {
                3: np.array([6, 8, 3, 7, 9, 5]),
            },
        }
        cells_h5_ref = np.concatenate(
            [
                np.array([4]),
                np.array([1, 3, 2]) - 1,
                np.array([5]),
                np.array([4, 5, 3, 1]) - 1,
                np.array([36]),
                np.array([6, 8, 3, 7, 9, 5]) - 1,
            ]
        )
        out_ref = [
            "INFO      : mocmg.mesh.xdmf_IO - Writing mesh data to XDMF file '"
            + filename
            + ".xdmf'."
        ]
        err_ref = []
        with captured_output() as (out, err):
            mocmg.initialize()
            mesh = mocmg.mesh.Mesh(vertices, cells)
            mocmg.mesh.write_xdmf_file(filename + ".xdmf", mesh)

        # message
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()

        # strip times
        out, err = [line.split(None, 1)[1] for line in out], [
            line.split(None, 1)[1] for line in err
        ]
        self.assertEqual(out, out_ref)
        self.assertEqual(err, err_ref)

        # Check xdmf
        ref_file = open("./tests/mesh/xdmf_files/" + filename + ".xdmf", "r")
        test_file = open(filename + ".xdmf", "r")
        ref_lines = ref_file.readlines()
        test_lines = test_file.readlines()
        ref_file.close()
        test_file.close()
        self.assertEqual(len(ref_lines), len(test_lines))
        for i in range(len(ref_lines)):
            self.assertEqual(ref_lines[i], test_lines[i])

        # Check h5
        with h5py.File(filename + ".h5", "r") as f:
            vertices_h5 = np.array(f.get(filename + "/vertices"))
            cells_h5 = np.array(f.get(filename + "/cells"))
        # Vertices
        for i, coord in enumerate(vertices.values()):
            for j in range(len(coord)):
                self.assertEqual(vertices_h5[i][j], coord[j])
        # Cells
        for i in range(len(cells_h5_ref)):
            self.assertEqual(cells_h5[i], cells_h5_ref[i])

        os.remove(filename + ".xdmf")
        os.remove(filename + ".h5")

    def test_disks_mixed_topology_no_cell_sets(self):
        """Test writing xdmf file for two disks with mixed topology and no cell sets."""
        filename = "mixed_topology_disks"
        vertices = two_disks_tri6_quad8_vertices
        cells = two_disks_tri6_quad8_cells
        cells_h5_ref = two_disks_tri6_quad8_cells_h5_ref
        out_ref = [
            "INFO      : mocmg.mesh.xdmf_IO - Writing mesh data to XDMF file '"
            + filename
            + ".xdmf'."
        ]
        err_ref = []
        with captured_output() as (out, err):
            mocmg.initialize()
            mesh = mocmg.mesh.Mesh(vertices, cells)
            mocmg.mesh.write_xdmf_file(filename + ".xdmf", mesh)

        # message
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()

        # strip times
        out, err = [line.split(None, 1)[1] for line in out], [
            line.split(None, 1)[1] for line in err
        ]
        self.assertEqual(out, out_ref)
        self.assertEqual(err, err_ref)

        # Check xdmf
        ref_file = open("./tests/mesh/xdmf_files/" + filename + ".xdmf", "r")
        test_file = open(filename + ".xdmf", "r")
        ref_lines = ref_file.readlines()
        test_lines = test_file.readlines()
        ref_file.close()
        test_file.close()
        self.assertEqual(len(ref_lines), len(test_lines))
        for i in range(len(ref_lines)):
            self.assertEqual(ref_lines[i], test_lines[i])

        # Check h5
        with h5py.File(filename + ".h5", "r") as f:
            vertices_h5 = np.array(f.get(filename + "/vertices"))
            cells_h5 = np.array(f.get(filename + "/cells"))
        # Vertices
        for i, coord in enumerate(vertices.values()):
            for j in range(len(coord)):
                self.assertEqual(vertices_h5[i][j], coord[j])
        # Cells
        for i in range(len(cells_h5_ref)):
            self.assertEqual(cells_h5[i], cells_h5_ref[i])

        os.remove(filename + ".xdmf")
        os.remove(filename + ".h5")

    def test_disks_mixed_topology_with_materials(self):
        """Test writing xdmf file for two disks with mixed topology and material only cell sets."""
        filename = "mixed_topology_disks_with_materials"
        vertices = two_disks_tri6_quad8_vertices
        cells = two_disks_tri6_quad8_cells
        cells_h5_ref = two_disks_tri6_quad8_cells_h5_ref
        cell_sets = {
            "Material DISK1": np.array([1, 2, 3, 4, 5, 6, 7]),
            "Material DISK2": np.array([8, 9, 10, 11, 12, 13]),
        }
        out_ref = [
            "INFO      : mocmg.mesh.xdmf_IO - Writing mesh data to XDMF file '"
            + filename
            + ".xdmf'."
        ]
        err_ref = []
        with captured_output() as (out, err):
            mocmg.initialize()
            mesh = mocmg.mesh.Mesh(vertices, cells, cell_sets=cell_sets)
            mocmg.mesh.write_xdmf_file(filename + ".xdmf", mesh)

        # message
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        # strip times
        out, err = [line.split(None, 1)[1] for line in out], [
            line.split(None, 1)[1] for line in err
        ]
        self.assertEqual(out, out_ref)
        self.assertEqual(err, err_ref)

        # Check xdmf
        ref_file = open("./tests/mesh/xdmf_files/" + filename + ".xdmf", "r")
        test_file = open(filename + ".xdmf", "r")
        ref_lines = ref_file.readlines()
        test_lines = test_file.readlines()
        ref_file.close()
        test_file.close()
        self.assertEqual(len(ref_lines), len(test_lines))
        for i in range(len(ref_lines)):
            self.assertEqual(ref_lines[i], test_lines[i])

        # Check h5
        with h5py.File(filename + ".h5", "r") as f:
            vertices_h5 = np.array(f.get(filename + "/vertices"))
            cells_h5 = np.array(f.get(filename + "/cells"))
            materials_h5 = np.array(f.get(filename + "/material_id"))
        # Vertices
        for i, coord in enumerate(vertices.values()):
            for j in range(len(coord)):
                self.assertEqual(vertices_h5[i][j], coord[j])
        # Cells
        for i in range(len(cells_h5_ref)):
            self.assertEqual(cells_h5[i], cells_h5_ref[i])

        # Material
        for i in range(7):
            self.assertEqual(materials_h5[i], 0)
        for i in range(7, 13):
            self.assertEqual(materials_h5[i], 1)

        os.remove(filename + ".xdmf")
        os.remove(filename + ".h5")

    def test_with_bad_type(self):
        """Test writing a non-mesh."""
        filename = "bad_type"
        out_ref = [
            "INFO      : mocmg.mesh.xdmf_IO - Writing mesh data to XDMF file '"
            + filename
            + ".xdmf'."
        ]
        err_ref = ["ERROR     : mocmg.mesh.xdmf_IO - Invalid type given as input."]
        with self.assertRaises(SystemExit):
            with captured_output() as (out, err):
                mocmg.initialize()
                mesh = [1]
                mocmg.mesh.write_xdmf_file(filename + ".xdmf", mesh)

        # message
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        # strip times
        out, err = [line.split(None, 1)[1] for line in out], [
            line.split(None, 1)[1] for line in [err[0]]
        ]
        self.assertEqual(out, out_ref)
        self.assertEqual(err, err_ref)

    def test_disks_mixed_topology_with_incomplete_materials(self):
        """Test writing xdmf file that only has materials for some cells."""
        filename = "mixed_topology_disks_with_incomplete_materials"
        vertices = two_disks_tri6_quad8_vertices
        cells = two_disks_tri6_quad8_cells
        cell_sets = {
            "Material DISK1": np.array([1, 2, 3, 4, 5, 6, 7]),
            "Material DISK2": np.array([8, 9, 10, 11]),
        }
        out_ref = [
            "INFO      : mocmg.mesh.xdmf_IO - Writing mesh data to XDMF file '"
            + filename
            + ".xdmf'."
        ]
        err_ref = [
            "ERROR     : mocmg.mesh.xdmf_IO - Total number of cells (13) not "
            + "equal to number of cells with a material (11)."
        ]
        with self.assertRaises(SystemExit):
            with captured_output() as (out, err):
                mocmg.initialize()
                mesh = mocmg.mesh.Mesh(vertices, cells, cell_sets=cell_sets)
                mocmg.mesh.write_xdmf_file(filename + ".xdmf", mesh)

        # message
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        # strip times
        out, err = [line.split(None, 1)[1] for line in out], [
            line.split(None, 1)[1] for line in [err[0]]
        ]
        self.assertEqual(out, out_ref)
        self.assertEqual(err, err_ref)

        os.remove(filename + ".h5")

    def test_three_level_grid(self):
        """Test writing a mesh with three grid levels and no materials."""
        name = "three_lvl_grid"
        filename = "three_level_grid"
        ref_vertices = three_level_grid_vertices
        ref_cells = three_level_grid_cells
        ref_cell_sets = three_level_grid_cell_sets
        mesh = mocmg.mesh.Mesh(ref_vertices, ref_cells, ref_cell_sets, name=name)
        mocmg.mesh.write_xdmf_file(filename + ".xdmf", mesh)

        # Check xdmf
        ref_file = open("./tests/mesh/xdmf_files/" + filename + ".xdmf", "r")
        test_file = open(filename + ".xdmf", "r")
        ref_lines = ref_file.readlines()
        test_lines = test_file.readlines()
        ref_file.close()
        test_file.close()
        self.assertEqual(len(ref_lines), len(test_lines))
        for i in range(len(ref_lines)):
            self.assertEqual(ref_lines[i], test_lines[i])

        # Check h5
        # Reference file
        with h5py.File("./tests/mesh/xdmf_files/" + filename + ".h5", "r") as f:
            cells_h5_ref = np.array(f.get(name + "/cells"))
        # Test file
        with h5py.File(filename + ".h5", "r") as f:
            vertices_h5 = np.array(f.get(name + "/vertices"))
            cells_h5 = np.array(f.get(name + "/cells"))
        # Vertices
        for i, coord in enumerate(ref_vertices.values()):
            for j in range(len(coord)):
                self.assertEqual(vertices_h5[i][j], coord[j])
        # Cells
        for i in range(len(cells_h5_ref)):
            self.assertEqual(cells_h5[i], cells_h5_ref[i])

        # Cell sets
        cell_id_map = {}
        cell_ctr = 0
        for cell_type in ref_cells.keys():
            for cell_id in ref_cells[cell_type].keys():
                cell_id_map[cell_id] = cell_ctr
                cell_ctr = cell_ctr + 1

        with h5py.File(filename + ".h5", "r") as f:
            for set_name in ref_cell_sets.keys():
                set_cells_h5 = np.array(f.get(name + "/" + set_name))
                for i, cell_id in enumerate(ref_cell_sets[set_name]):
                    self.assertEqual(cell_id_map[cell_id], set_cells_h5[i])

        os.remove(filename + ".xdmf")
        os.remove(filename + ".h5")

    def test_gridmesh_three_level_grid(self):
        """Test writing a GridMesh with three grid levels and no materials."""
        name = "three_lvl_grid"
        filename = "gridmesh_three_level_grid"
        ref_vertices = three_level_grid_vertices
        ref_cells = three_level_grid_cells
        ref_cell_sets = three_level_grid_cell_sets
        mesh = mocmg.mesh.Mesh(ref_vertices, ref_cells, ref_cell_sets, name=name)
        gridmesh = mocmg.mesh.make_gridmesh(mesh)
        mocmg.mesh.write_xdmf_file(filename + ".xdmf", gridmesh)

        # Check xdmf
        ref_file = open("./tests/mesh/xdmf_files/" + filename + ".xdmf", "r")
        test_file = open(filename + ".xdmf", "r")
        ref_lines = ref_file.readlines()
        test_lines = test_file.readlines()
        ref_file.close()
        test_file.close()
        self.assertEqual(len(ref_lines), len(test_lines))
        for i in range(len(ref_lines)):
            self.assertEqual(ref_lines[i], test_lines[i])

        # Check h5
        # Reference file
        with h5py.File("./tests/mesh/xdmf_files/" + filename + ".h5", "r") as f:
            cells_h5_ref = np.array(f.get(name + "/cells"))
        # Test file
        with h5py.File(filename + ".h5", "r") as f:
            vertices_h5 = np.array(f.get(name + "/vertices"))
            cells_h5 = np.array(f.get(name + "/cells"))
        # Vertices
        for i, coord in enumerate(ref_vertices.values()):
            for j in range(len(coord)):
                self.assertEqual(vertices_h5[i][j], coord[j])
        # Cells
        for i in range(len(cells_h5_ref)):
            self.assertEqual(cells_h5[i], cells_h5_ref[i])

        # Cell sets
        cell_id_map = {}
        cell_ctr = 0
        for cell_type in ref_cells.keys():
            for cell_id in ref_cells[cell_type].keys():
                cell_id_map[cell_id] = cell_ctr
                cell_ctr = cell_ctr + 1

        with h5py.File(filename + ".h5", "r") as f:
            for set_name in ref_cell_sets.keys():
                set_cells_h5 = np.array(f.get(name + "/" + set_name))
                for i, cell_id in enumerate(ref_cell_sets[set_name]):
                    self.assertEqual(cell_id_map[cell_id], set_cells_h5[i])

        os.remove(filename + ".xdmf")
        os.remove(filename + ".h5")
