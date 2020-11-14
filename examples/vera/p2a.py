import gmsh
import mocmg

lc = 0.40

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
R_gt = [R0_gt, R1_gt]

# Fuel
R0_f = 0.475   # clad
R1_f = 0.418   # gap 
R2_f = 0.4096  # fuel
R_f = [R0_f, R1_f, R2_f]

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
for i in range(2,52,2):
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


# Mesh
#gmsh.model.mesh.setSize(gmsh.model.getEntities(0), lc)
#gmsh.model.mesh.generate(2)
gmsh.fltk.run()

mocmg.finalize()
