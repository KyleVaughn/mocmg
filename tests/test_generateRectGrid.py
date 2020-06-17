import gmsh
import mocmg
import logging
import sys
from contextlib import contextmanager
from io import StringIO
from unittest import TestCase

@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

class test_generateRectGrid(TestCase):

    def test_rectGridDefault(self):
        mocmg.initialize(mocmgOption='silent', gmshOption='silent')
        bb = [0, 0, 0, 9, 4, 0]
        PGTagsL1, PGTagsL2, PGNamesL1, PGNamesL2 = mocmg.generateRectGrid(bb, 3, 2)
        IDL1 = list(range(1,7)) 
        IDL2 = list(range(7,13)) 
        namesL1 = ['Grid L1 (1,1)', 'Grid L1 (1,2)', 'Grid L1 (2,1)', 'Grid L1 (2,2)','Grid L1 (3,1)', 'Grid L1 (3,2)']
        namesL2 = ['Grid L2 (1,1)', 'Grid L2 (1,2)', 'Grid L2 (2,1)', 'Grid L2 (2,2)','Grid L2 (3,1)', 'Grid L2 (3,2)']
        self.assertEqual(IDL1, PGTagsL1)
        self.assertEqual(namesL1, PGNamesL1)
        self.assertEqual(IDL2, PGTagsL2)
        print(PGNamesL2)
        self.assertEqual(namesL2, PGNamesL2)
        # Locations/shape of entities
        for ptag in IDL1:
            # Elementary tag
            etag = gmsh.model.getEntitiesForPhysicalGroup(2, ptag)
            self.assertEqual(etag, ptag)
            # Area
            mass = gmsh.model.occ.getMass(2, etag)
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
        # Caputure output since bb will throw warning on purpose
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
            namesL1 = ['Grid L1 (1,1)', 'Grid L1 (1,2)', 'Grid L1 (2,1)', 'Grid L1 (2,2)','Grid L1 (3,1)', 'Grid L1 (3,2)']
            namesL2 = [
                    'Grid L2 (1,1)',\
                    'Grid L2 (1,2)',\
                    'Grid L2 (2,1)',\
                    'Grid L2 (2,2)',\
                    'Grid L2 (3,1)',\
                    'Grid L2 (3,2)',\
                    'Grid L2 (1,3)',\
                    'Grid L2 (1,4)',\
                    'Grid L2 (2,3)',\
                    'Grid L2 (2,4)',\
                    'Grid L2 (3,3)',\
                    'Grid L2 (3,4)',\
                    'Grid L2 (4,1)',\
                    'Grid L2 (4,2)',\
                    'Grid L2 (5,1)',\
                    'Grid L2 (5,2)',\
                    'Grid L2 (6,1)',\
                    'Grid L2 (6,2)',\
                    'Grid L2 (4,3)',\
                    'Grid L2 (4,4)',\
                    'Grid L2 (5,3)',\
                    'Grid L2 (5,4)',\
                    'Grid L2 (6,3)',\
                    'Grid L2 (6,4)',\
                    'Grid L2 (7,1)',\
                    'Grid L2 (7,2)',\
                    'Grid L2 (8,1)',\
                    'Grid L2 (8,2)',\
                    'Grid L2 (9,1)',\
                    'Grid L2 (9,2)',\
                    'Grid L2 (7,3)',\
                    'Grid L2 (7,4)',\
                    'Grid L2 (8,3)',\
                    'Grid L2 (8,4)',\
                    'Grid L2 (9,3)',\
                    'Grid L2 (9,4)'
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
#            gmsh.fltk.run()
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
