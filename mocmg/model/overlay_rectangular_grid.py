"""A function to combine grid generation and fragmentation for the whole model."""
import logging

import gmsh

from .group_preserving_fragment import group_preserving_fragment
from .rectangular_grid import rectangular_grid

module_log = logging.getLogger(__name__)


def overlay_rectangular_grid(bb, x=None, y=None, nx=None, ny=None, material="MATERIAL_WATER"):
    """Create a single or multilevel rectangular grid and overlay it on the model with a default material.

    View the :func:`mocmg.model.rectangular_grid` and :func:`mocmg.model.group_preserving_fragment`
    functions for more info.

    Args:
        bb (Iterable): The bounding box to be divided into rectangles, of the form:
            [x_min, y_min, z_min, x_max, y_max, z_max]

        x (list of Iterables): The x-coordinate locations to split the bounding box.

        y (list of Iterables): The y-coordinate locations to split the bounding box.

        nx (Iterable): The number of rectangles to split each entity into at each level.

        ny (Iterable): The number of rectangles to split each entity into at each level.

        material (str): A physical group of the form "MATERIAL_X" assigned to each grid
            entity. The string must contain "material", but is not case sensitive.

    Returns:
        list : A list of the resultant dim tags.
    """
    module_log.info("Overlaying rectangular grid")
    model_dim_tags = gmsh.model.getEntities(2)
    grid_tags = rectangular_grid(bb, x, y, nx, ny, material)
    grid_dim_tags = [(2, tag) for tag in grid_tags]
    gmsh.model.occ.synchronize()
    out_dim_tags = group_preserving_fragment(
        model_dim_tags + grid_dim_tags, model_dim_tags + grid_dim_tags, overwrite_material=material
    )

    return out_dim_tags
