"""A collection of functions to automate common tasks within gmsh."""
import logging

import gmsh

module_log = logging.getLogger(__name__)


def get_entities_for_physical_group_name(name):
    """Fix me later."""
    groups = gmsh.model.getPhysicalGroups()
    names = [gmsh.model.getPhysicalName(*grp) for grp in groups]
    index = names.index(name)
    ents = gmsh.model.getEntitiesForPhysicalGroup(*groups[index])
    return ents
