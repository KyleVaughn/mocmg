"""Test the overlay rectangular grid function."""
import os
import sys
from unittest import TestCase

import gmsh

import mocmg
from mocmg.model.overlay_rectangular_grid import overlay_rectangular_grid

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from testing_utils import captured_output

bb_42 = [0.0, 0.0, 0.0, 4.0, 2.0, 0.0]

groups_2_pins = {
    "MATERIAL_UO2": [1],
    "MATERIAL_MOX": [2],
    "Grid_L1_1_1": [1, 3],
    "Grid_L1_2_1": [2, 4],
    "MATERIAL_WATER": [3, 4],
}

groups_2_pins_new_mat = {
    "MATERIAL_UO2": [1],
    "MATERIAL_MOX": [2],
    "Grid_L1_1_1": [1, 3],
    "Grid_L1_2_1": [2, 4],
    "MATERIAL_NEW": [3, 4],
}

centroids_2_pins = {
    1: (1.0, 1.0, 0.0),
    2: (3.0, 1.0, 0.0),
    3: (1.0, 1.0, 0.0),
    4: (3.0, 1.0, 0.0),
}

# Expected output for overlaying rectangular grid
reference_out = [
    "INFO      : mocmg.model.overlay_rectangular_grid - Overlaying rectangular grid",
    "INFO      : mocmg.model.rectangular_grid - Generating rectangular grid",
    "INFO      : mocmg.model.rectangular_grid - Synchronizing model",
    "INFO      : mocmg.model.group_preserving_fragment - Fragmenting 8 entities",
    "INFO      : mocmg.model.group_preserving_fragment - Synchronizing model",
]


class TestOverlayRectangularGrid(TestCase):
    """Test the model.overlay_rectangular_grid function."""

    def test_2_pins(self):
        """Test overlaying grid on 2 pins."""
        ref_groups = groups_2_pins
        ref_centroids = centroids_2_pins

        with captured_output() as (out, err):
            mocmg.initialize()
            gmsh.initialize()

            gmsh.model.occ.addDisk(1.0, 1.0, 0.0, 0.5, 0.5)
            gmsh.model.occ.addDisk(3.0, 1.0, 0.0, 0.5, 0.5)
            gmsh.model.occ.synchronize()

            p = gmsh.model.addPhysicalGroup(2, [1])
            gmsh.model.setPhysicalName(2, p, "MATERIAL_UO2")
            p = gmsh.model.addPhysicalGroup(2, [2])
            gmsh.model.setPhysicalName(2, p, "MATERIAL_MOX")

            overlay_rectangular_grid(bb_42, nx=[2], ny=[1])

        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out = [line.split(None, 1)[1] for line in out]
        self.assertEqual(out, reference_out)
        self.assertEqual(err, [])

        group_nums = gmsh.model.getPhysicalGroups()
        names = [gmsh.model.getPhysicalName(*grp) for grp in group_nums]
        ref_names = list(ref_groups.keys())
        # Check correct names/entities
        for i, name in enumerate(ref_names):
            self.assertEqual(name, names[i])
            index = names.index(name)
            group_ents = list(gmsh.model.getEntitiesForPhysicalGroup(*group_nums[index]))
            ref_group_ents = ref_groups[name]
            self.assertEqual(group_ents, ref_group_ents)
        # Check correct area/centroid
        for ent in gmsh.model.getEntities(2):
            tag = ent[1]
            mass = gmsh.model.occ.getMass(2, tag)
            if tag == 1 or tag == 2:
                self.assertAlmostEqual(0.785398, mass, places=5, msg="pi*0.5**2")
                x, y, z = gmsh.model.occ.getCenterOfMass(2, tag)
                centroid = (x, y, z)
                for i in range(3):
                    self.assertAlmostEqual(centroid[i], ref_centroids[tag][i])
        gmsh.clear()
        gmsh.finalize()

    def test_2_pins_new_material(self):
        """Test overlaying grid on 2 pins with a new grid material."""
        ref_groups = groups_2_pins_new_mat
        ref_centroids = centroids_2_pins

        with captured_output() as (out, err):
            mocmg.initialize()
            gmsh.initialize()

            gmsh.model.occ.addDisk(1.0, 1.0, 0.0, 0.5, 0.5)
            gmsh.model.occ.addDisk(3.0, 1.0, 0.0, 0.5, 0.5)
            gmsh.model.occ.synchronize()

            p = gmsh.model.addPhysicalGroup(2, [1])
            gmsh.model.setPhysicalName(2, p, "MATERIAL_UO2")
            p = gmsh.model.addPhysicalGroup(2, [2])
            gmsh.model.setPhysicalName(2, p, "MATERIAL_MOX")

            overlay_rectangular_grid(bb_42, nx=[2], ny=[1], material="MATERIAL_NEW")

        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out = [line.split(None, 1)[1] for line in out]
        self.assertEqual(out, reference_out)
        self.assertEqual(err, [])

        group_nums = gmsh.model.getPhysicalGroups()
        names = [gmsh.model.getPhysicalName(*grp) for grp in group_nums]
        ref_names = list(ref_groups.keys())
        # Check correct names/entities
        for i, name in enumerate(ref_names):
            self.assertEqual(name, names[i])
            index = names.index(name)
            group_ents = list(gmsh.model.getEntitiesForPhysicalGroup(*group_nums[index]))
            ref_group_ents = ref_groups[name]
            self.assertEqual(group_ents, ref_group_ents)
        # Check correct area/centroid
        for ent in gmsh.model.getEntities(2):
            tag = ent[1]
            mass = gmsh.model.occ.getMass(2, tag)
            if tag == 1 or tag == 2:
                self.assertAlmostEqual(0.785398, mass, places=5, msg="pi*0.5**2")
                x, y, z = gmsh.model.occ.getCenterOfMass(2, tag)
                centroid = (x, y, z)
                for i in range(3):
                    self.assertAlmostEqual(centroid[i], ref_centroids[tag][i])
        gmsh.clear()
        gmsh.finalize()
