"""Test reading and writing of XDMF files."""

import os
import sys
from unittest import TestCase

import numpy as np

import mocmg
import mocmg.mesh

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from testing_utils import captured_output


class TestXDMFIO(TestCase):
    """Test the XDMF IO functions."""

    def test_uniform_grid_triangle_only(self):
        """Test reading abaqus file with triangle cells only and no cell sets."""
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
            "INFO      : mocmg.mesh.xdmf_IO - Writing mesh data to XDMF file "
            + "'uniform_grid_triangle_only.xdmf'."
        ]
        err_ref = []
        with captured_output() as (out, err):
            mocmg.initialize()
            mesh = mocmg.mesh.Mesh(vertices, cells)
            mocmg.mesh.write_xdmf_file("uniform_grid_triangle_only.xdmf", mesh)
            vertices = mesh.vertices
            cells = mesh.cells
            cell_sets = mesh.cell_sets

        # message
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        # strip times
        out, err = [line.split(None, 1)[1] for line in out], [
            line.split(None, 1)[1] for line in err
        ]
        self.assertEqual(out, out_ref)
        self.assertEqual(err, err_ref)

        self.assertEqual(cell_sets, {})

        os.remove("uniform_grid_triangle_only.xdmf")
        os.remove("uniform_grid_triangle_only.h5")
        self.assertTrue(False)
