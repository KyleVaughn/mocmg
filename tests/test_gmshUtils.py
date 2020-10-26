import gmsh
import mocmg
import pytest
import subprocess
from unittest import TestCase

class test_gmshUtils(TestCase):

    def test_getEntitiesForPhysicalGroupName(self):
        mocmg.initialize(gmshOption='silent')
        gmsh.model.occ.addDisk(0, 0, 0, 1, 1)
        gmsh.model.occ.addDisk(0, 0, 0, 1, 1)
        gmsh.model.occ.synchronize()
        gmsh.model.addPhysicalGroup(2,[1, 2],1)
        gmsh.model.setPhysicalName(2,1,'Material Uranium')
        ents = mocmg.getEntitiesForPhysicalGroupName('Material Uranium')
        self.assertSequenceEqual(set(ents), set([1, 2]))
        with pytest.raises(ValueError) as e_info:
            ents = mocmg.getEntitiesForPhysicalGroupName('NOT_A_REAL_GROUP')
        e_info.match("'NOT_A_REAL_GROUP' is not in list")
        mocmg.finalize()

    def test_findLinearDiskRadius(self):
        mocmg.initialize(gmshOption='silent')
        radius = 1.0
        lc = 0.5
        R = mocmg.findLinearDiskRadius(radius, lc)
        raise ValueError
        mocmg.finalize()

