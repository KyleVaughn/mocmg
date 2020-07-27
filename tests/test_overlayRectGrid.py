import gmsh
import mocmg
from math import pi
from .testingUtils import captured_output
from unittest import TestCase

# NOTE: You pretty much have to run gmsh.fltk.run() to debug these

class test_overlayRectGrid(TestCase):

    def test_gmshDisk(self):
        pgroups_ref = [
                'Material Uranium',
                'Grid_L1_001_001',
                'Grid_L2_001_001',
                'Material Void'
                ]
        elem_ents = [
                [1],
                [1, 2, 3, 4, 5],
                [1, 2, 3, 4, 5],
                [2, 3, 4, 5]
                ]
        areas = [pi,
                (4 - pi)/4.,
                (4 - pi)/4.,
                (4 - pi)/4.,
                (4 - pi)/4.
                ]
        out_ref = ['INFO      : mocmg.overlayRectGrid - Overlaying rectangular grid',
                'INFO      : mocmg.overlayRectGrid - Fragmenting 1 entities with 1 entities',
                'INFO      : mocmg.overlayRectGrid - Synchronizing model',
                'INFO      : mocmg.overlayRectGrid - Model synchronized']
        err_ref = []
        with captured_output() as (out,err):
            mocmg.initialize(gmshOption='silent')
            gmsh.model.occ.addDisk(0, 0, 0, 1, 1)
            gmsh.model.occ.synchronize()
            gmsh.model.addPhysicalGroup(2,[1],1)
            gmsh.model.setPhysicalName(2,1,'Material Uranium')
            mocmg.overlayRectGrid(1,1)
            # Check that entities were properly named 
            pgroups = gmsh.model.getPhysicalGroups(2)
            for i, p in enumerate(pgroups):
                name = gmsh.model.getPhysicalName(*p)
                self.assertEqual(name, pgroups_ref[i])
                ent = gmsh.model.getEntitiesForPhysicalGroup(*p)
                for j, e in enumerate(elem_ents[i]):
                    self.assertEqual(ent[j], e)
            # Check area of entities
            ents = gmsh.model.getEntities(2)
            for i, e in enumerate(ents):
                area = gmsh.model.occ.getMass(*e)
                self.assertAlmostEqual(area, areas[i], places=6)

            mocmg.finalize()
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out, err = [l.split(None,1)[1] for l in out], [l.split(None,1)[1] for l in err] # strip times
        self.assertEqual(out, out_ref)
        self.assertEqual(err, err_ref)

    def test_gmshDiskCustomBB(self):
        # Also tests multilevel grid
        pgroups_ref = [
                'Material Uranium',
                'Grid_L1_001_001',
                'Grid_L2_001_001',
                'Grid_L2_001_002',
                'Grid_L2_002_001',
                'Grid_L2_002_002',
                'Material Void'
                ]
        elem_ents = [
                [1, 2, 3, 4],
                [1, 2, 3, 4, 5, 6, 7, 8],
                [4, 5],
                [3, 6],
                [2, 7],
                [1, 8],
                [5, 6, 7, 8]
                ]
        areas = [pi/4,
                pi/4,
                pi/4,
                pi/4,
                (64 - pi)/4.,
                (64 - pi)/4.,
                (64 - pi)/4.,
                (64 - pi)/4.
                ]
        out_ref = ['INFO      : mocmg.overlayRectGrid - Overlaying rectangular grid',
                'INFO      : mocmg.overlayRectGrid - Fragmenting 1 entities with 4 entities',
                'INFO      : mocmg.overlayRectGrid - Synchronizing model',
                'INFO      : mocmg.overlayRectGrid - Model synchronized']
        err_ref = ['WARNING   : mocmg.overlayRectGrid - Bounding box for' +\
                ' rectangular grid manually specified. Use caution. Box: [-4, -4, 0, 4, 4, 0]']
        with captured_output() as (out,err):
            mocmg.initialize(gmshOption='silent')
            gmsh.model.occ.addDisk(0, 0, 0, 1, 1)
            gmsh.model.occ.synchronize()
            gmsh.model.addPhysicalGroup(2,[1],1)
            gmsh.model.setPhysicalName(2,1,'Material Uranium')
            bb = [-4,-4,0,4,4,0]
            mocmg.overlayRectGrid(1,1,nnx=2,nny=2,bb=bb)
            # Check that entities were properly named 
            pgroups = gmsh.model.getPhysicalGroups(2)
            for i, p in enumerate(pgroups):
                name = gmsh.model.getPhysicalName(*p)
                self.assertEqual(name, pgroups_ref[i])
                ent = gmsh.model.getEntitiesForPhysicalGroup(*p)
                for j, e in enumerate(elem_ents[i]):
                    self.assertEqual(ent[j], e)
            # Check area of entities
            ents = gmsh.model.getEntities(2)
            for i, e in enumerate(ents):
                area = gmsh.model.occ.getMass(*e)
                self.assertAlmostEqual(area, areas[i], places=6)

            mocmg.finalize()
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out, err = [l.split(None,1)[1] for l in out], [l.split(None,1)[1] for l in err] # strip times
        self.assertEqual(out, out_ref)
        self.assertEqual(err, err_ref)
