import gmsh

def test_gmshVerbosity99():
    gmshVerbosity = 99
    gmsh.initialize()
    gmsh.option.setNumber("General.Terminal", 1)
    gmsh.option.setNumber("General.Verbosity", gmshVerbosity)
    gmsh.model.occ.addDisk(0,0,0,1,1,1)
    gmsh.model.occ.synchronize()
    gmsh.model.mesh.setSize(gmsh.model.getEntities(0), 1)
    gmsh.model.mesh.generate(2)
    gmsh.finalize()

test_gmshVerbosity99()
