import mocmg
import gmsh

lc = 0.15
lcmin = lc/4.0
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
R = mocmg.findLinearDiskRadius(radius, lc)
for j in range(17):
    for i in range(17):
        gmsh.model.occ.addDisk(1.26 / 2 + 1.26 * i, 1.26 / 2 + 1.26 * j, 0, R, R)
gmsh.model.occ.synchronize()

ent = gmsh.model.getEntities(2)
tags_UO2 = [t[1] for t in ent]
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
    tags_UO2.remove(t)
tags_FC = [145]
for t in tags_FC:
    tags_UO2.remove(t)

p = gmsh.model.addPhysicalGroup(2, tags_UO2)
gmsh.model.setPhysicalName(2, p, "MATERIAL_UO2-3.3")
p = gmsh.model.addPhysicalGroup(2, tags_guide)
gmsh.model.setPhysicalName(2, p, "MATERIAL_GUIDE_TUBE")
p = gmsh.model.addPhysicalGroup(2, tags_FC)
gmsh.model.setPhysicalName(2, p, "MATERIAL_FISSION_CHAMBER")
mocmg.overlayRectGrid(
    1, 1, 17, 17, bb=[0, 0, 0, 21.42, 21.42, 0], defaultMat="MATERIAL_MODERATOR"
)
gmsh.model.occ.synchronize()

# Mesh
gmsh.model.mesh.setSize(gmsh.model.getEntities(0), lc)

gmsh.model.mesh.field.add("MathEval", 1)
gmsh.model.mesh.field.setString(1, "F", f"{lc:.6f}" )

gmsh.model.mesh.field.setAsBackgroundMesh(1)
gmsh.option.setNumber("Mesh.CharacteristicLengthExtendFromBoundary", 0)
gmsh.option.setNumber("Mesh.CharacteristicLengthFromPoints", 0)
gmsh.option.setNumber("Mesh.CharacteristicLengthFromCurvature", 0)

gmsh.model.mesh.generate(2)
gmsh.fltk.run()
#
# Convert mesh to XDMF
lcstr = f"{lc:.2f}"
lcstr = lcstr.replace(".", "p")
gmsh.write("uo2_assembly_c5g7_lc" + lcstr + ".inp")
mesh = mocmg.readAbaqusINP("uo2_assembly_c5g7_lc" + lcstr + ".inp")

# Area info
print("Area info")
elements = mesh.cells
num_elem = 0
for e in elements:
    num_elem = num_elem + len(e[1])
print("\nElements: ", num_elem)
total_area = mesh.getSetArea("GRID_L1_001_001")
fc_area = mesh.getSetArea("MATERIAL_FISSION_CHAMBER")
mod_area = mesh.getSetArea("MATERIAL_MODERATOR")
gt_area = mesh.getSetArea("MATERIAL_GUIDE_TUBE")
uo2_area = mesh.getSetArea("MATERIAL_UO2-3.3")
print(f"Fissile area:                   {uo2_area}")
print(f"Fissile area from compliment:   {total_area - fc_area - mod_area - gt_area}")
print(f"Total area: {total_area}")

print("\nError checks")
print(
    f"Fissile area - from compliment: {uo2_area - (total_area - fc_area - mod_area - gt_area)}"
)
print(f"Total actual - computed: {total_area - 21.42**2}")


mocmg.writeXDMF("uo2_assembly_c5g7_lc" + lcstr + ".xdmf", mesh)
mocmg.finalize()
