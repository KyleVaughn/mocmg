import mocmg
import gmsh

lc = 0.30

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
#gmsh.model.mesh.setSize(gmsh.model.getEntities(0), lc)
gmsh.model.mesh.field.add("Distance", 1)
#gmsh.model.mesh.field.setNumbers(1, "NodesList", [5])
gmsh.model.mesh.field.setNumber(1, "NNodesByEdge", 100)
gmsh.model.mesh.field.setNumbers(1, "EdgesList", [5])

gmsh.model.mesh.field.add("Threshold", 2)
gmsh.model.mesh.field.setNumber(2, "IField", 1)
gmsh.model.mesh.field.setNumber(2, "LcMin", 0.01)
gmsh.model.mesh.field.setNumber(2, "LcMax", lc)
gmsh.model.mesh.field.setNumber(2, "DistMin", 0.0)
gmsh.model.mesh.field.setNumber(2, "DistMax", 0.02)
gmsh.model.mesh.field.setAsBackgroundMesh(2)
# Makes interior of disk all one size
gmsh.option.setNumber("Mesh.CharacteristicLengthExtendFromBoundary", 0)
gmsh.option.setNumber("Mesh.CharacteristicLengthFromPoints", 0)
gmsh.option.setNumber("Mesh.CharacteristicLengthFromCurvature", 0)
gmsh.model.mesh.generate(2)
gmsh.fltk.run()

# Convert mesh to XDMF
nstr = f'{lc:.2f}'
nstr = nstr.replace('.','p')
gmsh.write('pin_c5g7_dynamic_lc' + nstr + '.inp')
nodes, elements, elsets = mocmg.readAbaqusINP('pin_c5g7_dynamic_lc' + nstr + '.inp')

# Give mesh area info
print('Area info')
mesh = mocmg.Mesh(nodes, elements, elsets)
total_area = mesh.getSetArea('GRID_L1_001_001')
print(f'Total area: {total_area}')
uo2_area = mesh.getSetArea('MATERIAL_UO2-3.3')
print(f'UO2 area: {uo2_area}')
pin_area = mesh.getSetArea('PIN_000001')
print(f'Pin area: {pin_area}')
mod_area = mesh.getSetArea('MATERIAL_MODERATOR')
print(f'Moderator area: {mod_area}\n')

# Error checks
print('Error checks')
print('Pin + moderator - total area = 0?', pin_area + mod_area - total_area)
print('Pin - UO2 = 0?', pin_area - uo2_area)

del mesh
# write  xdmf at end since routine deletes nodes, elements, etc to dave memory
mocmg.writeXDMF('pin_c5g7_dynamic_lc' + nstr + '.xdmf', nodes, elements, elsets)
mocmg.finalize()
