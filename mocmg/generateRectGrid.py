import gmsh
import logging
from collections import defaultdict

module_log = logging.getLogger(__name__)

# Generate an axis-aligned two-level rectangular grid. 
# The bounding box domain is subdivided into nx pieces in the x-direction and ny pieces in the y-direction.
# These rectangular elements compose grid level 1. Each grid level 1 rectangle is then further divided into
# nnx pieces in the x-direction and nny pieces in the y-direction.
#
# Inputs:
#   bb: Bounding box which the grid will conform to. A list of the form [x_min, y_min, z_min, x_max, y_max, z_max]
#   nx: Integer number of divisions of the bounding box in the x-direction
#   ny: Integer number of divisions of the bounding box in the y-direction
#   nnx: Integer number of divisions of the grid level 1 rectangles in the x-direction
#   nny: Integer number of divisions of the grid level 1 rectangles in the y-direction
# Outputs:
#   physicalGroupTagsL1: A list of integer tags of the physical groups in grid level 1
#   physicalGroupTagsL2: A list of integer tags of the physical groups in grid level 2
#   physicalGroupNamesL1: A list of names of the physical groups for grid level 1 of the form "Grid L1 (i,j)"
#   physicalGroupNamesL2: A list of names of the physical groups for grid level 2 of the form "Grid L2 (i,j)"
#
#   NOTE: gmsh.model.getPhysicalName(2, physicalGroupTagsL1[i]) = physicalGroupNamesL1[i]
#   This holds for L2 as well
def generateRectGrid(bb,nx,ny,nnx=1,nny=1):
    x_min, y_min, z_min = bb[0:3]
    x_max, y_max, z_max = bb[3:6]
    dx = x_max - x_min
    dy = y_max - y_min
    dz = z_max - z_min
    if abs(dz > 1e-6):
        module_log.warning(f'Model thickness is {dz:.6f} > 1e-6. Model expected in 2D x-y plane.')

    width1 = dx/float(nx) # width of rectangle in grid level 1
    height1 = dy/float(ny) # height of rectangle in grid level 1
    width2 = width1/float(nnx) # width of rectangle in grid level 2
    height2 = height1/float(nny) # height of rectangle in grid level 2
    z = bb[5] # z location of the model. Assumed all entities have same z

    # Generate rectangles to fill bounding box.
    # Generate only grid level 2 rectangles and group them based upon location to fit inside grid level 1 rectangles
    gridTags = [] # Tags of all grid level 2 rectangles
    gridTagsLevel1 = {} # Dictionary of grid level 1 names and tags of grid level 2 rectangles for each name 
    gridTagsLevel2 = {} # Dictionary of grid level 2 names and tags of grid level 2 rectangles for each name 
    x = x_min
    for i in range(nx):
        y = y_min
        for j in range(ny):
            xx = x
            # Generate grid level 2 entities for this grid level 1 entitity
            name1 = f'Grid L1 ({i+1},{j+1})'
            module_log.debug(f'Generating {name1} of width {width1:.2f}' + \
                   f' and height {height1:.2f} at ({x:.2f},{y:.2f},{z:.2f})')
            gridTagsLevel1[name1] = []
            for ii in range(nnx):
                yy = y
                for jj in range(nny):
                    name2 = f'Grid L2 ({i*nx+ii+1}, {j*ny+jj+1})'
                    tag = gmsh.model.occ.addRectangle(xx,yy,z, width2, height2)
                    gridTags.append(tag)
                    gridTagsLevel1[name1].append(tag)
                    gridTagsLevel1[name2] = [tag]
                    module_log.debug(f'Added grid L2 rectangle of width {width2:.2f}' + \
                           f' and height {height2:.2f} at ({xx:.2f},{yy:.2f},{z:.2f})')
                    yy = yy + height2
                xx = xx + width2
            y = y + height1
        x = x + width1
    

    # Model must be synchronized for entities to be able to have a physical group
    gmsh.model.occ.synchronize()

    # Set physical groups
    physicalGroupTagsL1 = []
    physicalGroupNamesL1 = gridTagsLevel1.keys()
    for name in physicalGroupNamesL1:
        outTag = gmsh.model.addPhysicalGroup(2, gridTagsLevel1[name])
        physicalGroupTagsL1.append(outTag)
        gmsh.model.setPhysicalName(2, outTag, name)

    physicalGroupTagsL2 = []
    physicalGroupNamesL2 = gridTagsLevel2.keys()
    for name in physicalGroupNamesL2:
        outTag = gmsh.model.addPhysicalGroup(2, gridTagsLevel2[name])
        physicalGroupTagsL2.append(outTag)
        gmsh.model.setPhysicalName(2, outTag, name)

    return physicalGroupTagsL1, physicalGroupTagsL2, physicalGroupNamesL1, physicalGroupNamesL2