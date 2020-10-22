import gmsh
import mocmg
import pytest
from contextlib import contextmanager
from .testingUtils import captured_output
from unittest import TestCase

class test_generateRectGrid(TestCase):

    def test_rectGridDefault(self):
        mocmg.initialize(mocmgOption='silent', gmshOption='silent')
        bb = [0, 0, 0, 9, 4, 0]
        PGTagsL1, PGTagsL2, PGNamesL1, PGNamesL2 = mocmg.generateRectGrid(bb, 3, 2)
        IDL1 = list(range(1,7)) 
        IDL2 = list(range(7,13)) 
        namesL1 = [
                'GRID_L1_001_001',
                'GRID_L1_001_002',
                'GRID_L1_002_001',
                'GRID_L1_002_002',
                'GRID_L1_003_001',
                'GRID_L1_003_002']
        namesL2 = [
                'GRID_L2_001_001',
                'GRID_L2_001_002',
                'GRID_L2_002_001',
                'GRID_L2_002_002',
                'GRID_L2_003_001',
                'GRID_L2_003_002']
        self.assertEqual(IDL1, PGTagsL1)
        self.assertEqual(namesL1, PGNamesL1)
        self.assertEqual(IDL2, PGTagsL2)
        self.assertEqual(namesL2, PGNamesL2)
        # Locations/shape of entities
        for ptag in IDL1:
            # Elementary tag
            etag = gmsh.model.getEntitiesForPhysicalGroup(2, ptag)
            self.assertEqual(etag, ptag)
            # Area
            print(etag)
            mass = gmsh.model.occ.getMass(2, etag[0])
            self.assertAlmostEqual(6.0, mass, places=5, msg='3 width, 2 height, 6 area')
        # Centroid
        x,y,z = gmsh.model.occ.getCenterOfMass(2, 1)
        self.assertAlmostEqual(1.5, x, places=5)
        self.assertAlmostEqual(1.0, y, places=5)
        self.assertAlmostEqual(0.0, z, places=5)
        x,y,z = gmsh.model.occ.getCenterOfMass(2, 4)
        self.assertAlmostEqual(4.5, x, places=5)
        self.assertAlmostEqual(3.0, y, places=5)
        self.assertAlmostEqual(0.0, z, places=5)
        mocmg.finalize()

    def test_rectGridOptionalArgs(self):
        # Capture output since bb will throw warning on purpose
        with captured_output() as (out,err):
            mocmg.initialize(mocmgOption='warning', gmshOption='silent')
            nx = 3
            ny = 2
            nnx = 3
            nny = 2
            bb = [0, 0, 0, 9, 4, 1]
            PGTagsL1, PGTagsL2, PGNamesL1, PGNamesL2 = mocmg.generateRectGrid(bb, nx, ny, nnx, nny)
            IDL1 = list(range(1,7))
            IDL2 = list(range(7,43))
            namesL1 = [
                    'GRID_L1_001_001',
                    'GRID_L1_001_002',
                    'GRID_L1_002_001',
                    'GRID_L1_002_002',
                    'GRID_L1_003_001',
                    'GRID_L1_003_002']
            namesL2 = [
                    'GRID_L2_001_001',
                    'GRID_L2_001_002',
                    'GRID_L2_002_001',
                    'GRID_L2_002_002',
                    'GRID_L2_003_001',
                    'GRID_L2_003_002',
                    'GRID_L2_001_003',
                    'GRID_L2_001_004',
                    'GRID_L2_002_003',
                    'GRID_L2_002_004',
                    'GRID_L2_003_003',
                    'GRID_L2_003_004',
                    'GRID_L2_004_001',
                    'GRID_L2_004_002',
                    'GRID_L2_005_001',
                    'GRID_L2_005_002',
                    'GRID_L2_006_001',
                    'GRID_L2_006_002',
                    'GRID_L2_004_003',
                    'GRID_L2_004_004',
                    'GRID_L2_005_003',
                    'GRID_L2_005_004',
                    'GRID_L2_006_003',
                    'GRID_L2_006_004',
                    'GRID_L2_007_001',
                    'GRID_L2_007_002',
                    'GRID_L2_008_001',
                    'GRID_L2_008_002',
                    'GRID_L2_009_001',
                    'GRID_L2_009_002',
                    'GRID_L2_007_003',
                    'GRID_L2_007_004',
                    'GRID_L2_008_003',
                    'GRID_L2_008_004',
                    'GRID_L2_009_003',
                    'GRID_L2_009_004'
                    ]
            self.assertEqual(IDL1, PGTagsL1)
            self.assertEqual(namesL1, PGNamesL1)
            self.assertEqual(IDL2, PGTagsL2)
            self.assertEqual(namesL2, PGNamesL2)
            # Locations/shape of entities
            tagCounter = 1
            for ptag in IDL1:                                                                       
                # Elementary tag
                etags = list(gmsh.model.getEntitiesForPhysicalGroup(2, ptag))
                self.assertEqual(etags, list(range(tagCounter, tagCounter+6)))
                # Area
                for tag in etags:
                    mass = gmsh.model.occ.getMass(2, tag)
                    self.assertAlmostEqual(1.0, mass, places=5)
                tagCounter += 6
            # Centroid
            x,y,z = gmsh.model.occ.getCenterOfMass(2, 1)
            self.assertAlmostEqual(0.5, x, places=5)
            self.assertAlmostEqual(0.5, y, places=5)
            self.assertAlmostEqual(0.0, z, places=5)
            x,y,z = gmsh.model.occ.getCenterOfMass(2, 14)
            self.assertAlmostEqual(3.5, x, places=5)
            self.assertAlmostEqual(1.5, y, places=5)
            self.assertAlmostEqual(0.0, z, places=5)
            for ptag in IDL2:
                # Elementary tag
                etag = list(gmsh.model.getEntitiesForPhysicalGroup(2, ptag))
                self.assertEqual(etag[0]+6, ptag)
                # Area
                mass = gmsh.model.occ.getMass(2, etag[0])
                self.assertAlmostEqual(1.0, mass, places=5)
        out, err = out.getvalue().splitlines(), err.getvalue().splitlines()
        out, err = [l.split(None,1)[1] for l in out], [l.split(None,1)[1] for l in err] # strip times
        self.assertEqual(out, [])
        err_ref = 'WARNING   : mocmg.generateRectGrid - Model thickness is 1.000000 > 1e-6.' +\
                ' Model expected in 2D x-y plane.'
        self.assertEqual(err[0], err_ref)
        mocmg.finalize()

    def test_rectGridTooManyXDiv(self):
        nx = 1E6
        ny = 2
        nnx = 3
        nny = 2
        bb = [0, 0, 0, 9, 4, 1]
        with pytest.raises(Exception) as e_info:
            PGTagsL1, PGTagsL2, PGNamesL1, PGNamesL2 = mocmg.generateRectGrid(bb, nx, ny, nnx, nny)
        e_info.match('Too many x-divisions of bounding box for the output format')

    def test_rectGridTooManyYDiv(self):
        nx = 2
        ny = 1E6
        nnx = 3
        nny = 2
        bb = [0, 0, 0, 9, 4, 1]
        with pytest.raises(ValueError) as e_info:
            PGTagsL1, PGTagsL2, PGNamesL1, PGNamesL2 = mocmg.generateRectGrid(bb, nx, ny, nnx, nny)
        e_info.match('Too many y-divisions of bounding box for the output format')
