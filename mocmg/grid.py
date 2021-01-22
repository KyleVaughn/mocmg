"""A collection of grid generation functions to automate grid generation within gmsh."""
import logging
from collections.abc import Iterable

import gmsh
import numpy as np

module_log = logging.getLogger(__name__)


def rectangular_grid(bb, x=None, y=None, nx=None, ny=None):
    """Fill me in."""
    module_log.info("Generating rectangular grid")
    x_min, y_min, z_min = bb[0:3]
    x_max, y_max, z_max = bb[3:6]
    dx = x_max - x_min
    dy = y_max - y_min
    dz = z_max - z_min
    zz = z_min

    # Error checking
    # dx, dy, dz should all be positive
    for d in [dx, dy, dz]:
        module_log.require(d >= 0, "Invalid bounding box.")
    # Number of args
    arg_ctr = 0
    arg_len = []
    for arg in [x, y, nx, ny]:
        if arg is not None:
            arg_ctr = arg_ctr + 1
            module_log.require(isinstance(arg, Iterable), "Arguments should be iterable.")
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
    nlevels = arg_len[0]
    # Model thickness for 2D
    module_log.require(
        abs(dz) <= 1e-6,
        f"Bounding box thickness is greater than 1e-6 ({dz:.6f})."
        + " Bounding box expected in 2D x-y plane.",
    )
    # If using nx, ny, ensure that the members are empty or int
    if nx is not None:
        module_log.require(
            all(isinstance(i, int) for i in nx) and all(xx > 0 for xx in nx),
            "nx must contain positive integer elements only.",
        )
    if ny is not None:
        module_log.require(
            all(isinstance(i, int) for i in ny) and all(yy > 0 for yy in ny),
            "ny must contain positive integer elements only.",
        )
    # If x, y, ensure that elements are iterable
    if x is not None:
        module_log.require(
            all(isinstance(i, Iterable) for i in x),
            "x must have iterable elements.",
        )
    if y is not None:
        module_log.require(
            all(isinstance(i, Iterable) for i in y),
            "y must have iterable elements.",
        )

    # Convert nx, ny notation to x, y format
    # Include bb limits
    if x is not None:
        x[0] = list(x[0])
        x[0] = sorted(set(x[0] + [x_min, x_max]))
        for lvl in range(1, nlevels):
            x[lvl] = sorted(set(x[lvl - 1] + x[lvl]))
    if y is not None:
        y[0] = list(y[0])
        y[0] = sorted(set(y[0] + [y_min, y_max]))
        for lvl in range(1, nlevels):
            y[lvl] = sorted(set(y[lvl - 1] + y[lvl]))
    if nx is not None:
        # Get first level intervals
        x = []
        div = nx[0]
        x.append(list(np.linspace(x_min, x_max, div + 1, endpoint=True)))
        # If there is more than one level, divide intervals further
        for lvl in range(1, nlevels):
            x.append([])
            for i in range(len(x[lvl - 1]) - 1):
                x[lvl].append(
                    np.linspace(x[lvl - 1][i], x[lvl - 1][i + 1], nx[lvl] + 1, endpoint=True)
                )
            # Get rid of duplicates
            x[lvl] = sorted(set(np.append(x[lvl][0], x[lvl][1:])))
    if ny is not None:
        # Get first level intervals
        y = []
        div = ny[0]
        y.append(list(np.linspace(y_min, y_max, div + 1, endpoint=True)))
        # If there is more than one level, divide intervals further
        for lvl in range(1, nlevels):
            y.append([])
            for i in range(len(y[lvl - 1]) - 1):
                y[lvl].append(
                    np.linspace(y[lvl - 1][i], y[lvl - 1][i + 1], ny[lvl] + 1, endpoint=True)
                )
            # Get rid of duplicates
            y[lvl] = sorted(set(np.append(y[lvl][0], y[lvl][1:])))

    # Create smallest rectangles
    # Ensure elements are in the bb
    module_log.require(
        all(x_min <= xx and xx <= x_max for xx in x[-1]),
        "Divisions must be within the bounding box.",
    )
    module_log.require(
        all(y_min <= yy and yy <= y_max for yy in y[-1]),
        "Divisions must be within the bounding box.",
    )
    grid_tags_coords = []
    for y_ind, yy in enumerate(y[-1][:-1]):
        for x_ind, xx in enumerate(x[-1][:-1]):
            tag = gmsh.model.occ.addRectangle(
                xx, yy, zz, x[-1][x_ind + 1] - xx, y[-1][y_ind + 1] - yy
            )
            grid_tags_coords.append([tag, xx, yy])
    gmsh.model.occ.synchronize()

    # Label the rectangles with the appropriate grid level and location
    # level_#_(i,j) like so:
    # y
    # ^
    # |------------
    # |(1,2)|(2,2)|
    # |-----|-----|
    # |(1,1)|(2,1)|
    # --------------> x
    grid_tags_levels = []
    max_grid_digits = max(len(str(len(x[-1]))), len(str(len(y[-1]))))
    for lvl in range(nlevels):
        grid_str = f"Grid_L{lvl+1}_"
        grid_tags_levels.append({})
        for j in range(len(y[lvl]) - 1):
            jstr = str(j + 1).zfill(max_grid_digits)
            for i in range(len(x[lvl]) - 1):
                istr = str(i + 1).zfill(max_grid_digits)
                name = grid_str + istr + "_" + jstr
                grid_tags_levels[lvl][name] = []
    for (tag, x0, y0) in grid_tags_coords:
        for lvl in range(nlevels):
            i = np.searchsorted(x[lvl], x0, side="right")
            j = np.searchsorted(y[lvl], y0, side="right")
            grid_str = f"Grid_L{lvl+1}_"
            istr = str(i).zfill(max_grid_digits)
            jstr = str(j).zfill(max_grid_digits)
            name = grid_str + istr + "_" + jstr
            grid_tags_levels[lvl][name].append(tag)

    # Set physical groups. This can be slow.
    module_log.debug("Setting grid tags")
    for lvl in range(nlevels):
        phys_grp_tags = []
        phys_grp_names = list(grid_tags_levels[lvl].keys())
        for name in phys_grp_names:
            output_tag = gmsh.model.addPhysicalGroup(2, grid_tags_levels[lvl][name])
            phys_grp_tags.append(output_tag)
            gmsh.model.setPhysicalName(2, output_tag, name)

    return [tupl[0] for tupl in grid_tags_coords]
