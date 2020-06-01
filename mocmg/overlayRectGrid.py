import gmsh
import logging
from collections import defaultdict

module_log = logging.getLogger('mocmg.overlayRectGrid')

# Function to overlay a rectangular grid onto a 2D geometry that exists solely in
#   the x-y plane.
def overlayRectGrid(nx,ny):
    module_log.info('Overlaying rectangular grid')

    # Get all 2D model entities 
    modelEntities = gmsh.model.getEntities(2)
    module_log.debug(f'2D entity tags: {modelEntities}')

    # Get bounding box
    bb = gmsh.model.getBoundingBox(-1,-1)

    # Compute quantities required for grid overlay 
    x_min, y_min, z_min = bb[0:3]
    x_max, y_max, z_max = bb[3:6]
    dx = x_max - x_min # Model width in x direction
    dy = y_max - y_min
    dz = z_max - z_min
    if abs(dz > 1e-6): 
        module_log.warning(f"Model thickness is {dz:.6f} > 1e-6. Model expected in 2D x-y plane.")
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
            module_log.debug(f'Added rectangle of width:{width:.2f} and height:{height:.2f} at ({x:.2f},{y:.2f},{z:.2f})')
            y = y + dy/float(ny) 
        x = x + dx/float(nx)

    # Fragment the grid components with themselves
    dimGridTags = [(2, tag) for tag in gridTags] # turn tags into tuples of the form (2,x)
    module_log.debug(f'Rectangular grid tags: {dimGridTags}')

    # Fragment the grid components with the original model components
    module_log.info(f'Fragmenting {len(dimGridTags)} entities with {len(modelEntities)} entities')
    outTags, outChildren = gmsh.model.occ.fragment(modelEntities, dimGridTags)

    # Assign new objects with correct material
    #
    # Get group tags for original entites and their children
    tagData = {}
    for i, e in enumerate(modelEntities):
        children = outChildren[i] 
        childTags = [t[1] for t in children]
        groups = gmsh.model.getPhysicalGroupsForEntity(*e)
        groups = list(groups)
        if len(groups) > 0:            
            for g in groups:
                if g in tagData:
                    # Union the current set and the child tags
                    tagData[g] = tagData.get(g).union(set(childTags))
                else:
                    # Add the key and children to the dict
                    tagData[g] = set(childTags)
#    for e in zip(modelEntities, children):
#        module_log.debug(f'Entity {e[0]} children: {e[1]}')
#
#        groupTags = gmsh.model.getPhysicalGroupsForEntity(e[0][0],e[0][1])
#        module_log.debug(f'Entity {e[0]} groups: {groupTags}')
#        # If the original geometric entitiy had group tags, give them to the new fragments
#        if len(groupTags) > 0:
#            for i in range(len(groupTags)):
#                
#                groupName = gmsh.model.getPhysicalName(2,groupTags[i])
#                module_log.debug(f'Group tag {groupTags[i]} name: {groupName}')

    module_log.info('Synchronizing model')
    gmsh.model.occ.synchronize()
    module_log.info('Model synchronized')
