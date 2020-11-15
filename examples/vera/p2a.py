import gmsh
import mocmg
import numpy as np

lc = 0.40
lcmin = lc/1.6

mocmg.initialize()

# Geometry
# 17 by 17 lattice, 1.26 cm pitch, 
# Label pinID like MPACT does
#        x 1   2   3   4   5
#      y ---------------------
#      1 | 11| 12| 13| 14| 15|
#        ---------------------
#      2 | 6 | 7 | 8 | 9 | 10|
#        ---------------------
#      3 | 1 | 2 | 3 | 4 | 5 |
#        *--------------------  * is where (0.0,0.0,0.0) is

# Radii. R0 is outermost radius
# Guide tube
R0_gt = 0.602 # clad
R1_gt = 0.561 # water
#R_gt = [R0_gt, R1_gt]
R_mod_gt = mocmg.findLinearDiskRadius_flatField(R1_gt, lcmin) 
R_clad_gt = mocmg.findLinearRingRadius_flatField(R_mod_gt, np.pi*(R0_gt**2 - R1_gt**2), lcmin) 
R_gt = [R_clad_gt, R_mod_gt]
#R_gt = [R0_gt, R_mod_gt]

# Fuel
R0_f = 0.475   # clad
R1_f = 0.418   # gap 
R2_f = 0.4096  # fuel
#R_f = [R0_f, R1_f, R2_f]
R_fuel_f = mocmg.findLinearDiskRadius_flatField(R2_f, lcmin) 
R_gap_f  = mocmg.findLinearRingRadius_flatField(R_fuel_f, np.pi*(R1_f**2 - R2_f**2), lcmin) 
R_clad_f = mocmg.findLinearRingRadius_flatField(R_gap_f, np.pi*(R0_f**2 - R1_f**2), lcmin) 
R_f = [R_clad_f, R_gap_f, R_fuel_f]


# Set (x, y) locations for pins
coords_GT = [
        (6, 15), (9, 15), (12, 15),
        (4, 14), (14, 14),
        (3, 12), (6, 12), (9, 12), (12, 12), (15, 12),
        (3, 9), (6, 9), (9, 9), (12, 9), (15, 9),
        (3, 6), (6, 6), (9, 6), (12, 6), (15, 6),
        (4, 4), (14, 4),
        (6, 3), (9, 3), (12, 3),
        ]
coords_f = []
for i in range(1, 18):
    for j in range(1, 18):
        if not (i, j) in coords_GT:
            coords_f.append((i, j)) 


# Guide tubes
for i, j in coords_GT:
    for radius in R_gt:
        gmsh.model.occ.addDisk(1.26 * i - 1.26/2 + 0.04, 1.26 * j - 1.26/2 + 0.04, 0, radius, radius)
# Fuel
for i, j in coords_f:
    for radius in R_f:
        gmsh.model.occ.addDisk(1.26 * i - 1.26/2 + 0.04, 1.26 * j - 1.26/2 + 0.04, 0, radius, radius)
ent = gmsh.model.occ.getEntities(2)
gmsh.model.occ.fragment(ent,ent)
gmsh.model.occ.synchronize()
#gmsh.fltk.run()

# Materials
ent = gmsh.model.occ.getEntities(2)
tags_fuel = [t[1] for t in ent]

tags_gap = []
for i in range(869, 1397, 2):
    tags_gap.append(i)

tags_clad = []
for t in tags_gap:
    tags_clad.append(t-1)
for i in range(843, 868):
    tags_clad.append(i)

tags_mod = []
for i in range(2,51,2):
    tags_mod.append(i)

for t in tags_gap:
    tags_fuel.remove(t)
for t in tags_clad:
    tags_fuel.remove(t)
for t in tags_mod:
    tags_fuel.remove(t)


p = gmsh.model.addPhysicalGroup(2, tags_gap)
gmsh.model.setPhysicalName(2, p, "MATERIAL_GAP")
p = gmsh.model.addPhysicalGroup(2, tags_clad)
gmsh.model.setPhysicalName(2, p, "MATERIAL_CLAD")
p = gmsh.model.addPhysicalGroup(2, tags_mod)
gmsh.model.setPhysicalName(2, p, "MATERIAL_MOD_GT")
p = gmsh.model.addPhysicalGroup(2, tags_fuel)
gmsh.model.setPhysicalName(2, p, "MATERIAL_UO2-3.1")
mocmg.overlayRectGrid(
    1, 1, 17, 17, bb=[0, 0, 0, 21.5, 21.5, 0], defaultMat="MATERIAL_MODERATOR"
)
gmsh.model.occ.synchronize()
#gmsh.fltk.run()


# Mesh
#gmsh.model.mesh.setSize(gmsh.model.getEntities(0), lc)

gapEnts = mocmg.getEntitiesForPhysicalGroupName(f"MATERIAL_GAP")
gapEnts_dimTags = [(2, t) for t in gapEnts]
gapBounds_dimTags = gmsh.model.getBoundary(
    gapEnts_dimTags, combined=False, oriented=False
)
gapBounds = [t[1] for t in gapBounds_dimTags]

cladEnts = mocmg.getEntitiesForPhysicalGroupName(f"MATERIAL_CLAD")
cladEnts_dimTags = [(2, t) for t in cladEnts]
cladBounds_dimTags = gmsh.model.getBoundary(
    cladEnts_dimTags, combined=False, oriented=False
)
cladBounds = [t[1] for t in cladBounds_dimTags]

