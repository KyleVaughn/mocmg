"""A collection of functions to automate common tasks within gmsh."""
import logging

# import gmsh
# import numpy as np

module_log = logging.getLogger(__name__)

# def _assign_rectangular_grid_tags(nx, ny, grid_tags):
#    x_min, y_min = bb[0:2]
#    x_max, y_max = bb[3:5]
#    z = bb[2]
#    lvl = lvl + 1
#    if len(nx) > 1:
#    return 1


def rectangular_grid(bb, x=None, y=None, nx=None, ny=None):
    """Fill me in."""
    module_log.info("Generating rectangular grid")
    x_min, y_min, z_min = bb[0:3]
    x_max, y_max, z_max = bb[3:6]
    #    dx = x_max - x_min
    #    dy = y_max - y_min
    dz = z_max - z_min
    #    z = z_min

    # Error checking
    # Number of args
    arg_ctr = 0
    arg_len = []
    for arg in [x, y, nx, ny]:
        if arg is not None:
            arg_ctr = arg_ctr + 1
            module_log.require(isinstance(arg, list), "Arguments should be list type.")
            arg_len.append(len(arg))
    module_log.require(
        arg_ctr == 2,
        "Incorrect number of arguments given. Provide one of (x or nx) and one of (ny or y).",
    )
    # Make sure that args are equal in levels.
    # Should only be 2 args now after last check
    module_log.require(
        arg_len[0] == arg_len[1],
        f"Length of arguments differ ({arg_len[0]} and {arg_len[1]})."
        + " They should have the same number of levels.",
    )
    # Model thickness for 2D
    module_log.require(
        abs(dz) <= 1e-6,
        f"Bounding box thickness is greater than 1e-6 ({dz:.6f})."
        + " Bounding box expected in 2D x-y plane.",
    )
    # If using nx, ny, ensure that the members are empty or int
    if nx is not None:
        module_log.require(
            not nx or all(isinstance(i, int) for i in nx),
            "nx must be empty or contain integer elements only",
        )

    if ny is not None:
        module_log.require(
            not ny or all(isinstance(i, int) for i in ny),
            "ny must be empty or contain integer elements only",
        )

    # Compute a few necessary quantities


#    max_grid_digits = len(str(np.prod(nx))) # Digits on grid label
#    width = dx/np.prod(nx)
#    height = dy/np.prod(ny)

#    # Create the smallest level of rectangles
#    grid_tags = []
#    y = y_min
#    for j in range(np.prod(ny)):
#        x = x_min
#        for i in range(np.prod(nx)):
#            tag = gmsh.model.occ.addRectangle(x, y, z, width, height)
#            print(tag)
#            x = x + width
#        y = y + height
#
#    gmsh.model.occ.synchronize()


#    objects = _make_rectangular_grid_level(bb, nx, ny, 0)
