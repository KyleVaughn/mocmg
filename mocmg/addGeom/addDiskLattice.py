import gmsh
def addDiskLattice(n):
    x = 0 
    for i in range(n):
        y = 0 
        for j in range(n):
            gmsh.model.occ.addDisk(x, y, 0, 0.2, 0.2)
            y = y + 1 
        x = x + 1 
    gmsh.model.occ.synchronize()
