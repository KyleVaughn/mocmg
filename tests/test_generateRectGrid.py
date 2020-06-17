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
        namesL1 = ['Grid L1 (1,1)', 'Grid L1 (1,2)', 'Grid L1 (2,1)', 'Grid L1 (2,2)','Grid L1 (3,1)', 'Grid L1 (3,2)']
        self.assertEqual(IDL1, PGTagsL1)
        self.assertEqual(namesL1, PGNamesL1)
        self.assertEqual([], PGTagsL2)
        self.assertEqual([], PGNamesL2)
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
            namesL2 = []
            for i in range(nx):
                for j in range(ny):
                    for ii in range(nnx):
                        for jj in range(nny):
                            namesL2.append(f'Grid L2 ({i*nx+ii+1}, {j*ny+jj+1})')

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
