import gmsh
import logging

module_log = logging.getLogger('mocmg.addDiskLattice')

# Add an n by n disk lattice of disk pitch p and disk diameter d
def addDiskLattice(n, p, d):
    module_log.info(f'Adding {n} by {n} disk lattice of pitch {p} and diameter {d}') 
    r = d/2.0
    x = 0 
    for i in range(n):
        y = 0 
        for j in range(n):
            tag = gmsh.model.occ.addDisk(x, y, 0, r, r)
            module_log.debug(f'Added disk of tag {tag} at ({x},{y},0)')
            y = y + p
        x = x + p
    module_log.info('Synchronizing model')
    gmsh.model.occ.synchronize()
    module_log.info('Model synchronized')
