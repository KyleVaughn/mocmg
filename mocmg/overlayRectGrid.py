import gmsh
import logging
from .generateRectGrid import generateRectGrid

module_log = logging.getLogger(__name__)

# NOTE: Remember to synchronize the model before using this function
# It is assumed that the model already has material assigned


def overlayRectGrid(nx, ny, nnx=1, nny=1, defaultMat="Material Void", bb=None):
    module_log.info("Overlaying rectangular grid")

    # 1. Get all 2D model entities
    modelDimTags = gmsh.model.getEntities(2)
    module_log.debug(f"2D entity dim tags: {modelDimTags}")

    # 2. Get bounding box
    if bb is None:
        bb = gmsh.model.getBoundingBox(-1, -1)
        module_log.debug(f"Model bounding box: {bb}")
    else:
        module_log.warning(
            "Bounding box for rectangular grid manually specified."
            + f" Use caution. Box: {bb}"
        )

    # 3. Generate rectangular grid
    pGroupTagsL1, pGroupTagsL2, pGroupNamesL1, pGroupNamesL2 = generateRectGrid(
        bb, nx, ny, nnx, nny
    )

    # 4. Fragment the grid components with the original model components
    # Generate a list of all elementary entities in the grid
    gridElemTags = set()
    for ptag in pGroupTagsL2:
        elemTags = gmsh.model.getEntitiesForPhysicalGroup(2, ptag)
        gridElemTags = gridElemTags.union(set(elemTags))

    gridElemTags = list(gridElemTags)
    gridElemDimTags = [(2, tag) for tag in gridElemTags]
    module_log.info(
        f"Fragmenting {len(modelDimTags)} entities"
        + f" with {len(gridElemDimTags)} entities"
    )
    # fragment outputs the NEW entities and the parent-child relationships for ALL input entities
    fragmentTags, fragmentChildren = gmsh.model.occ.fragment(
        modelDimTags, gridElemDimTags
    )
    #
    #
    # NOTE
    # At this point, the occ fragment model entities exist and
    #    the original geometric entities do not.
    # Except for visualization purposes.
    # However, since the model has not been synchronized, the physical group information about the
    # original geometric entities still exists and can be used. If the model is synchronized this
    # information will be destroyed.
    #
    #

    # 5. Assign old physical groups to new entities
    # Get  physical group tags and physical group names from original entites.
    # Associate them with children.
    fragmentChildrenGroups = {}
    fragmentChildrenGroupNames = {}
    for i, e in enumerate(modelDimTags + gridElemDimTags):
        children = fragmentChildren[i]  # dim tags of child entities
        module_log.debug(f"Entity {e} had children {children}")
        childTags = [t[1] for t in children]  # tags of child entities
        pGroupTags = list(
            gmsh.model.getPhysicalGroupsForEntity(*e)
        )  # physical group tags
        if len(pGroupTags) > 0:
            module_log.debug(f"Entity {e} had {len(pGroupTags)} physical groups")
            for tag in pGroupTags:
                # If group is already known, just add children to set
                # otherwise, add it and its name to dictionaries.
                if tag in fragmentChildrenGroupNames:
                    # Union the current set and the child tags
                    fragmentChildrenGroups[tag] = fragmentChildrenGroups[tag].union(
                        set(childTags)
                    )
                else:
                    # Add the key and children to the dict
                    fragmentChildrenGroupNames[tag] = gmsh.model.getPhysicalName(2, tag)
                    fragmentChildrenGroups[tag] = set(childTags)
        else:
            module_log.debug(f"Entity {e} had no physical groups")
        # Report group names and children
        module_log.debug(
            f"Group tag/name dictionary is now : {fragmentChildrenGroupNames}"
        )
        module_log.debug(f"Group tag/child dictionary is now: {fragmentChildrenGroups}")

    # Synchronize and remove old groups
    module_log.info("Synchronizing model")
    gmsh.model.removePhysicalGroups()
    gmsh.model.occ.synchronize()

    # For each group, create a new group with the appropriate children and name
    module_log.info("Adjusting tags to new entities")
    for tag in fragmentChildrenGroups.keys():
        outTag = gmsh.model.addPhysicalGroup(2, list(fragmentChildrenGroups[tag]), tag)
        if outTag != tag:  # pragma no cover
            module_log.warning(
                f"Physical group {tag} could not be assigned to"
                + " children with original tag."
                + " This could indicate an uncaught error prior to the execution"
                + " of this code."
            )
        gmsh.model.setPhysicalName(2, outTag, fragmentChildrenGroupNames[tag])

    # 6. Assign a default material to any entity that didn't inherit a material from parent.
    # This should just be {bounding box}\{original geometry}
    allEntities = gmsh.model.getEntities(2)
    allEntitiesTags = set([t[1] for t in allEntities])
    del allEntities  # Can potentially be very large. Free up before making more big sets
    originalGeom = set()
    for i, e in enumerate(modelDimTags):
        children = fragmentChildren[i]
        childTags = [t[1] for t in children]
        originalGeom = originalGeom.union(childTags)

    defaultMatGeom = allEntitiesTags.difference(originalGeom)
    outTag = gmsh.model.addPhysicalGroup(2, list(defaultMatGeom))
    gmsh.model.setPhysicalName(2, outTag, defaultMat)
