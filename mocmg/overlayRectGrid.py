import gmsh
import logging
from collections import defaultdict

module_log = logging.getLogger('mocmg.overlayRectGrid')

# Function to overlay a rectangular grid onto a 2D geometry that exists solely in
# the x-y plane.
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

    dimGridTags = [(2, tag) for tag in gridTags] # turn tags into tuples of the form (2,x)
    module_log.debug(f'Rectangular grid tags: {dimGridTags}')

    # Fragment the grid components with the original model components
    module_log.info(f'Fragmenting {len(modelEntities)} entities with {len(dimGridTags)} entities')
    outTags, outChildren = gmsh.model.occ.fragment(modelEntities, dimGridTags)
    #
    #
    # IMPORTANT
    # At this point, the occ model entities exist and the original geometric entities do not.
    # However, since the model has not been synchronized, the physical group information about the
    # original geometric entities still exists and can be used. If the model is synchronized this
    # information will be destroyed.
    #
    #

    # Goal: Assign children to parent physical groups
    #
    # Get group tags and group names for original entites. Associate them with children.
    groupChildren = {}
    groupNames = {}
    for i, e in enumerate(modelEntities):
        children = outChildren[i] 
        module_log.debug(f'Entity {e} had children {children}')
        childTags = [t[1] for t in children]
        groupTags = gmsh.model.getPhysicalGroupsForEntity(*e)
        groupTags = list(groupTags)
        if len(groupTags) > 0:            
            module_log.debug(f'Entity {e} had {len(groupTags)} physical groups')
            for tag in groupTags:
                # if group is already known, just add children to set
                # otherwise, add it and its name to dictionaries.
                if tag in groupNames:
                    # Union the current set and the child tags
                    groupChildren[tag] = groupChildren.get(tag).union(set(childTags))
                else:
                    # Add the key and children to the dict
                    groupNames[tag] = gmsh.model.getPhysicalName(2,tag)
                    groupChildren[tag] = set(childTags)
        else:
            module_log.debug(f'Entity {e} had no physical groups')
        # Report group names and children
        module_log.debug(f'Group tag/name dictionary is now : {groupNames}')
        module_log.debug(f'Group tag/child dictionary is now: {groupChildren}')

    # Synchronize and remove old groups
    module_log.info('Synchronizing model')
    gmsh.model.removePhysicalGroups()
    gmsh.model.occ.synchronize()
    module_log.info('Model synchronized')
    # For each group, create a new group with the appropriate children and name
    for tag in groupChildren.keys():
        outTag = gmsh.model.addPhysicalGroup(2, list(groupChildren[tag]), tag)
        if outTag != tag:
            module_log.warning(f'Physical group {tag} could not be assigned to children with original tag.' + \
                    'This could indicate an uncaught error prior to the execution of this code.')
        gmsh.model.setPhysicalName(2, outTag, groupNames[tag])
