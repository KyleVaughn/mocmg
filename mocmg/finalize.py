import gmsh

# Just finalize gmsh. Used so initialize and finalize are from same namespace
def finalize():
    gmsh.finalize()
