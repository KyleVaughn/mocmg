from unittest import TestCase

import gmsh

import mocmg


class test_xdmfIO(TestCase):
    def test_default(self):
        mocmg.initialize()
        gmshVerbosity = 0
        gmsh.initialize()
        gmsh.option.setNumber("General.Terminal", 1)
        gmsh.option.setNumber("General.Verbosity", gmshVerbosity)
        gmsh.model.occ.addDisk(0, 0, 0, 1, 1)
        gmsh.model.occ.synchronize()
        gmsh.model.addPhysicalGroup(2, [1], 1)
        gmsh.model.setPhysicalName(2, 1, "Material Uranium")
        #        mocmg.writeXDMF("test.xdmf", mesh)
        mocmg.finalize()
