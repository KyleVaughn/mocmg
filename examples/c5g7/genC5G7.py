import mocmg
import gmsh

pi = 3.141592653589793

lc = 0.20
lcmin = 0.04

# Geometry
# Module 1 - UO2-3.3 pin
# Module 2 - MOX-4.3 pin
# Module 3 - MOX-7.0 pin
# Module 4 - MOX-8.7 pin
# Module 5 - Fission Chamber pin
# Module 6 - Guide Tube pin
# Module 7 - Reflector pin

# lattice 1 2*17
#  1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
#  1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
#  1 1 1 1 1 6 1 1 6 1 1 6 1 1 1 1 1
#  1 1 1 6 1 1 1 1 1 1 1 1 1 6 1 1 1
#  1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
#  1 1 6 1 1 6 1 1 6 1 1 6 1 1 6 1 1
#  1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
#  1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
#  1 1 6 1 1 6 1 1 5 1 1 6 1 1 6 1 1
#  1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
#  1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
#  1 1 6 1 1 6 1 1 6 1 1 6 1 1 6 1 1
#  1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
#  1 1 1 6 1 1 1 1 1 1 1 1 1 6 1 1 1
#  1 1 1 1 1 6 1 1 6 1 1 6 1 1 1 1 1
#  1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
#  1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
# lattice 2 2*17
#  2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
#  2 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 2
#  2 3 3 3 3 6 3 3 6 3 3 6 3 3 3 3 2
#  2 3 3 6 3 4 4 4 4 4 4 4 3 6 3 3 2
#  2 3 3 3 4 4 4 4 4 4 4 4 4 3 3 3 2
#  2 3 6 4 4 6 4 4 6 4 4 6 4 4 6 3 2
#  2 3 3 4 4 4 4 4 4 4 4 4 4 4 3 3 2
#  2 3 3 4 4 4 4 4 4 4 4 4 4 4 3 3 2
#  2 3 6 4 4 6 4 4 5 4 4 6 4 4 6 3 2
#  2 3 3 4 4 4 4 4 4 4 4 4 4 4 3 3 2
#  2 3 3 4 4 4 4 4 4 4 4 4 4 4 3 3 2
#  2 3 6 4 4 6 4 4 6 4 4 6 4 4 6 3 2
#  2 3 3 3 4 4 4 4 4 4 4 4 4 3 3 3 2
#  2 3 3 6 3 4 4 4 4 4 4 4 3 6 3 3 2
#  2 3 3 3 3 6 3 3 6 3 3 6 3 3 3 3 2
#  2 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 2
#  2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
#
# lattice 3 2*17
#  7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
#  7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
#  7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
#  7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
#  7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
#  7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
#  7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
#  7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
#  7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
#  7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
#  7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
#  7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
#  7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
#  7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
#  7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
#  7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
#  7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7

# core 360
#   1 2 3
#   2 1 3
#   3 3 3

# Each lattice is has 1.26 cm pitch, 0.54 cm radius if cyl pins
# Label pinID like MPACT does
#        x 1   2   3   4   5
#      y ---------------------
#      1 | 11| 12| 13| 14| 15|
#        ---------------------
#      2 | 6 | 7 | 8 | 9 | 10|
#        ---------------------
#      3 | 1 | 2 | 3 | 4 | 5 |
#        *--------------------  * is where (0.0,0.0,0.0) is


def coord2ID(x, y):
    return (34 - y) * 34 + x


mocmg.initialize(mocmgOption="info")
for j in range(34):
    for i in range(34):
        gmsh.model.occ.addDisk(
            1.26 / 2 + 1.26 * i, 1.26 / 2 + 1.26 * j + 21.42, 0, 0.54, 0.54
        )
gmsh.model.occ.synchronize()

# Labels
# pinID = 1
# for j in range(34):
#    for i in range(33,-1,-1):
#        p = gmsh.model.addPhysicalGroup(2, [pinID])
#        gmsh.model.setPhysicalName(2, p, f'PIN_{pinID:06}')
#        pinID = pinID + 1

