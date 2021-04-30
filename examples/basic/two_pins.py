"""Create two adjacent, identical single disk fuel pins of different materials."""
import gmsh

import mocmg
import mocmg.mesh
import mocmg.model

lc = 0.5

bb_42 = [0.0, 0.0, 0.0, 4.0, 2.0, 0.0]

mocmg.initialize()
gmsh.initialize()

gmsh.model.occ.addDisk(1.0, 1.0, 0.0, 0.5, 0.5)
gmsh.model.occ.addDisk(3.0, 1.0, 0.0, 0.5, 0.5)
gmsh.model.occ.synchronize()

p = gmsh.model.addPhysicalGroup(2, [1, 2])
gmsh.model.setPhysicalName(2, p, "MATERIAL_UO2")
# p = gmsh.model.addPhysicalGroup(2, [2])
# gmsh.model.setPhysicalName(2, p, "MATERIAL_MOX")

mocmg.model.overlay_rectangular_grid(bb_42, nx=[1, 2], ny=[1, 1])

gmsh.model.mesh.setSize(gmsh.model.getEntities(0), lc)
gmsh.option.setNumber("Mesh.ElementOrder", 2)
gmsh.option.setNumber("Mesh.HighOrderOptimize", 2)
gmsh.model.mesh.generate(2)
# gmsh.fltk.run()

gmsh.write("two_pins.inp")
mesh = mocmg.mesh.read_abaqus_file("two_pins.inp")
gridmesh = mocmg.mesh.make_gridmesh(mesh)
mocmg.mesh.write_xdmf_file("two_pins_tri6.xdmf", gridmesh)
gmsh.finalize()
