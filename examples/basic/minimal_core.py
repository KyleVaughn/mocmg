"""A three level grid with pins in each cell."""
import gmsh

import mocmg
import mocmg.mesh
import mocmg.model

lc = 1.0

bb_44 = [0.0, 0.0, 0.0, 4.0, 4.0, 0.0]

mocmg.initialize()
gmsh.initialize()

for i in range(4):
    for j in range(4):
        gmsh.model.occ.addDisk(i + 0.5, j + 0.5, 0.0, 0.25, 0.25)
gmsh.model.occ.synchronize()

ents = [x for x in range(1, 17)]
p = gmsh.model.addPhysicalGroup(2, ents)
gmsh.model.setPhysicalName(2, p, "MATERIAL_UO2")
mocmg.model.overlay_rectangular_grid(bb_44, nx=[2, 2], ny=[2, 2])

gmsh.model.mesh.setSize(gmsh.model.getEntities(0), lc)
gmsh.model.mesh.generate(2)

gmsh.write("mini_core.inp")
mesh = mocmg.mesh.read_abaqus_file("mini_core.inp")
gridmesh = mocmg.mesh.make_gridmesh(mesh)
mocmg.mesh.write_xdmf_file("mini_core.xdmf", gridmesh, split_level=1)

gmsh.finalize()
