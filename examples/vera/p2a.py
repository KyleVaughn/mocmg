import gmsh
import mocmg

lc = 0.40

mocmg.initialize()

# Geometry
# 8.5 by 8.5 lattice, 1.26 cm pitch, 
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
        (0, 0),
        (3, 0),
        (6, 0),
        (0, 3),
        (3, 3),
        (6, 3),
        (0, 6),
        (3, 6),
        (5, 5),
        ]
coords_f = []
for i in range(0, 9):
    for j in range(0, 9):
        if not (i, j) in coords_GT:
            coords_f.append((i, j)) 


# Guide tubes
for i, j in coords_GT:
    for radius in R_gt:
        gmsh.model.occ.addDisk(1.26 * i, 1.26 * j, 0, radius, radius)
# Fuel
for i, j in coords_f:
    for radius in R_f:
        gmsh.model.occ.addDisk(1.26 * i, 1.26 * j, 0, radius, radius)
ent = gmsh.model.occ.getEntities(2)
gmsh.model.occ.fragment(ent,ent)

# Trim geometry
ent = gmsh.model.occ.getEntities(2)
t = gmsh.model.occ.addRectangle(0, 0, 0, 1.26*8.5, 1.26*8.5)
gmsh.model.occ.intersect([(2, t)], ent)
gmsh.model.occ.synchronize()

# Materials
ent = gmsh.model.occ.getEntities(2)
tags_fuel = [t[1] for t in ent]

tags_clad = [
        ]

tags_gap = [
        257,
        ]

p = gmsh.model.addPhysicalGroup(2, tags_gap)
gmsh.model.setPhysicalName(2, p, "MATERIAL_GAP")
mocmg.overlayRectGrid(
    1, 1, 17, 17, bb=[0, 0, 0, 21.5/2, 21.5/2, 0], defaultMat="MATERIAL_MODERATOR"
)
gmsh.model.occ.synchronize()


# Mesh
#gmsh.model.mesh.setSize(gmsh.model.getEntities(0), lc)
#gmsh.model.mesh.generate(2)
gmsh.fltk.run()

mocmg.finalize()
