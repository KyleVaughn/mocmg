import mocmg
import gmsh

N = 64 

mocmg.initialize(option='warning')

mocmg.addDiskLattice(N, 1.26, 0.95)

entities = gmsh.model.getEntities(2)
entitiesTags = [t[1] for t in entities]
gmsh.model.addPhysicalGroup(2,[entitiesTags],1)
gmsh.model.setPhysicalName(2,1,'Material 1')

mocmg.overlayRectGrid(N,N)


gmsh.model.mesh.setSize(gmsh.model.getEntities(0), 1e-1)
gmsh.write("model.geo_unrolled")

mocmg.finalize()
