import mocmg
import gmsh

# 17 by 17 lattice, 1.26 cm pitch, 0.54 cm radius
mocmg.initialize()
for i in range(17):
    for j in range(17):
        gmsh.model.occ.addDisk(1.26/2 + 1.26*i, 1.26/2 + 1.26*j, 0, 0.54, 0.54) 
gmsh.model.occ.synchronize()
ent = gmsh.model.getEntities(2)
tags_UO2 = [t[1] for t in ent]
tags_guide = [40, 43, 46, 55, 65, 100, 97, 94, 91, 88, 151, 148, 142, 139, 202, 199, 196,
        193, 190, 235, 225, 250, 247, 244]
for t in tags_guide:
    tags_UO2.remove(t)
tags_MOX87 = [145]
for t in tags_MOX87:
    tags_UO2.remove(t)
p = gmsh.model.addPhysicalGroup(2, tags_UO2)    
gmsh.model.setPhysicalName(2, p, 'Material_UO2-3.3')
p = gmsh.model.addPhysicalGroup(2, tags_guide)    
gmsh.model.setPhysicalName(2, p, 'Material_Guide_Tube')
p = gmsh.model.addPhysicalGroup(2, tags_MOX87)    
gmsh.model.setPhysicalName(2, p, 'Material_Fission_Chamber')
#gmsh.fltk.run()
#gmsh.write("c5g7_UO2_assembly.step")
mocmg.overlayRectGrid(1,1,17,17,bb=[0,0,0,21.42,21.42,0],defaultMat='Material_Moderator')
gmsh.model.occ.synchronize()
#gmsh.fltk.run()
gmsh.model.mesh.setSize(gmsh.model.getEntities(0), 0.1)
gmsh.model.mesh.generate(2)
gmsh.fltk.run()
gmsh.write("c5g7_UO2_assembly.inp")
nodes, elements, elsets = mocmg.readAbaqusINP("c5g7_UO2_assembly.inp")
mocmg.writeXDMF('c5g7_UO2_assembly.xdmf', nodes, elements, elsets)
mocmg.finalize()
