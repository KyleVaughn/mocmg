"""Ford nuclear reactor."""
import math

import gmsh

import mocmg

lc = 0.25
N = 10

gmsh.initialize()
mocmg.initialize()
gmsh.merge("xsec.step")
# gmsh.model.occ.importShapes('xsec.step')
# gmsh.option.setString('Geometry.OCCTargetUnit', 'CM')

# rotate
dim_tags = gmsh.model.getEntities(2)
gmsh.model.occ.rotate(dim_tags, 0, 1, 0, 0, 1, 0, -math.pi / 2)
gmsh.model.occ.translate(dim_tags, 37.3225 - 0.0099 + 1, 44.09 - 0.00174209 + 1, -436.5625)
gmsh.model.occ.dilate(dim_tags, 0.0, 0.0, 0.0, 0.1, 0.1, 0.0)
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

gmsh.model.occ.synchronize()

mocmg.overlayRectGrid(
    1, 1, nnx=10, nny=10, defaultMat="MATERIAL_MODERATOR", bb=[0, 0, 0, 7.7, 8.5, 0]
)
gmsh.model.occ.synchronize()

gmsh.model.mesh.setSize(gmsh.model.getEntities(0), lc)
# gmsh.option.setNumber("Mesh.ElementOrder", 2)
# gmsh.option.setNumber("Mesh.HighOrderOptimize", 2)
gmsh.model.mesh.generate(2)
gmsh.fltk.run()

gmsh.write("FNR_new.inp")
mesh = mocmg.readAbaqusINP("FNR_new.inp")
mocmg.writeXDMF("FNR_new.xdmf", mesh)

gmsh.finalize()
