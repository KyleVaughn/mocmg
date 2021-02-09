"""A physical group preserving version of gmsh's fragment."""
import logging

import gmsh

module_log = logging.getLogger(__name__)


def group_preserving_fragment(object_dim_tags, tool_dim_tags):
    """Fragment CAD entities with gmsh, but preserve physical groups.

    Compute the boolean fragments (general fuse) of the entities in object_dim_tags and
    tool_dim_tags in the gmsh OpenCASCADE CAD representation.
    Return the resulting entities in out_dim_tags.

    .. warning::
        Remember to synchronize the model before using this function.

    Args:
        object_dim_tags (list): A list of the dim tags of entities to fragment.

        tool_dim_tags (list): A list of the dim tags of entities to fragment.

    Returns:
        list : A list of the resultant dim tags.
    """
    # Get all the physical groups
    old_physical_groups = {}
    groups = gmsh.model.getPhysicalGroups()
    names = [gmsh.model.getPhysicalName(*grp) for grp in groups]
    for i, name in enumerate(names):
        ents = gmsh.model.getEntitiesForPhysicalGroup(*groups[i])
        dim = groups[i][0]
        old_physical_groups[name] = [(dim, ent) for ent in ents]

    # Fragment
    module_log.info(f"Fragmenting {len(object_dim_tags + tool_dim_tags)} entities.")
    out_dim_tags, out_dim_tags_map = gmsh.model.occ.fragment(object_dim_tags, tool_dim_tags)

    # Create dictionary of new physical groups using the parent child relationship
    # between object_dim_tags + tool_dim_tags and out_dim_tags_map. The parent at index i
    # of object_dim_tags + tool_dim_tags has children out_dim_tags_map[i]
    new_physical_groups = {}
    input_dim_tags = object_dim_tags + tool_dim_tags
    # For each physical group
    for name in names:
        new_physical_groups[name] = []
        # For each of the dim tags in the physical group
        for dim_tag in old_physical_groups[name]:
            # If the dim tag was one of the entities in the fragment
            if dim_tag in input_dim_tags:
                # Get its children
                index = input_dim_tags.index(dim_tag)
                children = out_dim_tags_map[index]
                # Add the children to the new physical group
                for child in children:
                    if child not in new_physical_groups[name]:
                        new_physical_groups[name].append(child)
            else:
                # If it wasn't in the fragment, no changes necessary.
                new_physical_groups[name].append(dim_tag)

    # Synchronize and remove old groups
    module_log.info("Synchronizing model")
    gmsh.model.occ.synchronize()
    gmsh.model.removePhysicalGroups()

    # Create new physical groups
    for i, name in enumerate(names):
        gmsh.model.removePhysicalName(name)
        dim = groups[i][0]
        tags = [dimtag[1] for dimtag in new_physical_groups[name]]
        ptag = gmsh.model.addPhysicalGroup(dim, tags)
        gmsh.model.setPhysicalName(dim, ptag, name)

    return out_dim_tags
