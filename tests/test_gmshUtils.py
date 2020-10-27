import gmsh
import mocmg
import pytest
from unittest import TestCase

pi = 3.141592653589793


class test_gmshUtils(TestCase):
    def test_getEntitiesForPhysicalGroupName(self):
        mocmg.initialize(gmshOption="silent")
        gmsh.model.occ.addDisk(0, 0, 0, 1, 1)
        gmsh.model.occ.addDisk(0, 0, 0, 1, 1)
        gmsh.model.occ.synchronize()
        gmsh.model.addPhysicalGroup(2, [1, 2], 1)
        gmsh.model.setPhysicalName(2, 1, "Material Uranium")
        ents = mocmg.getEntitiesForPhysicalGroupName("Material Uranium")
        self.assertSequenceEqual(set(ents), set([1, 2]))
        with pytest.raises(ValueError) as e_info:
            ents = mocmg.getEntitiesForPhysicalGroupName("NOT_A_REAL_GROUP")
        e_info.match("'NOT_A_REAL_GROUP' is not in list")
        mocmg.finalize()

    def test_findLinearDiskRadius(self):
        radius = 1.0
        lc = 0.5
        gmsh.initialize()
        R = mocmg.findLinearDiskRadius(radius, lc)
        s = gmsh.model.occ.addDisk(0, 0, 0, R, R)
        gmsh.model.occ.synchronize()
        p = gmsh.model.addPhysicalGroup(2, [s])
        gmsh.model.mesh.setSize(gmsh.model.getEntities(0), lc)
        gmsh.model.mesh.generate(2)
        gmsh.plugin.setNumber("MeshVolume", "Dimension", 2)
        gmsh.plugin.setNumber("MeshVolume", "PhysicalGroup", p)
        gmsh.plugin.run("MeshVolume")
        _, _, data = gmsh.view.getListData(0)
        total_area = data[0][-1]
        self.assertAlmostEqual(total_area, pi, places=10)
        gmsh.finalize()
