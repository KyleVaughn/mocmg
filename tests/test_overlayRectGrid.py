import gmsh
import mocmg
from .testingUtils import captured_output
from unittest import TestCase

class test_overlayRectGrid(TestCase):

    def test_gmshDisk(self):
        mocmg.initialize()
        gmsh.model.occ.addDisk(0, 0, 0, 1, 1)
        gmsh.model.occ.synchronize()
        gmsh.model.addPhysicalGroup(2,[1],1)
        gmsh.model.setPhysicalName(2,1,'Material Uranium')
        mocmg.overlayRectGrid(1,1)
        gmsh.fltk.run()
        mocmg.finalize()
