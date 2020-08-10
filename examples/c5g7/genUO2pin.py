import mocmg
import gmsh

lc = 0.4

# Geometry
# 1.26 cm pitch, 0.54 cm radius
mocmg.initialize(mocmgOption='debug')
gmsh.model.occ.addDisk(1.26/2, 1.26/2, 0, 0.54, 0.54) 
gmsh.model.occ.synchronize()

# Labels
p = gmsh.model.addPhysicalGroup(2, [1])    
gmsh.model.setPhysicalName(2, p, 'MATERIAL_UO2-3.3')
p = gmsh.model.addPhysicalGroup(2, [1])    
gmsh.model.setPhysicalName(2, p, 'PIN_000001')
mocmg.overlayRectGrid(1,1,bb=[0,0,0,1.26,1.26,0],defaultMat='MATERIAL_MODERATOR')
gmsh.model.occ.synchronize()

# Mesh
gmsh.model.mesh.setSize(gmsh.model.getEntities(0), lc)
gmsh.model.mesh.generate(2)
#gmsh.fltk.run()

# Convert mesh to XDMF
nstr = f'{lc:.2f}'
nstr = nstr.replace('.','p')
gmsh.write('pin_c5g7_lc' + nstr + '.inp')
nodes, elements, elsets = mocmg.readAbaqusINP('pin_c5g7_lc' + nstr + '.inp')

# Give mesh area info
print('Area info')
mesh = mocmg.Mesh(nodes, elements, elsets)
total_area = mesh.getSetArea('GRID_L1_001_001')
print(f'Total area:{total_area}')
uo2_area = mesh.getSetArea('MATERIAL_UO2-3.3')
print(f'UO2 area:{uo2_area}')
pin_area = mesh.getSetArea('PIN_000001')
print(f'Pin area:{pin_area}')
mod_area = mesh.getSetArea('MATERIAL_MODERATOR')
print(f'Moderator area:{mod_area}\n')

# Error checks
print('Error checks')
print('Pin + moderator - total area = 0?', pin_area + mod_area - total_area)
print('Pin - UO2 = 0?', pin_area - uo2_area)

del mesh
# write  xdmf at end since routine deletes nodes, elements, etc to dave memory
mocmg.writeXDMF('pin_c5g7_lc' + nstr + '.xdmf', nodes, elements, elsets)
mocmg.finalize()
