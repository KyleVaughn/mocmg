import gmsh
import numpy as np

import mocmg
import mocmg.model
import mocmg.mesh

lclist = [0.40, 0.30, 0.25, 0.20, 0.15, 0.12, 0.10]
results = []
results.append(
    (
        "lc",
        "cells",
        "uo2_mesh_area",
        "gap_mesh_area",
        "clad_mesh_area",
        "mod_mesh_area",
    )
)
mocmg.initialize()
gmsh.finalize()
for lc in lclist:
    gmsh.initialize()

    # Geometry
    # Fuel
    R0_f = 0.475  # clad
    R1_f = 0.418  # gap
    R2_f = 0.4096  # fuel
    R_f = [R0_f, R1_f, R2_f]
    #    R_fuel_f = mocmg.findLinearDiskRadius_flatField(R2_f, lcmin)
    #    R_gap_f  = mocmg.findLinearRingRadius_flatField(R_fuel_f, np.pi*(R1_f**2 - R2_f**2), lcmin)
    #    R_clad_f = mocmg.findLinearRingRadius_flatField(R_gap_f, np.pi*(R0_f**2 - R1_f**2), lcmin)
    #    R_f = [R_clad_f, R_gap_f, R_fuel_f]

    for radius in R_f:
        gmsh.model.occ.addDisk(
            1.26 - 1.26/2, 1.26 - 1.26/2, 0, radius, radius
        )
    ent = gmsh.model.occ.getEntities(2)
    gmsh.model.occ.fragment(ent, ent)
    gmsh.model.occ.synchronize()
#    gmsh.fltk.run()

    # Materials
    tags_fuel = [3]
    tags_gap = [5]
    tags_clad = [4]

    p = gmsh.model.addPhysicalGroup(2, tags_gap)
    gmsh.model.setPhysicalName(2, p, "MATERIAL_GAP")
    p = gmsh.model.addPhysicalGroup(2, tags_clad)
    gmsh.model.setPhysicalName(2, p, "MATERIAL_CLAD")
    p = gmsh.model.addPhysicalGroup(2, tags_fuel)
    gmsh.model.setPhysicalName(2, p, "MATERIAL_UO2-3.1")
    mocmg.model.overlay_rectangular_grid(
        nx=[1], ny=[1], bb=[0, 0, 0, 1.26, 1.26, 0], material="MATERIAL_MODERATOR"
    )
    gmsh.model.occ.synchronize()
#    gmsh.fltk.run()

    # Mesh
    gmsh.model.mesh.setSize(gmsh.model.getEntities(0), lc)
    gmsh.model.mesh.field.add("MathEval", 1)
    gmsh.model.mesh.field.setString(1, "F", f"{lc:.6f}")
    gmsh.model.mesh.field.setAsBackgroundMesh(1)
    gmsh.option.setNumber("Mesh.CharacteristicLengthExtendFromBoundary", 0)
    gmsh.option.setNumber("Mesh.CharacteristicLengthFromPoints", 0)
    gmsh.option.setNumber("Mesh.CharacteristicLengthFromCurvature", 0)

    gmsh.option.setNumber("Mesh.RecombineAll", 1)
    gmsh.model.mesh.generate(2)
#    gmsh.model.mesh.setOrder(2)
#    gmsh.model.mesh.optimize("HighOrderElastic")
    gmsh.fltk.run()

    # Convert mesh to XDMF
    lcstr = f"{lc:.2f}"
    lcstr = lcstr.replace(".", "p")
    gmsh.write("p1a_" + lcstr + ".inp")
    gmsh.finalize()
    mesh = mocmg.mesh.read_abaqus_file("p1a_" + lcstr + ".inp")

    # Area info
    print("\nArea info")
    num_cells = mesh.n_cells()
    print("Number of cells: ", num_cells)
    total_mesh_area = mesh.get_set_area("GRID_L1_1_1")
    uo2_mesh_area   = mesh.get_set_area("MATERIAL_UO2-3.1")
    gap_mesh_area   = mesh.get_set_area("MATERIAL_GAP")
    clad_mesh_area  = mesh.get_set_area("MATERIAL_CLAD")
    mod_mesh_area   = mesh.get_set_area("MATERIAL_MODERATOR")

    total_area = 1.26 ** 2
    uo2_area   = np.pi * R2_f ** 2
    gap_area   = np.pi * (R1_f ** 2 - R2_f ** 2)
    clad_area  = np.pi * (R0_f ** 2 - R1_f ** 2)
    mod_area   = total_area - uo2_area - gap_area - clad_area

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

    gridmesh = mocmg.mesh.make_gridmesh(mesh)
    mocmg.mesh.write_xdmf_file("p1a_" + lcstr + ".xdmf", gridmesh)
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
