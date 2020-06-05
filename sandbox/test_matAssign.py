import gmsh

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)

tags = []
tags.append(gmsh.model.occ.addDisk(0, 0, 0, 1, 1))
tags.append(gmsh.model.occ.addDisk(0.5, 0, 0, 1, 1))
gmsh.model.occ.synchronize()

gmsh.model.addPhysicalGroup(2,[1],1)
gmsh.model.addPhysicalGroup(2,[2],2)

gmsh.model.setPhysicalName(2,1,'Material 1')
gmsh.model.setPhysicalName(2,2,'Material 2')

dimTags = [(2, tag) for tag in tags]

#gmsh.model.occ.synchronize()
gmsh.fltk.run()

ov, ovv = gmsh.model.occ.fragment(dimTags, dimTags, removeObject = False, removeTool = False)
for e in zip(dimTags, ovv):
    print("parent " + str(e[0]) + " -> child " + str(e[1]))
    groupTags = gmsh.model.getPhysicalGroupsForEntity(e[0][0],e[0][1])
    if len(groupTags) > 0:
        print(gmsh.model.getPhysicalName(2,groupTags[0]))

gmsh.model.occ.synchronize()
gmsh.fltk.run()
gmsh.finalize()
