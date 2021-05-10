"""Generates the VERA Problem 2A benchmark mesh."""
import gmsh
import numpy as np

import mocmg
import mocmg.mesh
import mocmg.model

lclist = [0.40, 0.30, 0.25, 0.20, 0.15, 0.12, 0.10]
# lclist = [0.35]
results = []
results.append(
    (
        "lc",
        "elems",
        "uo2_mesh_area",
        "gap_mesh_area",
        "clad_mesh_area",
        "mod_mesh_area",
    )
)
mocmg.initialize()
gmsh.initialize()
# Not thread safe
# gmsh.option.setNumber("General.NumThreads", 4)

# Geometry
# 17 by 17 lattice, 1.26 cm pitch,

# Radii. R0 is outermost radius
# Guide tube
R0_gt = 0.602  # clad
R1_gt = 0.561  # water
R_gt = [R0_gt, R1_gt]
#    R_mod_gt = mocmg.findLinearDiskRadius_flatField(R1_gt, lcmin)
#    R_clad_gt = mocmg.findLinearRingRadius_flatField(R_mod_gt, np.pi*(R0_gt**2 - R1_gt**2), lcmin)
#    R_gt = [R_clad_gt, R_mod_gt]

# Fuel
R0_f = 0.475  # clad
R1_f = 0.418  # gap
R2_f = 0.4096  # fuel
R_f = [R0_f, R1_f, R2_f]
#    R_fuel_f = mocmg.findLinearDiskRadius_flatField(R2_f, lcmin)
#    R_gap_f  = mocmg.findLinearRingRadius_flatField(R_fuel_f, np.pi*(R1_f**2 - R2_f**2), lcmin)
#    R_clad_f = mocmg.findLinearRingRadius_flatField(R_gap_f, np.pi*(R0_f**2 - R1_f**2), lcmin)
#    R_f = [R_clad_f, R_gap_f, R_fuel_f]

# Set (x, y) locations for pins
coords_gt = [
    (6, 15),
    (9, 15),
    (12, 15),
    (4, 14),
    (14, 14),
    (3, 12),
    (6, 12),
    (9, 12),
    (12, 12),
    (15, 12),
    (3, 9),
    (6, 9),
    (9, 9),
    (12, 9),
    (15, 9),
    (3, 6),
    (6, 6),
    (9, 6),
    (12, 6),
    (15, 6),
    (4, 4),
    (14, 4),
    (6, 3),
    (9, 3),
    (12, 3),
]
coords_f = []
for i in range(1, 18):
    for j in range(1, 18):
        if not (i, j) in coords_gt:
            coords_f.append((i, j))

# Guide tubes
for i, j in coords_gt:
    elem_list = []
    for radius in R_gt:
        elem = gmsh.model.occ.addDisk(
            1.26 * i - 1.26 / 2 + 0.04, 1.26 * j - 1.26 / 2 + 0.04, 0, radius, radius
        )
        elem_list.append(elem)
    elem_dimtags = [(2, e) for e in elem_list]
    gmsh.model.occ.cut([elem_dimtags[0]], [elem_dimtags[1]])
gt_dimtags = gmsh.model.occ.getEntities(2)
gt_tags = [dt[1] for dt in gt_dimtags]

# Fuel
for i, j in coords_f:
    elem_list = []
    for radius in R_f:
        elem = gmsh.model.occ.addDisk(
            1.26 * i - 1.26 / 2 + 0.04, 1.26 * j - 1.26 / 2 + 0.04, 0, radius, radius
        )
        elem_list.append(elem)
    elem_dimtags = [(2, e) for e in elem_list]
    gmsh.model.occ.fragment(elem_dimtags, elem_dimtags)
gmsh.model.occ.synchronize()
# gmsh.fltk.run()

# Materials
ent = gmsh.model.occ.getEntities(2)
tags_fuel = [t[1] for t in ent]

tags_gap = []
for i in range(30, 1346, 5):
    tags_gap.append(i)

tags_clad = []
for i in range(1, 26):
    tags_clad.append(i)
for i in range(29, 1345, 5):
    tags_clad.append(i)

for t in tags_gap:
    tags_fuel.remove(t)
for t in tags_clad:
    tags_fuel.remove(t)


gmsh.model.occ.synchronize()
p = gmsh.model.addPhysicalGroup(2, tags_gap)
gmsh.model.setPhysicalName(2, p, "MATERIAL_GAP")
p = gmsh.model.addPhysicalGroup(2, tags_clad)
gmsh.model.setPhysicalName(2, p, "MATERIAL_CLAD")
p = gmsh.model.addPhysicalGroup(2, tags_fuel)
gmsh.model.setPhysicalName(2, p, "MATERIAL_UO2-3.1")
# gmsh.fltk.run()

# Overlay rectangular grid. Account for offset by generating lines manually
x = [[1.26 * i + 0.04 for i in range(1, 17)]]
y = x
mocmg.model.overlay_rectangular_grid(
    bb=[0, 0, 0, 21.5, 21.5, 0], material="MATERIAL_MODERATOR", x=x, y=y
)
gmsh.model.occ.synchronize()
# gmsh.fltk.run()


