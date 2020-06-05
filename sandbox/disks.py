import mocmg
import gmsh
mocmg.initialize(option='warning')

gmsh.model.occ.addDisk(0, 0, 0, 1, 1)
gmsh.model.occ.addDisk(0.5, 0, 0, 1, 1)
gmsh.model.occ.synchronize()

gmsh.model.setColor((2,2), 255,0,0)

gmsh.model.addPhysicalGroup(2,[1,2],1)
gmsh.model.addPhysicalGroup(2,[1],2)
gmsh.model.addPhysicalGroup(2,[2],3)

gmsh.model.setPhysicalName(2,1,'Material 1')
gmsh.model.setPhysicalName(2,2,'Disk 1')
gmsh.model.setPhysicalName(2,3,'Disk 2')
gmsh.fltk.run()

mocmg.overlayRectGrid(3,3)
gmsh.model.mesh.setSize(gmsh.model.getEntities(0), 1e-1)
gmsh.model.mesh.generate(2)
gmsh.fltk.run()
mocmg.finalize()
