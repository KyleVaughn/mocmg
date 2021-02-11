"""Test reading and writing of XDMF files."""

import hashlib
import os
import sys
from unittest import TestCase

import h5py
import numpy as np

import mocmg
import mocmg.mesh

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from testing_utils import captured_output


class TestXDMFIO(TestCase):
    """Test the XDMF IO functions."""

    def test_uniform_grid_triangle_only(self):
        """Test writing file with triangle cells only and no cell sets."""
        filename = "uniform_grid_triangle_only"
        xml_sha256 = "0c0b9c758820d77f4c03e7e777ff1f7c19d04076cb4cb333a6eec98444f4786b"
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

        # Check xml using sha256
        xml_hash = hashlib.sha256(open(filename + ".xdmf", "rb").read()).hexdigest()
        self.assertEqual(xml_hash, xml_sha256)

        # Check h5
        with h5py.File(filename + ".h5", "r") as f:
            vertices_h5 = np.array(f.get(filename + "/VERTICES"))
            cells_h5 = np.array(f.get(filename + "/CELLS"))
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
        xml_sha256 = "97c2dd7b926ec7856e10855f0dabbe6e4dd48a03c739c91b3497c7a9efdbb5be"
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

        # Check xml using sha256
        xml_hash = hashlib.sha256(open(filename + ".xdmf", "rb").read()).hexdigest()
        self.assertEqual(xml_hash, xml_sha256)

        # Check h5
        with h5py.File(filename + ".h5", "r") as f:
            vertices_h5 = np.array(f.get(filename + "/VERTICES"))
            cells_h5 = np.array(f.get(filename + "/CELLS"))
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
        xml_sha256 = "d9556a5924ee1142bad35b1d58771898b8be2680c47d8e490e7e669f337afe4f"
        vertices = {
            1: np.array([1.0, 0.0, 0.0]),
            2: np.array([3.0, 0.0, 0.0]),
            3: np.array([0.62348980185873, 0.78183148246803, 0]),
            4: np.array([-0.22252093395631, 0.97492791218182, 0]),
            5: np.array([-0.90096886790242, 0.43388373911756, 0]),
            6: np.array([-0.90096886790242, -0.43388373911756, 0]),
            7: np.array([-0.22252093395631, -0.97492791218182, 0]),
            8: np.array([0.62348980185873, -0.78183148246803, 0]),
            9: np.array([0.90096886790242, 0.43388373911756, 0]),
            10: np.array([0.22252093395631, 0.97492791218182, 0]),
            11: np.array([-0.62348980185873, 0.78183148246803, 0]),
            12: np.array([-1, 1.2246467991474e-16, 0]),
            13: np.array([-0.62348980185873, -0.78183148246803, 0]),
            14: np.array([0.22252093395631, -0.97492791218182, 0]),
            15: np.array([0.90096886790242, -0.43388373911756, 0]),
            16: np.array([2.70710996354, 0.70710359881873, 0]),
            17: np.array([1.9918462491018, 0.99996675762062, 0]),
            18: np.array([1.2928926767367, 0.70710623910939, 0]),
            19: np.array([1.0000332017522, 0.0081487669001626, 0]),
            20: np.array([1.2928879761966, -0.7071015385308, 0]),
            21: np.array([2.0076807905656, -0.99997050229309, 0]),
            22: np.array([2.7070847766723, -0.70712878501603, 0]),
            23: np.array([2.9237489226553, 0.38299860038019, 0]),
            24: np.array([2.38299510833, 0.92375037049805, 0]),
            25: np.array([1.6338745929072, 0.93056551960682, 0]),
            26: np.array([1.0694364290352, 0.36613035983548, 0]),
            27: np.array([1.0762502016859, -0.38299648838425, 0]),
            28: np.array([1.6170182046085, -0.92375589004818, 0]),
            29: np.array([2.3670690911736, -0.93019367999627, 0]),
            30: np.array([2.9302142257684, -0.36701702164618, 0]),
            31: np.array([1.5202888403297e-17, -7.7860210853066e-18, 0]),
            32: np.array([-0.45048443395121, 0.21694186955878, 0]),
            33: np.array([-0.11126046697816, 0.48746395609091, 0]),
            34: np.array([-0.45048443395121, -0.21694186955878, 0]),
            35: np.array([0.31174490092937, 0.39091574123401, 0]),
            36: np.array([-0.11126046697816, -0.48746395609091, 0]),
            37: np.array([0.5, -3.8930105426533e-18, 0]),
            38: np.array([0.31174490092937, -0.39091574123401, 0]),
            39: np.array([1.9939169035527, 0.00079973439438155, 0]),
            40: np.array([2.3354083217744, -0.33306514902439, 0]),
            41: np.array([1.652296679386, 0.34201120858086, 0]),
            42: np.array([1.6405716677311, -0.35579835707924, 0]),
            43: np.array([1.830900682302, 0.16345807128212, 0]),
            44: np.array([1.3331173056494, 0.16859944295424, 0]),
            45: np.array([2.3532471196873, 0.35675071610953, 0]),
            46: np.array([2.1570160552678, -0.1586081427035, 0]),
            47: np.array([2.660694970063, -0.16384124850615, 0]),
            48: np.array([2.1649675154598, -0.65963968373472, 0]),
            49: np.array([1.8282722837808, 0.66421423025096, 0]),
        }
        cells = {
            "triangle6": {
                1: np.array([5, 31, 4, 32, 33, 11]),
                2: np.array([6, 31, 5, 34, 32, 12]),
                3: np.array([4, 31, 3, 33, 35, 10]),
                4: np.array([7, 31, 6, 36, 34, 13]),
                5: np.array([3, 31, 1, 35, 37, 9]),
                6: np.array([8, 31, 7, 38, 36, 14]),
                7: np.array([1, 31, 8, 37, 38, 15]),
            },
            "quad8": {
                8: np.array([19, 20, 39, 41, 27, 42, 43, 44]),
                9: np.array([2, 16, 39, 40, 23, 45, 46, 47]),
                10: np.array([40, 39, 20, 21, 46, 42, 28, 48]),
                11: np.array([41, 39, 16, 17, 43, 45, 24, 49]),
                12: np.array([17, 18, 19, 41, 25, 26, 44, 49]),
                13: np.array([21, 22, 2, 40, 29, 30, 47, 48]),
            },
        }
        cells_h5_ref = np.concatenate(
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

        # Check xml using sha256
        xml_hash = hashlib.sha256(open(filename + ".xdmf", "rb").read()).hexdigest()
        self.assertEqual(xml_hash, xml_sha256)

        # Check h5
        with h5py.File(filename + ".h5", "r") as f:
            vertices_h5 = np.array(f.get(filename + "/VERTICES"))
            cells_h5 = np.array(f.get(filename + "/CELLS"))
        # Vertices
        for i, coord in enumerate(vertices.values()):
            for j in range(len(coord)):
                self.assertEqual(vertices_h5[i][j], coord[j])
        # Cells
        for i in range(len(cells_h5_ref)):
            self.assertEqual(cells_h5[i], cells_h5_ref[i])

        os.remove(filename + ".xdmf")
        os.remove(filename + ".h5")
