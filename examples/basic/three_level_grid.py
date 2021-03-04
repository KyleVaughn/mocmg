"""A three level grid without materials."""
import gmsh

import mocmg
import mocmg.mesh
import mocmg.model

lc = 1.0

bb_44 = [0.0, 0.0, 0.0, 4.0, 4.0, 0.0]

mocmg.initialize()
gmsh.initialize()

mocmg.model.overlay_rectangular_grid(bb_44, nx=[1, 2, 2], ny=[1, 2, 2])
gmsh.model.removePhysicalGroups([(2, 44)])

gmsh.model.mesh.setSize(gmsh.model.getEntities(0), lc)
# gmsh.option.setNumber("Mesh.ElementOrder", 2)
# gmsh.option.setNumber("Mesh.HighOrderOptimize", 2)
gmsh.model.mesh.setRecombine(2, 1)
gmsh.model.mesh.setRecombine(2, 2)
gmsh.model.mesh.setRecombine(2, 5)
gmsh.model.mesh.setRecombine(2, 6)
gmsh.option.setNumber("Mesh.Algorithm", 8)
gmsh.model.mesh.generate(2)
# gmsh.fltk.run()

gmsh.write("three_level_grid.inp")
mesh = mocmg.mesh.read_abaqus_file("three_level_grid.inp")
print(mesh.vertices)
mocmg.mesh.write_xdmf_file("three_level_grid.xdmf", mesh)

gmsh.finalize()
