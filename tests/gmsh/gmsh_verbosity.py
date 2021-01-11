import sys

import gmsh


def test_gmshVerbosity(N):
    gmshVerbosity = N
    gmsh.initialize()
    gmsh.option.setNumber("General.Terminal", 1)
    gmsh.option.setNumber("General.Verbosity", gmshVerbosity)
    gmsh.model.occ.addDisk(0, 0, 0, 1, 1, 1)
    gmsh.model.occ.synchronize()  # produce debug
    gmsh.model.mesh.setSize(gmsh.model.getEntities(0), 1)
    gmsh.model.mesh.generate(2)  # produce info
    gmsh.initialize()  # produce warning
    gmsh.model.occ.addDisk(0, 0, 0, 1, 1, 1)  # produce error
    gmsh.finalize()


arg = int(sys.argv[1])
test_gmshVerbosity(arg)
