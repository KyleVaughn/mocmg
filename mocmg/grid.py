"""A collection of grid generation functions to automate grid generation within gmsh."""
import logging
from collections.abc import Iterable

import gmsh
import numpy as np

module_log = logging.getLogger(__name__)


def _input_check_rectangular_grid(bb, x, y, nx, ny):
    """Check the rectangular grid input for correct format/common errors."""
    x_min, y_min, z_min = bb[0:3]
    x_max, y_max, z_max = bb[3:6]
    dx = x_max - x_min
    dy = y_max - y_min
    dz = z_max - z_min
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

    return nlevels


def _nxy_to_xy_rectangular_grid(nlevels, bb, x, y, nx, ny):
    """Convert the nx, ny arguments to the x, y format."""
    x_min, y_min, z_min = bb[0:3]
    x_max, y_max, z_max = bb[3:6]
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

    return x, y, nx, ny


def _create_model_rectangular_grid(bb, x, y):
    """Generate the rectangles in gmsh."""
    x_min, y_min, z_min = bb[0:3]
    x_max, y_max, z_max = bb[3:6]
    zz = z_min
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

    return grid_tags_coords


def _label_rectangular_grid(nlevels, grid_tags_coords, x, y):
    """Label the rectangles with the appropriate grid level and location."""
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

    return grid_tags_coords


def rectangular_grid(bb, x=None, y=None, nx=None, ny=None):
    """Create a single or multilevel rectangular grid.

    You must provide one of x or nx, and one of y or ny. The following are valid combinations:

    - x and y
    - nx and ny
    - x and ny
    - nx and y

    The grid will generate rectangles with tags labeled first in increasing x, then
    increasing y, as seen below.

    .. figure:: ../_figures/rectangular_grid.png
        :scale: 70 %

    The highest level (smallest) rectangles are grouped into lower levels and labeled using
    gmsh physical groups of the form "Grid_LN_i_j", where:

    - N is the grid level,
    - i is the x-index of the group,
    - and j is the y-index of the group.

    Assuming the figure above was generated with nx=[2,2], ny=[2,2], the original
    bounding box will be split in two in x and y for the first level. The resulting
    4 entities will then be split in two in x and y again for the second level,
    producing 16 total entities. A part of the labeled grid can be seen below.

    .. figure:: ../_figures/rectangular_grid_labeled.png
        :scale: 60 %

    Args:
        bb (Iterable): The bounding box to be divided into rectangles, of the form:
            [x_min, y_min, z_min, x_max, y_max, z_max]

        x (list of Iterables): The x-coordinate locations to split the bounding box.

            -   Example: To divide the unit square (bb=[0, 0, 0, 1, 1, 0]) into a two level grid,
                dividing each element in half in the x-direction: x=[[0.5], [0.25, 0.75]].
                Note that x may or may not include the divisions from higher levels, as
                well as the bounding box sides. This x is equivalent to the previous:
                x=[[0.5],[0.0, 0.25, 0.5, 0.75, 1.0]].

        y (list of Iterables): The y-coordinate locations to split the bounding box.

        nx (Iterable): The number of rectangles to split each entity into at each level.

            -   Example: nx = [1, 2, 3] will not split the bounding box in x on the first level (L1).
                All L1 entities are then passed to L2, in this case just the bounding box.
                The bounding box is then split into 2 equal halves. The halves are then passed
                to L3, where each half is equally divided into thirds, for 6 total, uniform
                rectangles.

        ny (Iterable): The number of rectangles to split each entity into at each level.

    Returns:
        A list of tags of the rectangles that make up the grid.
    """
    module_log.info("Generating rectangular grid")
    x_min, y_min, z_min = bb[0:3]
    x_max, y_max, z_max = bb[3:6]

    nlevels = _input_check_rectangular_grid(bb, x, y, nx, ny)
    x, y, nx, ny = _nxy_to_xy_rectangular_grid(nlevels, bb, x, y, nx, ny)

    # Include bb limits
    x[0] = list(x[0])
    x[0] = sorted(set(x[0] + [x_min, x_max]))
    for lvl in range(1, nlevels):
        x[lvl] = sorted(set(x[lvl - 1] + x[lvl]))
    y[0] = list(y[0])
    y[0] = sorted(set(y[0] + [y_min, y_max]))
    for lvl in range(1, nlevels):
        y[lvl] = sorted(set(y[lvl - 1] + y[lvl]))

    grid_tags_coords = _create_model_rectangular_grid(bb, x, y)
    _label_rectangular_grid(nlevels, grid_tags_coords, x, y)

    return [tupl[0] for tupl in grid_tags_coords]
