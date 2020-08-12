import mocmg
import gmsh

lc = 0.03

# Geometry
# 17 by 17 lattice, 1.26 cm pitch, 0.54 cm radius
# Label pinID like MPACT does
#        x 1   2   3   4   5
#      y ---------------------
#      1 | 11| 12| 13| 14| 15|
#        ---------------------
#      2 | 6 | 7 | 8 | 9 | 10|
#        ---------------------
#      3 | 1 | 2 | 3 | 4 | 5 |
#        *--------------------  * is where (0.0,0.0,0.0) is


mocmg.initialize()
for j in range(17):
    for i in range(17):
        gmsh.model.occ.addDisk(1.26/2 + 1.26*i, 1.26/2 + 1.26*j, 0, 0.54, 0.54) 
gmsh.model.occ.synchronize()

# Labels
pinID = 1
for j in range(17):
    for i in range(16,-1,-1):
        p = gmsh.model.addPhysicalGroup(2, [pinID])
        gmsh.model.setPhysicalName(2, p, f'PIN_{pinID:06}')
        pinID = pinID + 1
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
gmsh.model.setPhysicalName(2, p, 'MATERIAL_UO2-3.3')
p = gmsh.model.addPhysicalGroup(2, tags_guide)    
gmsh.model.setPhysicalName(2, p, 'MATERIAL_GUIDE_TUBE')
p = gmsh.model.addPhysicalGroup(2, tags_MOX87)    
gmsh.model.setPhysicalName(2, p, 'MATERIAL_FISSION_CHAMBER')
mocmg.overlayRectGrid(1,1,17,17,bb=[0,0,0,21.42,21.42,0],defaultMat='MATERIAL_MODERATOR')
gmsh.model.occ.synchronize()
 
# Mesh 
gmsh.model.mesh.setSize(gmsh.model.getEntities(0), lc)
gmsh.model.mesh.generate(2)
#gmsh.fltk.run()

# Convert mesh to XDMF
lcstr = f'{lc:.2f}'
lcstr = lcstr.replace('.','p')
gmsh.write('uo2_assembly_c5g7_lc' + lcstr + '.inp')
nodes, elements, elsets = mocmg.readAbaqusINP('uo2_assembly_c5g7_lc' + lcstr + '.inp')

# Area info
print('Area info')
mesh = mocmg.Mesh(nodes, elements, elsets)
total_area = mesh.getSetArea('GRID_L1_001_001')
uo2_area = mesh.getSetArea('MATERIAL_UO2-3.3')
gt_area = mesh.getSetArea('MATERIAL_GUIDE_TUBE')
fc_area = mesh.getSetArea('MATERIAL_FISSION_CHAMBER')
fis_area = uo2_area + gt_area + fc_area
pin_area = 0.0
for i in range(1,290):
    pin_area = pin_area + mesh.getSetArea(f'PIN_{i:06}')
mod_area = mesh.getSetArea('MATERIAL_MODERATOR')
print(f'Total area: {total_area}')
print(f'Fissile area: {fis_area}')
print(f'Pin area: {pin_area}')
print(f'Moderator area: {mod_area}\n')

# Error checks
print('Error checks')
print('Pin + moderator - total area = 0?', pin_area + mod_area - total_area)
print('Pin - fissile = 0?', pin_area - fis_area)


del mesh
mocmg.writeXDMF('uo2_assembly_c5g7_lc' + lcstr + '.xdmf', nodes, elements, elsets)
mocmg.finalize()
