import gmsh
import logging

module_log = logging.getLogger(__name__)

def getEntitiesForPhysicalGroupName(name):
    groups = gmsh.model.getPhysicalGroups()
    names = [gmsh.model.getPhysicalName(*g) for g in groups]
    i = names.index(name)
    return gmsh.model.getEntitiesForPhysicalGroup(*groups[i])
