"""A collection of functions to automate common tasks within gmsh."""
import logging

import gmsh

module_log = logging.getLogger(__name__)


def get_entities_for_physical_group_name(name):
    """Get the integer IDs of the entities in the physical group.

    Args:
        name (str): The name of the physical group.

    Returns:
        List of integer IDs of the entities in the physical group.

    """
    groups = gmsh.model.getPhysicalGroups()
    names = [gmsh.model.getPhysicalName(*grp) for grp in groups]
    module_log.require(name in names, f"No physical group of name '{name}'.")
    index = names.index(name)
    ents = gmsh.model.getEntitiesForPhysicalGroup(*groups[index])
    return ents
