from unittest import TestCase
import gmsh
import mocmg

class test_addDiskLattice(TestCase):
    def test_numDisks(self):
        gmsh.initialize()
        mocmg.addDiskLattice(5)
        s=4
        self.assertTrue(isinstance(s, int))
        gmsh.finalize()