gmsh.model.mesh.field.add("MathEval", 1)
gmsh.model.mesh.field.setString(1, "F", f"{lc:.6f}" )

gmsh.model.mesh.field.add("Distance", 2)
gmsh.model.mesh.field.setNumber(2, "NNodesByEdge", 500)
gmsh.model.mesh.field.setNumbers(2, "EdgesList", gapBounds)

gmsh.model.mesh.field.add("Threshold", 3)
gmsh.model.mesh.field.setNumber(3, "IField", 2)
gmsh.model.mesh.field.setNumber(3, "LcMin", lcmin)
gmsh.model.mesh.field.setNumber(3, "LcMax", lc)
gmsh.model.mesh.field.setNumber(3, "DistMin", 0.5 * lcmin)
gmsh.model.mesh.field.setNumber(3, "DistMax", 0.5 * lcmin)

gmsh.model.mesh.field.add("Distance", 4)
gmsh.model.mesh.field.setNumber(4, "NNodesByEdge", 500)
gmsh.model.mesh.field.setNumbers(4, "EdgesList", cladBounds)

gmsh.model.mesh.field.add("Threshold", 5)
gmsh.model.mesh.field.setNumber(5, "IField", 4)
gmsh.model.mesh.field.setNumber(5, "LcMin", lcmin)
gmsh.model.mesh.field.setNumber(5, "LcMax", lc)
gmsh.model.mesh.field.setNumber(5, "DistMin", 0.5 * lcmin)
gmsh.model.mesh.field.setNumber(5, "DistMax", 0.5 * lcmin)


gmsh.model.mesh.field.add("Min", 6)
gmsh.model.mesh.field.setNumbers(6, "FieldsList", [5, 3])


gmsh.model.mesh.field.setAsBackgroundMesh(6)
gmsh.option.setNumber("Mesh.CharacteristicLengthExtendFromBoundary", 0)
gmsh.option.setNumber("Mesh.CharacteristicLengthFromPoints", 0)
gmsh.option.setNumber("Mesh.CharacteristicLengthFromCurvature", 0)
#gmsh.option.setNumber("Mesh.ElementOrder", 2)
#gmsh.option.setNumber("Mesh.HighOrderOptimize", 2)
gmsh.model.mesh.generate(2)
gmsh.fltk.run()

# Convert mesh to XDMF
lcstr = f"{lc:.2f}"
lcstr = lcstr.replace(".", "p")
gmsh.write("p2a_" + lcstr + ".inp")
mesh = mocmg.readAbaqusINP("p2a_" + lcstr + ".inp")

# Area info
print("\nArea info")
elements = mesh.cells
num_elem = 0
for e in elements:
    num_elem = num_elem + len(e[1])
print("Elements: ", num_elem)
total_mesh_area = mesh.getSetArea("GRID_L1_001_001")
uo2_mesh_area = mesh.getSetArea("MATERIAL_UO2-3.1")
gap_mesh_area = mesh.getSetArea("MATERIAL_GAP")
mod_gt_mesh_area = mesh.getSetArea("MATERIAL_MOD_GT")
clad_mesh_area = mesh.getSetArea("MATERIAL_CLAD")
mod_mesh_area = mesh.getSetArea("MATERIAL_MODERATOR") 

total_area = 21.5**2
uo2_area = (17*17-25)*np.pi*R2_f**2
gap_area = (17*17-25)*np.pi*(R1_f**2 - R2_f**2)
mod_gt_area = 25*np.pi*R1_gt**2
clad_area = (17*17-25)*np.pi*(R0_f**2 - R1_f**2) + 25*np.pi*(R0_gt**2 - R1_gt**2)
mod_area = total_area - uo2_area - gap_area - clad_area

print(f'\nTotal area (analytic): {total_area}')
print(f'Total area (computed): {total_mesh_area}')
print(f'Total area error: {100*(total_mesh_area - total_area)/total_area} %\n')

print(f'Fuel area (analytic): {uo2_area}')
print(f'Fuel area (computed): {uo2_mesh_area}')
print(f'Fuel area error: {100*(uo2_mesh_area - uo2_area)/uo2_area} %\n')

print(f'Gap area (analytic): {gap_area}')
print(f'Gap area (computed): {gap_mesh_area}')
print(f'Gap area error: {100*(gap_mesh_area - gap_area)/gap_area} %\n')

print(f'Clad area (analytic): {clad_area}')
print(f'Clad area (computed): {clad_mesh_area}')
print(f'Clad area error: {100*(clad_mesh_area - clad_area)/clad_area} %\n')

print(f'Guide tube moderator area (analytic): {mod_gt_area}')
print(f'Guide tube moderator area (computed): {mod_gt_mesh_area}')
print(f'Guide tube moderator area error: {100*(mod_gt_mesh_area - mod_gt_area)/mod_gt_area} %\n')

print(f'Moderator area (analytic): {mod_area}')
print(f'Moderator area (computed): {mod_mesh_area + mod_gt_area}')
print(f'Moderator area error: {100*(mod_mesh_area + mod_gt_area - mod_area)/mod_area} %\n')


#mocmg.writeXDMF("p2a_" + lcstr + ".xdmf", mesh)
mocmg.finalize()