# Assign materials using tags of entities, but determine tags from coordinates of pins
# using the diagram above.
# UO2 tags generated by setting all pins to UO2 and removing guide tube and fission chamber pins
coords_UO2 = []
for i in range(1, 18):
    for j in range(1, 18):
        coords_UO2.append((i, j))
for i in range(18, 35):
    for j in range(18, 35):
        coords_UO2.append((i, j))
tags_UO2 = [coord2ID(*c) for c in coords_UO2]
del coords_UO2
# MOX-7.0 by removal of guide tube, fission chamber, 4.3, and 8.7
coords_MOX70 = []
for i in range(1, 18):
    for j in range(18, 35):
        coords_MOX70.append((i, j))
for i in range(18, 35):
    for j in range(1, 18):
        coords_MOX70.append((i, j))
tags_MOX70 = [coord2ID(*c) for c in coords_MOX70]
del coords_MOX70
# Fission chamber
coords_FC = [(9, 9), (26, 9), (26, 26), (9, 26)]
tags_FC = [coord2ID(*c) for c in coords_FC]
del coords_FC
# Guide Tube
coords_GT = [
    (6, 3),
    (9, 3),
    (12, 3),
    (4, 4),
    (14, 4),
    (3, 6),
    (6, 6),
    (9, 6),
    (12, 6),
    (15, 6),
    (3, 9),
    (6, 9),
    (12, 9),
    (15, 9),
    (3, 12),
    (6, 12),
    (9, 12),
    (12, 12),
    (15, 12),
    (4, 14),
    (14, 14),
    (6, 15),
    (9, 15),
    (12, 15),
]
coords_shift = coords_GT.copy()
for c in coords_GT:
    coords_shift.append((c[0] + 17, c[1]))
    coords_shift.append((c[0], c[1] + 17))
    coords_shift.append((c[0] + 17, c[1] + 17))
tags_GT = [coord2ID(*c) for c in coords_shift]
del coords_GT
del coords_shift
# MOX-4.3
coords_MOX43 = []
for i in range(18, 35):
    coords_MOX43.append((i, 1))
    coords_MOX43.append((i, 17))
for i in range(2, 17):
    coords_MOX43.append((18, i))
    coords_MOX43.append((34, i))
coords_shift = coords_MOX43.copy()
for c in coords_MOX43:
    coords_shift.append((c[0] - 17, c[1] + 17))
tags_MOX43 = [coord2ID(*c) for c in coords_shift]
del coords_MOX43
del coords_shift
# MOX-8.7
coords_MOX87 = []
for i in range(6, 13):
    coords_MOX87.append((i, 21))
    coords_MOX87.append((i, 31))
for i in range(5, 14):
    coords_MOX87.append((i, 22))
    coords_MOX87.append((i, 30))
exclude = [
    (6, 23),
    (9, 23),
    (12, 23),
    (6, 26),
    (9, 26),
    (12, 26),
    (6, 29),
    (9, 29),
    (12, 29),
]
for i in range(4, 15):
    for j in range(23, 30):
        if not (i, j) in exclude:
            coords_MOX87.append((i, j))
coords_shift = coords_MOX87.copy()
for c in coords_MOX87:
    coords_shift.append((c[0] + 17, c[1] - 17))
tags_MOX87 = [coord2ID(*c) for c in coords_shift]
del coords_MOX87
del coords_shift

for t in tags_FC:
    if t in tags_UO2:
        tags_UO2.remove(t)
    elif t in tags_MOX70:
        tags_MOX70.remove(t)
for t in tags_GT:
    if t in tags_UO2:
        tags_UO2.remove(t)
    elif t in tags_MOX70:
        tags_MOX70.remove(t)
for t in tags_MOX43:
    if t in tags_MOX70:
        tags_MOX70.remove(t)
for t in tags_MOX87:
    if t in tags_MOX70:
        tags_MOX70.remove(t)

