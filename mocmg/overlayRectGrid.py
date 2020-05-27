import gmsh
# Function to overlay a rectangular grid onto a 2D geometry that exists solely in
#   the x-y plane.
def overlayRectGrid(nx,ny):
    # Get all 2D model entities 
    modelEntities = gmsh.model.getEntities(2)
    # Get bounding box
    bb = gmsh.model.getBoundingBox(-1,-1)
    # Compute quantities required for grid overlay 
    x_min, y_min, z_min = bb[0:3]
    x_max, y_max, z_max = bb[3:6]
    dx = x_max - x_min # Model width in x direction
    dy = y_max - y_min
    dz = z_max - z_min
    if abs(dz > 1e-3): 
        raise ValueError("Model dx is: %f > 1e-3. Model must exist solely in x-y plane." % dz)
    width = dx/float(nx) # width of rectangle in grid
    height = dy/float(ny) # height of rectangle in grid
    z = bb[5] # z location of the model. Assumed all entities have same z.
    
    # Generate rectangles to fill bounding box
    gridTags = [] # tags of the rectangles
    x = x_min
    for i in range(nx):
        y = y_min
        for j in range(ny):
            gridTags.append(gmsh.model.occ.addRectangle(x,y,z, width, height))
            y = y + dy/float(ny) 
        x = x + dx/float(nx)

    # Fragment the grid components with themselves
    dimGridTags = [(2, tag) for tag in gridTags] # turn tags into tuples of the form (2,x)
#    outGridTags, outGridTagsMap = gmsh.model.occ.fragment(dimGridTags, dimGridTags)
#    # This should only contain the grid tags
#    outGridTags = list(set(outGridTags)) # set then list of list eliminates duplicate values
#    gmsh.model.occ.synchronize()
    # Fragment the grid components with the original model components
    gmsh.model.occ.fragment(dimGridTags, modelEntities)
    gmsh.model.occ.synchronize()
