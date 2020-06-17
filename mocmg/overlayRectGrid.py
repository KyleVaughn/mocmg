import gmsh
import logging
from collections import defaultdict
from .generateRectGrid import generateRectGrid

module_log = logging.getLogger(__name__)

# NOTE: Remember to synchronize the model before using this function

def overlayRectGrid(nx,ny,nnx=1,nny=1,defaultMat='Material Void',bb=None):
    module_log.info('Overlaying rectangular grid')

# 1. Get all 2D model entities 
    modelDimTags = gmsh.model.getEntities(2)
    module_log.debug(f'2D entity tags: {modelEntities}')

# 2. Get bounding box
    if bb == None:
        bb = gmsh.model.getBoundingBox(-1,-1)
        module_log.debug(f'Model bounding box: {bb}')
    else:
        module_log.warning(f'Bounding box for rectangular grid manually specified. Use caution. Box: {bb}')

# 3. Generate rectangular grid
    pGroupTagsL1, pGroupTagsL2, pGroupNamesL1, pGroupNamesL2 = generateRectGrid(bb,nx,ny,nnx,nny)

# 4. Fragment the grid components with the original model components
    # Generate a list of all elementary entities in the grid
    gridTags = set()
    if nnx == 1 and nny == 1:
        # No L2 if nnx = nny = 1
        for ptag in pGroupTagsL1:
            elemTags = gmsh.model.getEntitiesForPhysicalGroup(2, ptag)
            gridTags.union(set(elemTags))
    else:
        for ptag in pGroupTagsL2:
            elemTags = gmsh.model.getEntitiesForPhysicalGroup(2, ptag)
            gridTags.union(set(elemTags))

    module_log.info(f'Fragmenting {len(modelDimTags)} entities with {len(gridDimTags)} entities')
    outTags, outChildren = gmsh.model.occ.fragment(modelEntities, dimGridTags)
    #
    #
    # NOTE
    # At this point, the occ model entities exist and the original geometric entities do not.
    # However, since the model has not been synchronized, the physical group information about the
    # original geometric entities still exists and can be used. If the model is synchronized this
    # information will be destroyed.
    #
    #

## 4. Assign new entities to parent physical groups
#    #
#    # Get group tags and group names for original entites. Associate them with children.
#    groupChildren = {}
#    groupNames = {}
#    for i, e in enumerate(modelEntities):
#        children = outChildren[i] 
#        module_log.debug(f'Entity {e} had children {children}')
#        childTags = [t[1] for t in children]
#        groupTags = gmsh.model.getPhysicalGroupsForEntity(*e)
#        groupTags = list(groupTags)
#        if len(groupTags) > 0:            
#            module_log.debug(f'Entity {e} had {len(groupTags)} physical groups')
#            for tag in groupTags:
#                # if group is already known, just add children to set
#                # otherwise, add it and its name to dictionaries.
#                if tag in groupNames:
#                    # Union the current set and the child tags
#                    groupChildren[tag] = groupChildren[tag].union(set(childTags))
#                else:
#                    # Add the key and children to the dict
#                    groupNames[tag] = gmsh.model.getPhysicalName(2,tag)
#                    groupChildren[tag] = set(childTags)
#        else:
#            module_log.debug(f'Entity {e} had no physical groups')
#        # Report group names and children
#        module_log.debug(f'Group tag/name dictionary is now : {groupNames}')
#        module_log.debug(f'Group tag/child dictionary is now: {groupChildren}')
#
#    # Synchronize and remove old groups
#    module_log.info('Synchronizing model')
#    gmsh.model.removePhysicalGroups()
#    gmsh.model.occ.synchronize()
#    module_log.info('Model synchronized')
#
#    # For each group, create a new group with the appropriate children and name
#    for tag in groupChildren.keys():
#        outTag = gmsh.model.addPhysicalGroup(2, list(groupChildren[tag]), tag)
#        if outTag != tag:
#            module_log.warning(f'Physical group {tag} could not be assigned to children with original tag.' + \
#                    'This could indicate an uncaught error prior to the execution of this code.')
#        gmsh.model.setPhysicalName(2, outTag, groupNames[tag])
#
## 5. Group new entities based on which grid entity they reside in
#
## 6. Assign a default material to any entity that didn't inherit a material from parent.
#    # This should just be {bounding box}\{original geometry}
#    allEntities = gmsh.model.getEntities(2)
#    allEntitiesTags = set([t[1] for t in allEntities])
#    del allEntities # Can potentially be very large. Free up before making more big sets
#    originalGeom = set()
#    for tag in groupChildren.keys():
#        originalGeom = originalGeom.union(groupChildren[tag])
#    
#    del groupChildren # Likewise. Free up memory
#    defaultMatGeom = allEntitiesTags.difference(originalGeom)
#    outTag = gmsh.model.addPhysicalGroup(2, list(defaultMatGeom))
#    gmsh.model.setPhysicalName(2, outTag, defaultMat)
