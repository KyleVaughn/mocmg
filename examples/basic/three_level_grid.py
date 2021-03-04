"""A three level grid without materials."""
import gmsh
import numpy as np

import mocmg
import mocmg.mesh
import mocmg.model

lc = 1.0

bb_44 = [0.0, 0.0, 0.0, 4.0, 4.0, 0.0]

mocmg.initialize()
gmsh.initialize()

mocmg.model.overlay_rectangular_grid(bb_44, nx=[1, 2, 2], ny=[1, 2, 2])
gmsh.model.removePhysicalGroups([(2, 44)])

gmsh.model.mesh.setSize(gmsh.model.getEntities(0), lc)
# gmsh.option.setNumber("Mesh.ElementOrder", 2)
# gmsh.option.setNumber("Mesh.HighOrderOptimize", 2)
gmsh.model.mesh.setRecombine(2, 1)
gmsh.model.mesh.setRecombine(2, 2)
gmsh.model.mesh.setRecombine(2, 5)
gmsh.model.mesh.setRecombine(2, 6)
gmsh.option.setNumber("Mesh.Algorithm", 8)
gmsh.model.mesh.generate(2)
# gmsh.fltk.run()

gmsh.write("three_level_grid.inp")
mesh = mocmg.mesh.read_abaqus_file("three_level_grid.inp")
# vert_ids = list(mesh.vertices.keys())
# for vid in vert_ids:
#    print(f"{vid}: np.array({mesh.vertices[vid]}),")
# for cell_type in list(mesh.cells.keys()):
#    print(cell_type,":")
#    for cell_id in list(mesh.cells[cell_type].keys()):
#        print(f"{cell_id}: np.array({mesh.cells[cell_type][cell_id]}),")
# for set_name in list(mesh.cell_sets.keys()):
#    print(set_name, mesh.cell_sets[set_name])
for i in range(1, 5):
    for j in range(1, 5):
        set_name = f"GRID_L3_{i}_{j}"
        print("\n" + set_name)
        grid_cells = mesh.get_cells(set_name)
        cell_verts = mesh.get_vertices_for_cells(grid_cells)
        cell_verts_list = np.sort(np.concatenate(cell_verts))
        print("vertices")
        # verts
        for v in cell_verts_list:
            c = mesh.vertices[v]
            print(f"{v}: np.array([{c[0]}, {c[1]}, {c[2]}]),")

        # cells
        print("cells")
        for cell_type in list(mesh.cells.keys()):
            print(cell_type, ":")
            for c in grid_cells:
                if c in list(mesh.cells[cell_type].keys()):
                    print(f"{c}: np.array({mesh.cells[cell_type][c]}),")


# mocmg.mesh.write_xdmf_file("three_level_grid.xdmf", mesh)

gmsh.finalize()
