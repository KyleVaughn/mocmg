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

# TODO: Add all the methods for the base mesh class, but make them work with subset meshes


class GridMesh(Mesh):
    """Class to represent a grid mesh and mesh data.

    See :func:`mocmg.mesh.Mesh` for more information on inherited attributes.

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

        subset_meshes (list of mocmg.mesh.GridMesh): GridMesh objects that make up this GridMesh object.

        superset_mesh (mocmg.mesh.GridMesh): GridMesh objects that this mesh belongs to.

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

        subset_meshes (list of mocmg.mesh.GridMesh): GridMesh objects that make up this GridMesh object.

        superset_mesh (mocmg.mesh.GridMesh): GridMesh objects that this mesh belongs to.
    """

    def __init__(
        self,
        vertices=None,
        cells=None,
        cell_sets=None,
        name="",
        subset_meshes=None,
        superset_mesh=None,
    ):
        """See class docstring."""
        module_log.require(
            not (subset_meshes is not None and vertices is not None),
            "Grid mesh is initialized with subset meshes or topological data, not both.",
        )

        if subset_meshes:
            self.name = name
            self.subset_meshes = subset_meshes
            for sub_mesh in subset_meshes:
                module_log.require(
                    isinstance(sub_mesh, GridMesh),
                    "All meshes used to generate a GridMesh must also be a GridMesh.",
                )
                sub_mesh.superset_mesh = self
        else:
            super().__init__(vertices, cells, cell_sets, name)
