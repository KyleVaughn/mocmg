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
            "INFO      : mocmg.mesh.abaqus_IO - "
            + "Reading mesh data from tests/mesh/abaqus_files/triangle_only.inp"
        ]
        err_ref = []
        with captured_output() as (out, err):
            mocmg.initialize()
            mesh = mocmg.mesh.read_abaqus_file("tests/mesh/abaqus_files/triangle_only.inp")
            vertices = mesh.vertices
            cells = mesh.cells
            cell_sets = mesh.cell_sets

        # vertices
        for i in range(1, 9):
            for j in range(3):
                self.assertEqual(vertices[i][j], vertices_ref[i][j])
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
            "INFO      : mocmg.mesh.abaqus_IO - "
            + "Reading mesh data from tests/mesh/abaqus_files/mixed_topology.inp"
        ]
        err_ref = []

        with captured_output() as (out, err):
            mocmg.initialize()
            mesh = mocmg.mesh.read_abaqus_file("tests/mesh/abaqus_files/mixed_topology.inp")
            vertices = mesh.vertices
            cells = mesh.cells
            cell_sets = mesh.cell_sets

        # vertices
        for i in range(1, 50):
            for j in range(3):
                self.assertEqual(vertices[i][j], vertices_ref[i][j])
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
            "INFO      : mocmg.mesh.abaqus_IO - "
            + "Reading mesh data from tests/mesh/abaqus_files/disks_mixed.inp"
        ]
        err_ref = []
        with captured_output() as (out, err):
            mocmg.initialize()
            mesh = mocmg.mesh.read_abaqus_file("tests/mesh/abaqus_files/disks_mixed.inp")
            vertices = mesh.vertices
            cells = mesh.cells
            cell_sets = mesh.cell_sets

        # vertices
        for i in range(1, 50):
            for j in range(3):
                self.assertEqual(vertices[i][j], vertices_ref[i][j])
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

    def test_element_type_error(self):
        """Test reading a file with an unsupported element type."""
        out_ref = [
            "INFO      : mocmg.mesh.abaqus_IO - "
            + "Reading mesh data from tests/mesh/abaqus_files/element_error.inp"
        ]
        err_ref = [
            "ERROR     : mocmg.mesh.abaqus_IO - Unrecognized mesh element type: 'MADEUPTYPE'."
        ]

        with self.assertRaises(SystemExit):
            with captured_output() as (out, err):
                mocmg.initialize()
                mocmg.mesh.read_abaqus_file("tests/mesh/abaqus_files/element_error.inp")
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out, err = [line.split(None, 1)[1] for line in out], [
            line.split(None, 1)[1] for line in [err[0]]
        ]
        self.assertEqual(out, out_ref)
        self.assertEqual(err, err_ref)

    def test_two_triangular_disks(self):
        """Test reading a file with 1D elements and multiple same element surfaces."""
        vertices_ref = {
            1: np.array([1, 0, 0]),
            2: np.array([3, 0, 0]),
            3: np.array([0.9135454576426, 0.4067366430758, 0]),
            4: np.array([0.66913060635886, 0.74314482547739, 0]),
            5: np.array([0.30901699437495, 0.95105651629515, 0]),
            6: np.array([-0.10452846326766, 0.99452189536827, 0]),
            7: np.array([-0.5, 0.86602540378444, 0]),
            8: np.array([-0.80901699437495, 0.58778525229247, 0]),
            9: np.array([-0.97814760073381, 0.20791169081776, 0]),
            10: np.array([-0.97814760073381, -0.20791169081776, 0]),
            11: np.array([-0.80901699437495, -0.58778525229247, 0]),
            12: np.array([-0.5, -0.86602540378444, 0]),
            13: np.array([-0.10452846326765, -0.99452189536827, 0]),
            14: np.array([0.30901699437495, -0.95105651629515, 0]),
            15: np.array([0.66913060635886, -0.74314482547739, 0]),
            16: np.array([0.9135454576426, -0.4067366430758, 0]),
            17: np.array([2.9135454576426, 0.4067366430758, 0]),
            18: np.array([2.6691306063589, 0.74314482547739, 0]),
            19: np.array([2.3090169943749, 0.95105651629515, 0]),
            20: np.array([1.8954715367323, 0.99452189536827, 0]),
            21: np.array([1.5, 0.86602540378444, 0]),
            22: np.array([1.1909830056251, 0.58778525229247, 0]),
            23: np.array([1.0218523992662, 0.20791169081776, 0]),
            24: np.array([1.0218523992662, -0.20791169081776, 0]),
            25: np.array([1.1909830056251, -0.58778525229247, 0]),
            26: np.array([1.5, -0.86602540378444, 0]),
            27: np.array([1.8954715367323, -0.99452189536827, 0]),
            28: np.array([2.3090169943749, -0.95105651629515, 0]),
            29: np.array([2.6691306063589, -0.74314482547739, 0]),
            30: np.array([2.9135454576426, -0.4067366430758, 0]),
            31: np.array([-0.6180339887499, -1.4221562401074e-15, 0]),
            32: np.array([0.70320311944336, -0.15053733078756, 0]),
            33: np.array([0.065686021199849, 0.63291493762804, 0]),
            34: np.array([-0.20429227931724, -0.6023252887068, 0]),
            35: np.array([0.30901699437495, -0.53523313465964, 0]),
            36: np.array([-0.4386781959022, 0.48806006236265, 0]),
            37: np.array([0.5, 0.36327126400268, 0]),
            38: np.array([-0.50036169095541, -0.54131557472686, 0]),
            39: np.array([-0.30901699437495, -0.22451398828979, 0]),
            40: np.array([0.02418275723581, -0.33146743273124, 0]),
            41: np.array([-0.051312367929457, 0.037045290181453, 0]),
            42: np.array([0.37503515830872, -0.073679515563182, 0]),
            43: np.array([-0.3483318058987, 0.15508731199142, 0]),
            44: np.array([0.70765748385681, 0.12235860101394, 0]),
            45: np.array([0.37361913746615, 0.64712732877144, 0]),
            46: np.array([0.17975297427597, 0.31134128425759, 0]),
            47: np.array([0.59699832323769, -0.39825181792442, 0]),
            48: np.array([0.078107668573447, -0.74314482547739, 0]),
            49: np.array([-0.6826361318411, 0.30392918752372, 0]),
            50: np.array([-0.6826361318411, -0.30392918752372, 0]),
            51: np.array([-0.2309093258015, 0.71066583059952, 0]),
            52: np.array([-0.13729878334267, 0.38918578617011, 0]),
            53: np.array([1.3819660112501, -1.4221562401074e-15, 0]),
            54: np.array([2.7032031194434, -0.15053733078756, 0]),
            55: np.array([2.0656860211998, 0.63291493762805, 0]),
            56: np.array([1.7957077206828, -0.6023252887068, 0]),
            57: np.array([2.5, 0.36327126400268, 0]),
            58: np.array([1.5613218040978, 0.48806006236265, 0]),
            59: np.array([2.3090169943749, -0.53523313465964, 0]),
            60: np.array([1.4996383090446, -0.54131557472686, 0]),
            61: np.array([1.6909830056251, -0.22451398828979, 0]),
            62: np.array([2.0241827572358, -0.33146743273124, 0]),
            63: np.array([1.9486876320705, 0.037045290181453, 0]),
            64: np.array([2.3750351583087, -0.073679515563182, 0]),
            65: np.array([1.6516681941013, 0.15508731199142, 0]),
            66: np.array([2.7076574838568, 0.12235860101394, 0]),
            67: np.array([2.3736191374662, 0.64712732877144, 0]),
            68: np.array([2.179752974276, 0.31134128425759, 0]),
            69: np.array([2.5969983232377, -0.39825181792442, 0]),
            70: np.array([2.0781076685734, -0.74314482547739, 0]),
            71: np.array([1.7690906741985, 0.71066583059952, 0]),
            72: np.array([1.3173638681589, -0.30392918752372, 0]),
            73: np.array([1.3173638681589, 0.30392918752372, 0]),
            74: np.array([1.8627012166573, 0.38918578617011, 0]),
        }
        cells_ref = {
            "triangle": {
                33: np.array([42, 44, 37]),
                34: np.array([32, 44, 42]),
                35: np.array([35, 47, 42]),
                36: np.array([42, 47, 32]),
                37: np.array([37, 46, 42]),
                38: np.array([1, 32, 16]),
                39: np.array([4, 37, 3]),
                40: np.array([6, 33, 5]),
                41: np.array([8, 36, 7]),
                42: np.array([15, 35, 14]),
                43: np.array([10, 31, 9]),
                44: np.array([13, 34, 12]),
                45: np.array([35, 42, 40]),
                46: np.array([40, 41, 39]),
                47: np.array([34, 48, 40]),
                48: np.array([40, 48, 35]),
                49: np.array([41, 43, 39]),
                50: np.array([40, 42, 41]),
                51: np.array([34, 40, 39]),
                52: np.array([12, 38, 11]),
                53: np.array([34, 39, 38]),
                54: np.array([31, 50, 39]),
                55: np.array([39, 50, 38]),
                56: np.array([3, 44, 1]),
                57: np.array([5, 45, 4]),
                58: np.array([6, 51, 33]),
                59: np.array([34, 38, 12]),
                60: np.array([4, 45, 37]),
                61: np.array([15, 47, 35]),
                62: np.array([37, 44, 3]),
                63: np.array([8, 49, 36]),
                64: np.array([32, 47, 16]),
                65: np.array([10, 50, 31]),
                66: np.array([14, 48, 13]),
                67: np.array([16, 47, 15]),
                68: np.array([33, 45, 5]),
                69: np.array([7, 51, 6]),
                70: np.array([11, 50, 10]),
                71: np.array([13, 48, 34]),
                72: np.array([36, 51, 7]),
                73: np.array([9, 49, 8]),
                74: np.array([31, 49, 9]),
                75: np.array([1, 44, 32]),
                76: np.array([35, 48, 14]),
                77: np.array([39, 43, 31]),
                78: np.array([42, 46, 41]),
                79: np.array([45, 46, 37]),
                80: np.array([33, 46, 45]),
                81: np.array([43, 49, 31]),
                82: np.array([36, 49, 43]),
                83: np.array([36, 52, 51]),
                84: np.array([51, 52, 33]),
                85: np.array([46, 52, 41]),
                86: np.array([33, 52, 46]),
                87: np.array([38, 50, 11]),
                88: np.array([43, 52, 36]),
                89: np.array([41, 52, 43]),
                90: np.array([64, 66, 57]),
                91: np.array([54, 66, 64]),
                92: np.array([59, 69, 64]),
                93: np.array([64, 69, 54]),
                94: np.array([57, 68, 64]),
                95: np.array([29, 59, 28]),
                96: np.array([22, 58, 21]),
                97: np.array([18, 57, 17]),
                98: np.array([2, 54, 30]),
                99: np.array([24, 53, 23]),
                100: np.array([27, 56, 26]),
                101: np.array([20, 55, 19]),
                102: np.array([59, 64, 62]),
                103: np.array([62, 63, 61]),
                104: np.array([56, 70, 62]),
                105: np.array([62, 70, 59]),
                106: np.array([63, 65, 61]),
                107: np.array([62, 64, 63]),
                108: np.array([56, 62, 61]),
                109: np.array([56, 61, 60]),
                110: np.array([26, 60, 25]),
                111: np.array([61, 72, 60]),
                112: np.array([54, 69, 30]),
                113: np.array([19, 67, 18]),
                114: np.array([53, 72, 61]),
                115: np.array([17, 66, 2]),
                116: np.array([2, 66, 54]),
                117: np.array([56, 60, 26]),
                118: np.array([29, 69, 59]),
                119: np.array([27, 70, 56]),
                120: np.array([30, 69, 29]),
                121: np.array([53, 73, 23]),
                122: np.array([20, 71, 55]),
                123: np.array([58, 71, 21]),
                124: np.array([25, 72, 24]),
                125: np.array([57, 66, 17]),
                126: np.array([18, 67, 57]),
                127: np.array([22, 73, 58]),
                128: np.array([21, 71, 20]),
                129: np.array([23, 73, 22]),
                130: np.array([24, 72, 53]),
                131: np.array([28, 70, 27]),
                132: np.array([59, 70, 28]),
                133: np.array([55, 67, 19]),
                134: np.array([61, 65, 53]),
                135: np.array([64, 68, 63]),
                136: np.array([55, 68, 67]),
                137: np.array([67, 68, 57]),
                138: np.array([58, 73, 65]),
                139: np.array([65, 73, 53]),
                140: np.array([58, 74, 71]),
                141: np.array([71, 74, 55]),
                142: np.array([55, 74, 68]),
                143: np.array([68, 74, 63]),
                144: np.array([60, 72, 25]),
                145: np.array([63, 74, 65]),
                146: np.array([65, 74, 58]),
            }
        }
        out_ref = [
            "INFO      : mocmg.mesh.abaqus_IO - Reading mesh data from "
            + "tests/mesh/abaqus_files/two_trianglular_disks.inp"
        ]
        err_ref = []

        with captured_output() as (out, err):
            mocmg.initialize()
            mesh = mocmg.mesh.read_abaqus_file("tests/mesh/abaqus_files/two_trianglular_disks.inp")
            vertices = mesh.vertices
            cells = mesh.cells
            cell_sets = mesh.cell_sets
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out, err = [line.split(None, 1)[1] for line in out], [
            line.split(None, 1)[1] for line in err
        ]
        self.assertEqual(out, out_ref)
        self.assertEqual(err, err_ref)
        # vertices
        for i in range(1, 75):
            for j in range(3):
                self.assertEqual(vertices[i][j], vertices_ref[i][j])
        # cells
        self.assertEqual(len(cells), 1)
        self.assertEqual(list(cells.keys()), ["triangle"])
        for i in range(33, 147):
            for j in range(3):
                self.assertEqual(cells["triangle"][i][j], cells_ref["triangle"][i][j])
        # cell_sets
        self.assertEqual(cell_sets, {})
