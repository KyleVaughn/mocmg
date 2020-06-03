from unittest import TestCase
import gmsh
import mocmg
import logging
logging.disable(logging.CRITICAL)

class test_overlayRectGrid(TestCase):
    def test_diskLattice(self):
        gmsh.initialize()
        mocmg.addDiskLattice(3,1,0.2)
        mocmg.overlayRectGrid(3,3)
        n=4
        self.assertAlmostEqual(4.0,4.2,places=3,msg='More descriptive message here!')
        gmsh.finalize()
