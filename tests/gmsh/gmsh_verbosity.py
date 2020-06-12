import gmsh
import sys

def test_gmshVerbosity(N):
    gmshVerbosity = N
    gmsh.initialize()
    gmsh.option.setNumber("General.Terminal", 1)
    gmsh.option.setNumber("General.Verbosity", gmshVerbosity)
    gmsh.model.occ.addDisk(0,0,0,1,1,1)
    gmsh.model.occ.synchronize()
    gmsh.model.mesh.setSize(gmsh.model.getEntities(0), 1)
    gmsh.model.mesh.generate(2)
    gmsh.model.occ.addDisk(0,0,0,1,1,1)
    gmsh.finalize()


arg = int(sys.argv[1])
test_gmshVerbosity(arg)
