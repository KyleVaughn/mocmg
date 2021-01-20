"""A collection of functions to automate common tasks within gmsh."""
import logging

# from collections.abc import Iterable

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


# def rectangular_grid(bb, x=None, y=None, nx=None, ny=None):
#    """Fill me in."""
#    module_log.info("Generating rectangular grid")
#    x_min, y_min, z_min = bb[0:3]
#    x_max, y_max, z_max = bb[3:6]
#    dx = x_max - x_min
#    dy = y_max - y_min
#    dz = z_max - z_min
#    zz = z_min
#
#    # Error checking
#    # dx, dy, dz should all be positive
#    for d in [dx, dy, dz]:
#        module_log.require(d >= 0, "Invalid bounding box.")
#    # Number of args
#    arg_ctr = 0
#    arg_len = []
#    for arg in [x, y, nx, ny]:
#        if arg is not None:
#            arg_ctr = arg_ctr + 1
#            module_log.require(isinstance(arg, Iterable), "Arguments should be iterable.")
#            arg_len.append(len(arg))
#    module_log.require(
#        arg_ctr == 2,
#        "Incorrect number of arguments given. Provide one of (x or nx) and one of (ny or y).",
#    )
#    # Make sure that args are equal in levels.
#    # Should only be 2 args now after last check
#    module_log.require(
#        arg_len[0] == arg_len[1],
#        f"Length of arguments differ ({arg_len[0]} and {arg_len[1]})."
#        + " They should have the same number of levels.",
#    )
#    nlevels = arg_len[0]
#    # Model thickness for 2D
#    module_log.require(
#        abs(dz) <= 1e-6,
#        f"Bounding box thickness is greater than 1e-6 ({dz:.6f})."
#        + " Bounding box expected in 2D x-y plane.",
#    )
#    # If using nx, ny, ensure that the members are empty or int
#    if nx is not None:
#        module_log.require(
#            not nx or all(isinstance(i, int) for i in nx),
#            "nx must be empty or contain integer elements only.",
#        )
#    if ny is not None:
#        module_log.require(
#            not ny or all(isinstance(i, int) for i in ny),
#            "ny must be empty or contain integer elements only.",
#        )
#    # If x, y, ensure that elements are iterable
#    if x is not None:
#        module_log.require(
#            all(isinstance(i, Iterable) for i in x),
#            "x must have iterable elements.",
#        )
#    if y is not None:
#        module_log.require(
#            all(isinstance(i, Iterable) for i in y),
#            "y must have iterable elements.",
#        )
#
#    # Convert nx, ny notation to x, y format
#    # Include bb limits
#    if x is not None:
#        x[0] = list(x[0])
#        x[0] = sorted(set(x[0] + [x_min, x_max]))
#        for lvl in range(1, nlevels):
#            x[lvl] = sorted(set(x[lvl - 1] + x[lvl]))
#    if y is not None:
#        y[0] = list(y[0])
#        y[0] = sorted(set(y[0] + [y_min, y_max]))
#        for lvl in range(1, nlevels):
#            y[lvl] = sorted(set(y[lvl - 1] + y[lvl]))
#    if nx is not None:
#        # Get first level intervals
#        x = []
#        div = nx[0]
#        if div == 0:
#            div = 1
#        x.append(list(np.linspace(x_min, x_max, div + 1, endpoint=True)))
#        # If there is more than one level, divide intervals further
#        for lvl in range(1, nlevels):
#            x.append([])
#            for i in range(len(x[lvl - 1]) - 1):
#                x[lvl].append(
#                    np.linspace(x[lvl - 1][i], x[lvl - 1][i + 1], nx[lvl] + 1, endpoint=True)
#                )
#            # Get rid of duplicates
#            x[lvl] = sorted(set(np.append(x[lvl][0], x[lvl][1:])))
#    if ny is not None:
#        # Get first level intervals
#        y = []
#        div = ny[0]
#        if div == 0:
#            div = 1
#        y.append(list(np.linspace(y_min, y_max, div + 1, endpoint=True)))
#        # If there is more than one level, divide intervals further
#        for lvl in range(1, nlevels):
#            y.append([])
#            for i in range(len(y[lvl - 1]) - 1):
#                y[lvl].append(
#                    np.linspace(y[lvl - 1][i], y[lvl - 1][i + 1], ny[lvl] + 1, endpoint=True)
#                )
#            # Get rid of duplicates
#            y[lvl] = sorted(set(np.append(y[lvl][0], y[lvl][1:])))
#
#    # Create smallest rectangles
#    # Ensure elements are in the bb
#    module_log.require(
#        all(x_min <= xx and xx <= x_max for xx in x[-1]),
#        "Divisions must be within the bounding box.",
#    )
#    module_log.require(
#        all(y_min <= yy and yy <= y_max for yy in y[-1]),
#        "Divisions must be within the bounding box.",
#    )
#    grid_tags_coords = []
#    for y_ind, yy in enumerate(y[-1][:-1]):
#        for x_ind, xx in enumerate(x[-1][:-1]):
#            tag = gmsh.model.occ.addRectangle(
#                xx, yy, zz, x[-1][x_ind + 1] - xx, y[-1][y_ind + 1] - yy
#            )
#            grid_tags_coords.append([tag, xx, yy])
#    gmsh.model.occ.synchronize()

# Label the rectangles with the appropriate grid level and location
# level_#_(i,j) like so:
# y
# ^
# |------------
# |(1,2)|(2,2)|
# |-----|-----|
# |(1,1)|(2,1)|
# --------------> x


#    total_rect = (len(x[-1]) - 1) * (len(x[-1]) - 1)


#    max_grid_digits = len(str(total_rect))  # Digits on grid label
#    level_tags = []
#    for _i in range(nlevels):
#        level_tags.append([])
#    # Lowest level
#    for t in grid_tags:
#        level_tags[nlevels - 1].append(t)
#    # All other levels
#    print(level_tags)
