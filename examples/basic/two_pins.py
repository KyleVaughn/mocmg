"""Create two adjacent, identical single disk fuel pins of different materials."""
import gmsh

import mocmg
import mocmg.mesh
import mocmg.model

lc = 0.5

bb_42 = [0.0, 0.0, 0.0, 4.0, 2.0, 0.0]

mocmg.initialize()
gmsh.initialize()

gmsh.model.occ.addDisk(1.0, 1.0, 0.0, 0.5, 0.5)
gmsh.model.occ.addDisk(3.0, 1.0, 0.0, 0.5, 0.5)
gmsh.model.occ.synchronize()

p = gmsh.model.addPhysicalGroup(2, [1])
gmsh.model.setPhysicalName(2, p, "MATERIAL_UO2")
p = gmsh.model.addPhysicalGroup(2, [2])
gmsh.model.setPhysicalName(2, p, "MATERIAL_MOX")

mocmg.model.overlay_rectangular_grid(bb_42, nx=[1, 2], ny=[1, 1])

gmsh.model.mesh.setSize(gmsh.model.getEntities(0), lc)
gmsh.option.setNumber("Mesh.ElementOrder", 2)
gmsh.option.setNumber("Mesh.HighOrderOptimize", 2)
gmsh.model.mesh.generate(2)
# gmsh.fltk.run()

gmsh.write("two_pins.inp")
mesh = mocmg.mesh.read_abaqus_file("two_pins.inp")
pin1_cells = set(mesh.cell_sets["GRID_L2_2_1"])
for cell_set in list(mesh.cell_sets.keys()):
    print(cell_set, pin1_cells.intersection(set(mesh.cell_sets[cell_set])))

    #    print(cell_set, mesh.cell_sets[cell_set])
# cell_types = list(mesh.cells.keys())
# grid_cells = list(mesh.cells["triangle6"].keys())
# grid_cells = mesh.get_cells("GRID_L2_2_1")
# cell_verts = mesh.get_vertices_for_cells(grid_cells)
# for c in grid_cells:
#    print(f"{c}: np.array({mesh.cells['triangle6'][c]}),")
# grid_verts = mesh.get_vertices("GRID_L2_2_1")
# for v in grid_verts:
#    c = mesh.vertices[v]
#    print(f"{v}: np.array([{c[0]}, {c[1]}, {c[2]}]),")

gmsh.finalize()