p = gmsh.model.addPhysicalGroup(2, tags_UO2)
gmsh.model.setPhysicalName(2, p, "MATERIAL_UO2-3.3")
p = gmsh.model.addPhysicalGroup(2, tags_MOX70)
gmsh.model.setPhysicalName(2, p, "MATERIAL_MOX-7.0")
p = gmsh.model.addPhysicalGroup(2, tags_FC)
gmsh.model.setPhysicalName(2, p, "MATERIAL_FISSION_CHAMBER")
p = gmsh.model.addPhysicalGroup(2, tags_GT)
gmsh.model.setPhysicalName(2, p, "MATERIAL_GUIDE_TUBE")
p = gmsh.model.addPhysicalGroup(2, tags_MOX43)
gmsh.model.setPhysicalName(2, p, "MATERIAL_MOX-4.3")
p = gmsh.model.addPhysicalGroup(2, tags_MOX87)
gmsh.model.setPhysicalName(2, p, "MATERIAL_MOX-8.7")
mocmg.overlayRectGrid(
    1, 1, 17 * 3, 17 * 3, bb=[0, 0, 0, 64.26, 64.26, 0], defaultMat="MATERIAL_MODERATOR"
)
gmsh.model.occ.synchronize()

# Mesh
# Get all pin entities
# pinEnts = []
# for i in range(1,4*17*17+1):
#    # should only return 1 entity
#    pinEnts.append(*mocmg.getEntitiesForPhysicalGroupName(f'PIN_{i:06}'))

# pinEnts_dimTags = [(2,t) for t in pinEnts]
pinEnts_dimTags = [(2, t) for t in range(1, 34 * 34 + 1)]
pinBounds_dimTags = gmsh.model.getBoundary(
    pinEnts_dimTags, combined=False, oriented=False
)
pinBounds = [t[1] for t in pinBounds_dimTags]

# gmsh.model.mesh.setSize(gmsh.model.getEntities(0), lc)

gmsh.model.mesh.field.add("Distance", 1)
gmsh.model.mesh.field.setNumber(1, "NNodesByEdge", 500)
gmsh.model.mesh.field.setNumbers(1, "EdgesList", pinBounds)
#
gmsh.model.mesh.field.add("Threshold", 2)
gmsh.model.mesh.field.setNumber(2, "IField", 1)
gmsh.model.mesh.field.setNumber(2, "LcMin", lcmin)
gmsh.model.mesh.field.setNumber(2, "LcMax", lc)
gmsh.model.mesh.field.setNumber(2, "DistMin", 0.5 * lcmin)
gmsh.model.mesh.field.setNumber(2, "DistMax", 0.5 * lcmin)
gmsh.model.mesh.field.setAsBackgroundMesh(2)
gmsh.option.setNumber("Mesh.CharacteristicLengthExtendFromBoundary", 0)
gmsh.option.setNumber("Mesh.CharacteristicLengthFromPoints", 0)
gmsh.option.setNumber("Mesh.CharacteristicLengthFromCurvature", 0)
gmsh.model.mesh.generate(2)
gmsh.fltk.run()
#
# Write to abaqus
lcstr = f"{lc:.2f}"
lcstr = lcstr.replace(".", "p")
gmsh.write("c5g7_lc" + lcstr + ".inp")

nodes, elements, elsets = mocmg.readAbaqusINP(sys.argv[1])
# Give mesh info
num_elem = 0
for e in elements:
    num_elem = num_elem + len(e[1])
print("\nElements: ", num_elem)

mesh = mocmg.Mesh(nodes, elements, elsets)
total_area = mesh.getSetArea("GRID_L1_001_001")
uo2 = mesh.getSetArea("MATERIAL_UO2-3.3")
mox70 = mesh.getSetArea("MATERIAL_MOX-7.0")
mox43 = mesh.getSetArea("MATERIAL_MOX-4.3")
mox87 = mesh.getSetArea("MATERIAL_MOX-8.7")
fis = uo2 + mox70 + mox43 + mox87
print(f"Total mesh area: {total_area}")
print("Total mesh area error: ", total_area - 64.26 ** 2)
print(f"Fissile mesh area: {fis}")
print("Fissile mesh area error: ", fis - pi * 0.54 ** 2 * (17 ** 2 - 25) * 4, "\n")

del mesh
mocmg.writeXDMF("c5g7.xdmf", nodes, elements, elsets)
mocmg.finalize()
