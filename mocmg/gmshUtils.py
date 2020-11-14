import gmsh
import logging
import numpy as np
from scipy.optimize import fsolve


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
        module_log.info(f"Radius: {R[0]}, linear Disk area error: {total_area - np.pi*r*r}")
        gmsh.clear()
        return total_area - np.pi * r * r

    R = fsolve(f, r)
    return R[0]

def findLinearRingRadius(r_inner, ring_area, lc):
    # Finding the correct radius is quite hard, and does not match predicted results for
    # equal size elements, so an iterative solver is used
    # Call before mocmg.initialize, otherwise gmsh verbosity will be reset
    def f(r, R_inner, ring_area):
        disk1 = gmsh.model.occ.addDisk(0, 0, 0, R_inner, R_inner)
        disk2 = gmsh.model.occ.addDisk(0, 0, 0, r, r)
        ring = gmsh.model.occ.fragment([(2, disk2)], [(2, disk1)])
        tag = ring[0][1][1]
        gmsh.model.occ.synchronize()
        p = gmsh.model.addPhysicalGroup(2, [tag])
        gmsh.model.mesh.setSize(gmsh.model.getEntities(0), lc)
        gmsh.model.mesh.generate(2)
        gmsh.plugin.setNumber("MeshVolume", "Dimension", 2)
        gmsh.plugin.setNumber("MeshVolume", "PhysicalGroup", p)
        gmsh.plugin.run("MeshVolume")
        _, _, data = gmsh.view.getListData(0)
        total_area = data[0][-1]
        module_log.info(f"Radius: {r[0]}, linear ring area error: {total_area - ring_area}")
        gmsh.clear()
        return total_area - ring_area
    
    r_guess = np.sqrt(ring_area/np.pi + r_inner**2)
    R = fsolve(f, r_guess, args=(r_inner, ring_area))
    return R[0]
