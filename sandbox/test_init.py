import mocmg
import gmsh
mocmg.initialize(option='debug')
mocmg.addDiskLattice(3,1,0.4)
mocmg.overlayRectGrid(3,3)
gmsh.model.mesh.setSize(gmsh.model.getEntities(0), 1e-1)
gmsh.model.mesh.generate(2)
mocmg.finalize()
