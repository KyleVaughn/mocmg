import gmsh
import mocmg
from unittest import TestCase


class test_xdmfIO(TestCase):
    def test_default(self):
        mocmg.initialize(gmshOption="silent")
        gmsh.model.occ.addDisk(0, 0, 0, 1, 1)
        gmsh.model.occ.synchronize()
        gmsh.model.addPhysicalGroup(2, [1], 1)
        gmsh.model.setPhysicalName(2, 1, "Material Uranium")
        #        mocmg.writeXDMF("test.xdmf", mesh)
        mocmg.finalize()
