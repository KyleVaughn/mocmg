from unittest import TestCase
import gmsh
import mocmg

class test_overlayRectGrid(TestCase):
    def test_diskLattice(self):
        gmsh.initialize()
        mocmg.addDiskLattice(3)
        mocmg.overlayRectGrid(3,3)
        gmsh.finalize()
