"""Generate a 2D axis-aligned, two-level rectangular grid within gmsh."""
import logging

import gmsh

module_log = logging.getLogger(__name__)


# Generate an axis-aligned two-level rectangular grid.
# The bounding box domain is subdivided into nx pieces in the x-direction and ny pieces in the
# y-direction.
# These rectangular elements compose grid level 1. Each grid level 1 rectangle is then further
# divided into nnx pieces in the x-direction and nny pieces in the y-direction.
#
# Inputs:
#   bb: Bounding box which the grid will conform to.
#       A list of the form [x_min, y_min, z_min, x_max, y_max, z_max]
#   nx: Integer number of divisions of the bounding box in the x-direction
#   ny: Integer number of divisions of the bounding box in the y-direction
#   nnx: Integer number of divisions of the grid level 1 rectangles in the x-direction
#   nny: Integer number of divisions of the grid level 1 rectangles in the y-direction
# Outputs:
#   phys_grp_tags_lvl_1: A list of integer tags of the physical groups in grid level 1
#   phys_grp_tags_lvl_2: A list of integer tags of the physical groups in grid level 2
#   phys_grp_names_lvl_1: A list of names of the physical groups for grid level 1
#                         of the form "Grid L1 (i,j)"
#   phys_grp_names_lvl_2: A list of names of the physical groups for grid level 2
#                         of the form "Grid L2 (i,j)"
#
#   NOTE: gmsh.model.getPhysicalName(2, phys_grp_tags_lvl_1[i]) == phys_grp_names_lvl_1[i]
#   This holds for L2 as well
def rectangular_grid(bb, nx, ny, nnx=1, nny=1):
    """Generate a 2D axis-aligned, two-level rectangular grid using gmsh.

    The bounding box domain is subdivided into nx pieces in the x-direction and ny pieces in the
    y-direction.
    These rectangular elements compose grid level 1 and are given physical group names of the form
    "Grid_L1_i_j", where i and j are the indices of the rectangle in the x and y-directions
    respectively. i is in the set [1, nx]. j is is the set [1, ny].
    The rectangle at (bb[0], bb[1]) will have index (1, 1)

    Each grid level 1 rectangle is then further
    divided into nnx pieces in the x-direction and nny pieces in the y-direction.
    These rectangles have the additional physical group of "Grid_L2_ii_jj".
    Similar to the grid level 1,
    The rectangle at (bb[0], bb[1]) will have index (1, 1).
    This grid has a global index, so i is in the set [1, nx*nnx] and j is in the set [1, ny*nny].

    Args:
        bb (Iterable(float)): Bounding box which the grid will conform to.
            An iterable of the form [x_min, y_min, z_min, x_max, y_max, z_max]
        nx: Integer number of divisions of the bounding box in the x-direction
        ny: Integer number of divisions of the bounding box in the y-direction
        nnx: Integer number of divisions of the grid level 1 rectangles in the x-direction
        nny: Integer number of divisions of the grid level 1 rectangles in the y-direction

    Returns:
        phys_grp_tags_lvl_1: A list of integer tags of the physical groups in grid level 1
        phys_grp_tags_lvl_2: A list of integer tags of the physical groups in grid level 2
        phys_grp_names_lvl_1: A list of names of the physical groups for grid level 1
        of the form 'Grid L1 (i,j)'.
        phys_grp_names_lvl_2: A list of names of the physical groups for grid level 2
        of the form 'Grid L2 (i,j)'.

    NOTE:
        gmsh.model.getPhysicalName(2, phys_grp_tags_lvl_1[i]) == phys_grp_names_lvl_1[i]
        This holds for L2 as well
    """
    module_log.info("Generating rectangular grid")
    x_min, y_min, z_min = bb[0:3]
    x_max, y_max, z_max = bb[3:6]
    dx = x_max - x_min
    dy = y_max - y_min
    dz = z_max - z_min
    if abs(dz > 1e-6):
        module_log.warning(f"Model thickness is {dz:.6f} > 1e-6. Model expected in 2D x-y plane.")

    width1 = dx / float(nx)  # width of rectangle in grid level 1
    height1 = dy / float(ny)  # height of rectangle in grid level 1
    width2 = width1 / float(nnx)  # width of rectangle in grid level 2
    height2 = height1 / float(nny)  # height of rectangle in grid level 2
    z = bb[2]  # z location of the model. Assumed all entities have same z

    # Generate rectangles to fill bounding box.
    # Generate only grid level 2 rectangles and group them based upon location to fit
    # inside grid level 1 rectangles
    grid_tags = []  # Tags of all grid level 2 rectangles
    grid_tags_lvl_1 = {}  # Dict of grid lvl 1 names and tags of grid lvl 2 rectangles for each name
    grid_tags_lvl_2 = {}  # Dict of grid lvl 2 names and tags of grid lvl 2 rectangles for each name
    x = x_min
    # Check to make sure divisions is 3 digits or less, otherwise grid naming changes
    if nx * nnx > 999:
        module_log.error("Too many x-divisions of bounding box for the output format")
        raise ValueError("Too many x-divisions of bounding box for the output format")
    if ny * nny > 999:
        module_log.error("Too many y-divisions of bounding box for the output format")
        raise ValueError("Too many y-divisions of bounding box for the output format")
    for i in range(nx):
        y = y_min
        for j in range(ny):
            xx = x
            # Generate grid level 2 entities for this grid level 1 entitity
            name1 = f"GRID_L1_{i+1:03}_{j+1:03}"
            module_log.debug(
                f"Generating {name1} of width {width1:.2f}"
                + f" and height {height1:.2f} at ({x:.2f},{y:.2f},{z:.2f})"
            )
            grid_tags_lvl_1[name1] = []
            for ii in range(nnx):
                yy = y
                for jj in range(nny):
                    name2 = f"GRID_L2_{i*nnx+ii+1:03}_{j*nny+jj+1:03}"
                    tag = gmsh.model.occ.addRectangle(xx, yy, z, width2, height2)
                    grid_tags.append(tag)
                    grid_tags_lvl_1[name1].append(tag)
                    grid_tags_lvl_2[name2] = [tag]
                    module_log.debug(
                        f"Added grid L2 rectangle of tag {tag}, width {width2:.2f},"
                        + f" and height {height2:.2f} at ({xx:.2f},{yy:.2f},{z:.2f})"
                    )
                    yy = yy + height2
                xx = xx + width2
            y = y + height1
        x = x + width1

    # Model must be synchronized for entities to be able to have a physical group
    module_log.info("Synchronizing model")
    gmsh.model.occ.synchronize()

    # Set physical groups. This can be slow.
    module_log.info("Setting grid tags")
    phys_grp_tags_lvl_1 = []
    phys_grp_names_lvl_1 = list(grid_tags_lvl_1.keys())
    for name in phys_grp_names_lvl_1:
        output_tag = gmsh.model.addPhysicalGroup(2, grid_tags_lvl_1[name])
        phys_grp_tags_lvl_1.append(output_tag)
        gmsh.model.setPhysicalName(2, output_tag, name)

    phys_grp_tags_lvl_2 = []
    phys_grp_names_lvl_2 = list(grid_tags_lvl_2.keys())
    for name in phys_grp_names_lvl_2:
        output_tag = gmsh.model.addPhysicalGroup(2, grid_tags_lvl_2[name])
        phys_grp_tags_lvl_2.append(output_tag)
        gmsh.model.setPhysicalName(2, output_tag, name)

    # NOTE: physical surface tags are NOT elementary entity tags
    return (
        phys_grp_tags_lvl_1,
        phys_grp_tags_lvl_2,
        phys_grp_names_lvl_1,
        phys_grp_names_lvl_2,
    )
