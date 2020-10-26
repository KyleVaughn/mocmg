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
    def f(R):
        gmsh.model.occ.addDisk(0, 0, 0, R, R)
        gmsh.model.occ.synchronize()
        p = gmsh.model.addPhysicalGroup(2, [1])
        gmsh.model.setPhysicalName(2, p, 'Disk')
        gmsh.model.occ.synchronize
        gmsh.model.mesh.setSize(gmsh.model.getEntities(0), lc)
        gmsh.model.mesh.generate(2)
        gmsh.write("linDisk.inp")
        mesh = readAbaqusINP('linDisk.inp')
        total_area = mesh.getSetArea('DISK')
        module_log.info(f'Linear Disk area error: {total_area - pi*r*r}')
        gmsh.model.remove()
        return total_area - pi*r*r
    R = fsolve(f, r)
    return R[0]
