"""Ford nuclear reactor."""
import math

import gmsh

import mocmg
import mocmg.mesh
import mocmg.model

lc = 5.0
N = 10

gmsh.initialize()
mocmg.initialize()
gmsh.merge("xsec.step")

# rotate
dim_tags = gmsh.model.getEntities(2)
gmsh.model.occ.rotate(dim_tags, 0, 1, 0, 0, 1, 0, -math.pi / 2)
gmsh.model.occ.translate(dim_tags, 37.3225 - 0.0099 + 1, 44.09 - 0.00174209 + 1, -436.5625)
gmsh.model.occ.synchronize()
# gmsh.fltk.run()

fuel_tags = [20, 10, 5, 32, 38, 6, 15, 27, 31, 11, 12, 13, 33, 4, 36, 9, 25, 21]
clad_tags = [t[1] for t in dim_tags]
for t in fuel_tags:
    if t in clad_tags:
        clad_tags.remove(t)
p = gmsh.model.addPhysicalGroup(2, fuel_tags)
gmsh.model.setPhysicalName(2, p, "MATERIAL_UO2")
p = gmsh.model.addPhysicalGroup(2, clad_tags)
gmsh.model.setPhysicalName(2, p, "MATERIAL_CLAD")

# gmsh.option.setNumber("Geometry.OCCBoundsUseStl", 1)
# bb = gmsh.model.getBoundingBox(-1, -1)
# print(bb)


grid_tags = mocmg.model.rectangular_grid(
    bb=[0, 0, 0, 77, 85, 0], nx=[6], ny=[6], material="MATERIAL_MODERATOR"
)
grid_dim_tags = [(2, tag) for tag in grid_tags]
gmsh.model.occ.synchronize()

mocmg.model.group_preserving_fragment(
    dim_tags + grid_dim_tags, dim_tags + grid_dim_tags, overwrite_material="MATERIAL_MODERATOR"
)
# gmsh.fltk.run()


gmsh.model.mesh.setSize(gmsh.model.getEntities(0), lc)
# gmsh.option.setNumber("Mesh.ElementOrder", 2)
# gmsh.option.setNumber("Mesh.HighOrderOptimize", 2)
gmsh.model.mesh.generate(2)
gmsh.fltk.run()

gmsh.write("FNR_new.inp")
mesh = mocmg.mesh.read_abaqus_file("FNR_new.inp")
mocmg.mesh.write_xdmf_file("grid.xdmf", mesh)

gmsh.finalize()
