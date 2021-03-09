"""Generate a single UO2 assembly from the C5G7 benchmark."""
import gmsh

import mocmg
import mocmg.mesh
import mocmg.model

lc = 0.50
lcmin = lc / 4.0
radius = 0.54

# Geometry
# 17 by 17 lattice, 1.26 cm pitch, 0.54 cm radius
# Label pinID like MPACT does
#        x 1   2   3   4   5
#      y ---------------------
#      1 | 11| 12| 13| 14| 15|
#        ---------------------
#      2 | 6 | 7 | 8 | 9 | 10|
#        ---------------------
#      3 | 1 | 2 | 3 | 4 | 5 |
#        *--------------------  * is where (0.0,0.0,0.0) is


mocmg.initialize()
gmsh.initialize()
for j in range(17):
    for i in range(17):
        gmsh.model.occ.addDisk(1.26 / 2 + 1.26 * i, 1.26 / 2 + 1.26 * j, 0, radius, radius)
gmsh.model.occ.synchronize()

ent = gmsh.model.getEntities(2)
tags_uo2 = [t[1] for t in ent]
tags_guide = [
    40,
    43,
    46,
    55,
    65,
    100,
    97,
    94,
    91,
    88,
    151,
    148,
    142,
    139,
    202,
    199,
    196,
    193,
    190,
    235,
    225,
    250,
    247,
    244,
]
for t in tags_guide:
    tags_uo2.remove(t)
tags_fc = [145]
for t in tags_fc:
    tags_uo2.remove(t)

p = gmsh.model.addPhysicalGroup(2, tags_uo2)
gmsh.model.setPhysicalName(2, p, "MATERIAL_UO2-3.3")
p = gmsh.model.addPhysicalGroup(2, tags_guide)
gmsh.model.setPhysicalName(2, p, "MATERIAL_GUIDE_TUBE")
p = gmsh.model.addPhysicalGroup(2, tags_fc)
gmsh.model.setPhysicalName(2, p, "MATERIAL_FISSION_CHAMBER")
mocmg.model.overlay_rectangular_grid(bb=[0, 0, 0, 21.42, 21.42, 0], nx=[1, 17], ny=[1, 17])
gmsh.fltk.run()

# Mesh
gmsh.model.mesh.setSize(gmsh.model.getEntities(0), lc)

# gmsh.model.mesh.field.add("MathEval", 1)
# gmsh.model.mesh.field.setString(1, "F", f"{lc:.6f}")
#
# gmsh.model.mesh.field.setAsBackgroundMesh(1)
# gmsh.option.setNumber("Mesh.CharacteristicLengthExtendFromBoundary", 0)
# gmsh.option.setNumber("Mesh.CharacteristicLengthFromPoints", 0)
# gmsh.option.setNumber("Mesh.CharacteristicLengthFromCurvature", 0)
gmsh.option.setNumber("Mesh.ElementOrder", 2)
gmsh.option.setNumber("Mesh.HighOrderOptimize", 2)
gmsh.model.mesh.generate(2)
gmsh.fltk.run()
#
# Convert mesh to XDMF
gmsh.write("uo2_assembly.inp")
mesh = mocmg.mesh.read_abaqus_file("uo2_assembly.inp")
gridmesh = mocmg.mesh.make_gridmesh(mesh)
mocmg.mesh.write_xdmf_file("uo2_assembly.xdmf", gridmesh)

gmsh.finalize()
