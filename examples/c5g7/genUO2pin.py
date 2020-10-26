import mocmg
import gmsh
import os

pi = 3.141592653589793

lc = 0.20
lcmin = 0.04

# Geometry
# 1.26 cm pitch, 0.54 cm radius
mocmg.initialize(mocmgOption="debug", gmshOption="debug")
gmsh.model.occ.addDisk(1.26 / 2, 1.26 / 2, 0, 0.54, 0.54)
gmsh.model.occ.synchronize()

# Labels
p = gmsh.model.addPhysicalGroup(2, [1])
gmsh.model.setPhysicalName(2, p, "MATERIAL_UO2-3.3")
p = gmsh.model.addPhysicalGroup(2, [1])
gmsh.model.setPhysicalName(2, p, "PIN_000001")
mocmg.overlayRectGrid(
    1, 1, bb=[0, 0, 0, 1.26, 1.26, 0], defaultMat="MATERIAL_MODERATOR"
)
gmsh.model.occ.synchronize()

# Mesh
gmsh.model.mesh.setSize(gmsh.model.getEntities(0), lc)
#
gmsh.model.mesh.field.add("MathEval", 1)
gmsh.model.mesh.field.setString(1, "F", str(lc))

gmsh.model.mesh.field.add("Distance", 2)
gmsh.model.mesh.field.setNumber(2, "NNodesByEdge", 500)
gmsh.model.mesh.field.setNumbers(2, "EdgesList", [5])

gmsh.model.mesh.field.add("Threshold", 3)
gmsh.model.mesh.field.setNumber(3, "IField", 2)
gmsh.model.mesh.field.setNumber(3, "LcMin", lcmin)
gmsh.model.mesh.field.setNumber(3, "LcMax", lc)
gmsh.model.mesh.field.setNumber(3, "DistMin", 0.5 * lcmin)
gmsh.model.mesh.field.setNumber(3, "DistMax", 0.5 * lcmin)

gmsh.model.mesh.field.add("Restrict", 4)
gmsh.model.mesh.field.setNumber(4, "IField", 3)
gmsh.model.mesh.field.setNumbers(4, "FacesList", [1])

gmsh.model.mesh.field.add("Min", 5)
gmsh.model.mesh.field.setNumbers(5, "FieldsList", [4, 1])

# gmsh.model.mesh.field.setAsBackgroundMesh(3)
## Makes interior of disk all one size
# gmsh.option.setNumber("Mesh.CharacteristicLengthExtendFromBoundary", 0)
# gmsh.option.setNumber("Mesh.CharacteristicLengthFromPoints", 0)
# gmsh.option.setNumber("Mesh.CharacteristicLengthFromCurvature", 0)
# gmsh.merge('field.pos')
# bg_field = gmsh.model.mesh.field.add("PostView")
# gmsh.model.mesh.field.setAsBackgroundMesh(bg_field)
gmsh.model.mesh.generate(2)
gmsh.fltk.run()

# Convert mesh to XDMF
nstr = f"{lc:.2f}"
nstr = nstr.replace(".", "p")
gmsh.write("pin_c5g7_dynamic_lc" + nstr + ".inp")
nodes, elements, elsets = mocmg.readAbaqusINP("pin_c5g7_dynamic_lc" + nstr + ".inp")

# Give mesh info
num_elem = 0
for e in elements:
    num_elem = num_elem + len(e[1])
print("\nElements: ", num_elem)

mesh = mocmg.Mesh(nodes, elements, elsets)
total_area = mesh.getSetArea("GRID_L1_001_001")
uo2_area = mesh.getSetArea("MATERIAL_UO2-3.3")
print(f"Total mesh area: {total_area}")
print("Total mesh area error: ", total_area - 1.26 ** 2)
print(f"UO2 mesh area: {uo2_area}")
print("UO2 mesh area error: ", uo2_area - pi * 0.54 ** 2, "\n")

del mesh
# write  xdmf at end since routine deletes nodes, elements, etc to dave memory
mocmg.writeXDMF("pin_c5g7_dynamic_lc" + nstr + ".xdmf", nodes, elements, elsets)
mocmg.finalize()
