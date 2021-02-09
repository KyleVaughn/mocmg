"""Test reading and writing of Abaqus files."""

import os
import sys
from unittest import TestCase

import numpy as np

import mocmg
import mocmg.mesh

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from testing_utils import captured_output


class TestAbaqusIO(TestCase):
    """Test the abaqus IO functions."""

    def test_triangle_only(self):
        """Test reading abaqus file with triangle cells only and no cell sets."""
        vertices_ref = {
            1: np.array([1.0, 0.0, 0.0]),
            2: np.array([0.62348980185873, 0.78183148246803, 0.0]),
            3: np.array([-0.22252093395631, 0.97492791218182, 0.0]),
            4: np.array([-0.90096886790242, 0.43388373911756, 0.0]),
            5: np.array([-0.90096886790242, -0.43388373911756, 0.0]),
            6: np.array([-0.22252093395631, -0.97492791218182, 0.0]),
            7: np.array([0.62348980185873, -0.78183148246803, 0.0]),
            8: np.array([1.5202888403297e-17, -7.7860210853066e-18, 0.0]),
        }
        cells_ref = {
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
            "INFO      : mocmg.mesh.abaqus_IO - Reading mesh data from tests/abaqus_files/triangle_only.inp"
        ]
        err_ref = []
        with captured_output() as (out, err):
            mocmg.initialize()
            mesh = mocmg.mesh.read_abaqus_file("tests/abaqus_files/triangle_only.inp")
            vertices = mesh.vertices
            cells = mesh.cells
            cell_sets = mesh.cell_sets

        # vertices
        for i in range(1, 9):
            for j in range(3):
                self.assertAlmostEqual(vertices[i][j], vertices_ref[i][j], places=10)
        # cells
        self.assertEqual(len(cells), 1)
        self.assertEqual(list(cells.keys()), ["triangle"])
        for i in range(1, 8):
            for j in range(3):
                self.assertEqual(cells["triangle"][i][j], cells_ref["triangle"][i][j])
        # cell_sets
        self.assertEqual(cell_sets, {})
        # message
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        # strip times
        out, err = [line.split(None, 1)[1] for line in out], [
            line.split(None, 1)[1] for line in err
        ]
        self.assertEqual(out, out_ref)
        self.assertEqual(err, err_ref)

    def test_mixed_topology_2nd_order(self):
        """Test reading abaqus file with mixed topology and 2nd order cells and no cell sets."""
        vertices_ref = {
            1: np.array([1, 0, 0]),
            2: np.array([3, 0, 0]),
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
        cells_ref = {
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
        out_ref = [
            "INFO      : mocmg.mesh.abaqus_IO - Reading mesh data from tests/abaqus_files/mixed_topology.inp"
        ]
        err_ref = []

        with captured_output() as (out, err):
            mocmg.initialize()
            mesh = mocmg.mesh.read_abaqus_file("tests/abaqus_files/mixed_topology.inp")
            vertices = mesh.vertices
            cells = mesh.cells
            cell_sets = mesh.cell_sets

        # vertices
        for i in range(1, 50):
            for j in range(3):
                self.assertAlmostEqual(vertices[i][j], vertices_ref[i][j], places=10)
        # cells
        self.assertEqual(len(cells), 2)
        self.assertEqual(list(cells.keys()), ["triangle6", "quad8"])
        for i in range(1, 8):
            for j in range(6):
                self.assertEqual(cells["triangle6"][i][j], cells_ref["triangle6"][i][j])

        for i in range(8, 14):
            for j in range(8):
                self.assertEqual(cells["quad8"][i][j], cells_ref["quad8"][i][j])
        # cell_sets
        self.assertEqual(cell_sets, {})
        # message
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        # strip times
        out, err = [line.split(None, 1)[1] for line in out], [
            line.split(None, 1)[1] for line in err
        ]
        self.assertEqual(out, out_ref)
        self.assertEqual(err, err_ref)

    def test_cell_sets(self):
        """Test reading abaqus file with cell sets."""
        vertices_ref = {
            1: np.array([1, 0, 0]),
            2: np.array([3, 0, 0]),
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
        cells_ref = {
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
        cell_sets_ref = {
            "MATERIAL_URANIUM": np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]),
            "DISK2": np.array([8, 9, 10, 11, 12, 13]),
            "DISK1": np.array([1, 2, 3, 4, 5, 6, 7]),
        }
        out_ref = [
            "INFO      : mocmg.mesh.abaqus_IO - Reading mesh data from tests/abaqus_files/disks_mixed.inp"
        ]
        err_ref = []
        with captured_output() as (out, err):
            mocmg.initialize()
            mesh = mocmg.mesh.read_abaqus_file("tests/abaqus_files/disks_mixed.inp")
            vertices = mesh.vertices
            cells = mesh.cells
            cell_sets = mesh.cell_sets

        # vertices
        for i in range(1, 50):
            for j in range(3):
                self.assertAlmostEqual(vertices[i][j], vertices_ref[i][j], places=10)
        # cells
        self.assertEqual(len(cells), 2)
        self.assertEqual(list(cells.keys()), ["triangle6", "quad8"])
        for i in range(1, 8):
            for j in range(6):
                self.assertEqual(cells["triangle6"][i][j], cells_ref["triangle6"][i][j])

        for i in range(8, 14):
            for j in range(8):
                self.assertEqual(cells["quad8"][i][j], cells_ref["quad8"][i][j])
        # cell_sets
        self.assertEqual(len(cell_sets), 3)
        keys = [k for k in cell_sets.keys()]
        for key in keys:
            for j in range(len(cell_sets_ref[key])):
                self.assertEqual(cell_sets[key][j], cell_sets_ref[key][j])
        # message
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        # strip times
        out, err = [line.split(None, 1)[1] for line in out], [
            line.split(None, 1)[1] for line in err
        ]
        self.assertEqual(out, out_ref)
        self.assertEqual(err, err_ref)
