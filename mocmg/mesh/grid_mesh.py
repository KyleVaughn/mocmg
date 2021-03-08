"""The grid mesh class and related functions."""
import logging

from .mesh import Mesh

module_log = logging.getLogger(__name__)

_has_quadratic_edges = {
    "quad": False,
    "quad8": True,
    "triangle": False,
    "triangle6": True,
}

# TODO: Add all the methods for the base mesh class, but make them work with children meshes


class GridMesh(Mesh):
    """Class to represent a grid mesh and mesh data.

    The grid mesh represents the grid levels used to represent a simulation domain.
    A GridMesh object is either a typical mesh containing, vertices, cells, and cell sets,
    representing the highest level of grid objects, or is a collection of the higher level
    grid objects that compose it.

    See :class:`mocmg.mesh.Mesh` for more information on inherited attributes.
    See :func:`mocmg.model.rectangular_grid` for more information on the grid hierarchy.

    Example:
        Suppose a simulation domain is a rectangle of width 2 and height 1 called Grid_L1_1_1.
        This total domain is divided into two parts in the x-direction, making two squares of
        side length 1, called Grid_L2_1_1 and Grid_L2_2_1. The GridMesh objects used to represent
        this domain would be two objects to represent Grid_L2_1_1 and Grid_L2_2_1. Each of these
        smallest objects will have its vertex, cell, and cell_set information. The Grid_L2_1_1
        object will not have any topological or cell set information, and will just contain
        a list of the meshes that make up its domain, namely Grid_L2_1_1 and Grid_L2_2_1.

    Parameters:
        vertices (dict): The ID and x,y,z location of vertices. A dictionary with integer keys
            and numpy array values, corresponding to point ID and spatial coordinates, respectively.

        cells (dict): The individual cells that compose a mesh.
            Dictionaries, where each key/value has the form: "cell_type": dict,
            where the "cell_type" string can be
            "triangle", "quad8", etc. The dictionary value has integer keys and numpy array values.
            This dictionary denotes cell ID and the vertex ID that make up the cell.

        cell_sets (dict): The sets of cells that share the same attributes.
            A dictionary of the form: "set_name": ID np.array
            The ID array contains the integer IDs of all cells that share the attribute "set_name".

        name (str): Name of the mesh.

        children (list of mocmg.mesh.GridMesh): GridMesh objects that make up this GridMesh object.

        parent (mocmg.mesh.GridMesh): GridMesh object that this mesh belongs to.

    Attributes:
        vertices (dict): The ID and x,y,z location of vertices. A dictionary with integer keys
            and numpy array values, corresponding to point ID and spatial coordinates, respectively.

        cells (dict): The individual cells that compose a mesh.
            Dictionaries, where each key/value has the form: "cell_type": dict,
            where the "cell_type" string can be
            "triangle", "quad8", etc. The dictionary value has integer keys and numpy array values.
            This dictionary denotes cell ID and the vertex ID that make up the cell.

        cell_sets (dict): The sets of cells that share the same attributes.
            A dictionary of the form: "set_name": ID np.array
            The ID array contains the integer IDs of all cells that share the attribute "set_name".

        name (str): Name of the mesh.

        children (list of mocmg.mesh.GridMesh): GridMesh objects that make up this GridMesh object.

        parent (mocmg.mesh.GridMesh): GridMesh object that this mesh belongs to.
    """

    def __init__(
        self,
        vertices=None,
        cells=None,
        cell_sets=None,
        name="",
        children=None,
    ):
        """See class docstring."""
        module_log.require(
            not (children is not None and vertices is not None),
            "Grid mesh is initialized with children meshes or topological data, not both.",
        )

        if children:
            self.name = name
            self.vertices = None
            self.cells = None
            self.cell_sets = None
            self.children = children
            for child in children:
                module_log.require(
                    isinstance(child, GridMesh),
                    "All meshes used to generate a GridMesh must also be a GridMesh.",
                )
                child.parent = self
        else:
            super().__init__(vertices, cells, cell_sets, name)
            self.children = None
