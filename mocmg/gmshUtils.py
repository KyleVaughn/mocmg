import gmsh
import logging
from .abaqusIO import readAbaqusINP
from .mesh import Mesh
from scipy.optimize import fsolve

pi = 3.141592653589793

module_log = logging.getLogger(__name__)


def getEntitiesForPhysicalGroupName(name):
    groups = gmsh.model.getPhysicalGroups()
    names = [gmsh.model.getPhysicalName(*g) for g in groups]
    i = names.index(name)
    ents = gmsh.model.getEntitiesForPhysicalGroup(*groups[i])
    return ents


def findLinearDiskRadius(r, lc):
    # Finding the correct radius is quite hard, and does not match predicted results for
    # equal size elements, so an iterative solver is used
    # Call before mocmg.initialize, otherwise gmsh verbosity will be reset
    def f(R):
        s = gmsh.model.occ.addDisk(0, 0, 0, R, R)
        gmsh.model.occ.synchronize()
        p = gmsh.model.addPhysicalGroup(2, [s])
        gmsh.model.mesh.setSize(gmsh.model.getEntities(0), lc)
        gmsh.model.mesh.generate(2)
        gmsh.plugin.setNumber("MeshVolume", "Dimension", 2)
        gmsh.plugin.setNumber("MeshVolume", "PhysicalGroup", p)
        gmsh.plugin.run("MeshVolume")
        _, _, data = gmsh.view.getListData(0)
        total_area = data[0][-1]
        module_log.info(f"Linear Disk area error: {total_area - pi*r*r}")
        gmsh.clear()
        return total_area - pi * r * r

    R = fsolve(f, r)
    return R[0]