for i, lc in enumerate(lclist):
    # Mesh
    gmsh.model.mesh.setSize(gmsh.model.getEntities(0), lc)
    gmsh.model.mesh.field.add("MathEval", i)
    gmsh.model.mesh.field.setString(i, "F", f"{lc:.6f}")
    gmsh.model.mesh.field.setAsBackgroundMesh(i)
    # gmsh.option.setNumber("Mesh.CharacteristicLengthExtendFromBoundary", 0)
    # gmsh.option.setNumber("Mesh.CharacteristicLengthFromPoints", 0)
    # gmsh.option.setNumber("Mesh.CharacteristicLengthFromCurvature", 0)

    # Quads
    gmsh.option.setNumber("Mesh.RecombineAll", 1)
    gmsh.option.setNumber("Mesh.Algorithm", 8)
    gmsh.option.setNumber("Mesh.RecombinationAlgorithm", 1)
    gmsh.option.setNumber("Mesh.CharacteristicLengthExtendFromBoundary", 0)
    gmsh.option.setNumber("Mesh.CharacteristicLengthFromPoints", 0)
    gmsh.option.setNumber("Mesh.CharacteristicLengthFromCurvature", 0)

    gmsh.model.mesh.generate(2)

    # First order triangles
    # niter = 2
    # for n in range(niter):
    #     gmsh.model.mesh.optimize("Laplace2D")

    # First order quad
    # niter = 2
    # for n in range(niter):
    #    gmsh.model.mesh.optimize("Laplace2D")
    #    gmsh.model.mesh.optimize("Relocate2D")
    #    gmsh.model.mesh.optimize("Laplace2D")

    # Second order triangles
    # gmsh.option.setNumber("Mesh.HighOrderDistCAD", 1)
    # gmsh.model.mesh.setOrder(2)
    # niter = 2
    # for n in range(niter):
    #    gmsh.model.mesh.optimize("HighOrderElastic")
    #    gmsh.model.mesh.optimize("Relocate2D")
    #    gmsh.model.mesh.optimize("HighOrderElastic")

    # Second order quad
    gmsh.option.setNumber("Mesh.HighOrderDistCAD", 1)
    gmsh.model.mesh.setOrder(2)
    niter = 2
    for _n in range(niter):
        gmsh.model.mesh.optimize("HighOrderElastic")
        gmsh.model.mesh.optimize("Relocate2D")
        gmsh.model.mesh.optimize("HighOrderElastic")

    gmsh.fltk.run()

    # Convert mesh to XDMF
    lcstr = f"{lc:.2f}"
    lcstr = lcstr.replace(".", "p")
    gmsh.write("p2a_" + lcstr + ".inp")
    gmsh.model.mesh.clear()
    mesh = mocmg.mesh.read_abaqus_file("p2a_" + lcstr + ".inp")
    gridmesh = mocmg.mesh.make_gridmesh(mesh)

    # Area info
    print("\nArea info")
    num_cells = mesh.n_cells()
    print("Number of cells: ", num_cells)
    total_mesh_area = 0.0
    for i in range(1, 18):
        istr = str(i).zfill(2)
        for j in range(1, 18):
            jstr = str(j).zfill(2)
            total_mesh_area += mesh.get_set_area("GRID_L1_" + istr + "_" + jstr)
    uo2_mesh_area = mesh.get_set_area("MATERIAL_UO2-3.1")
    gap_mesh_area = mesh.get_set_area("MATERIAL_GAP")
    clad_mesh_area = mesh.get_set_area("MATERIAL_CLAD")
    mod_mesh_area = mesh.get_set_area("MATERIAL_MODERATOR")

    total_area = 21.5 ** 2
    uo2_area = np.pi * (R2_f ** 2) * (17 * 17 - 25)
    gap_area = np.pi * (R1_f ** 2 - R2_f ** 2) * (17 * 17 - 25)
    clad_area = np.pi * ((17 * 17 - 25) * (R0_f ** 2 - R1_f ** 2) + 25 * (R0_gt ** 2 - R1_gt ** 2))
    mod_area = total_area - uo2_area - gap_area - clad_area

    print(f"\nTotal area (analytic): {total_area}")
    print(f"Total area (computed): {total_mesh_area}")
    print(f"Total area error: {100*(total_mesh_area - total_area)/total_area} %\n")

    print(f"Fuel area (analytic): {uo2_area}")
    print(f"Fuel area (computed): {uo2_mesh_area}")
    print(f"Fuel area error: {100*(uo2_mesh_area - uo2_area)/uo2_area} %\n")

    print(f"Gap area (analytic): {gap_area}")
    print(f"Gap area (computed): {gap_mesh_area}")
    print(f"Gap area error: {100*(gap_mesh_area - gap_area)/gap_area} %\n")

    print(f"Clad area (analytic): {clad_area}")
    print(f"Clad area (computed): {clad_mesh_area}")
    print(f"Clad area error: {100*(clad_mesh_area - clad_area)/clad_area} %\n")

    print(f"Moderator area (analytic): {mod_area}")
    print(f"Moderator area (computed): {mod_mesh_area}")
    print(f"Moderator area error: {100*(mod_mesh_area - mod_area)/mod_area} %\n")

    mocmg.mesh.write_xdmf_file("p2a_" + lcstr + ".xdmf", gridmesh)
    results.append(
        (
            lc,
            num_cells,
            uo2_mesh_area,
            gap_mesh_area,
            clad_mesh_area,
            mod_mesh_area,
        )
    )

    f = open("./info.txt", "w")
    for line in results:
        f.write(", ".join(map(str, line)) + "\n")
    f.close()

gmsh.finalize()
