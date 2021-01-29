"""The mesh class and related functions."""
import logging

module_log = logging.getLogger(__name__)

quadratic_edges = {
    "quad": False,
    "quad8": True,
    "triangle": False,
    "triangle6": True,
}


class Mesh:
    """Class to represent a mesh and mesh data.

    Attributes:
        vertices (dict): The ID and x,y,z location of vertices. A dictionary with integer keys
            and numpy array values, corresponding to point ID and spatial coordinates, respectively.

            - To store vertex 3 at x,y,z-coordinate (0.0, 1.0, 2.0):

                .. code:: python

                    vertices={3: np.array([0.0, 1.0, 2.0])}

        cells (dict): The individual cells that compose a mesh.
            A dictionaries, where each key/value has the form: "cell_type": dict,
            where the "cell_type" string can be
            "triangle", "quad8", etc. The dictionary value has integer keys and numpy array values.
            This dictionary denotes cell ID and the vertex ID that make up the cell.

            - For two triangles (ID 1 & 2) and a quadrilateral (ID 3), from vertices 1 through 6:

                .. code:: python

                    cells = {
                        "triangle": {
                            1: np.array([1, 2, 3]),
                            2: np.array([2, 3, 4]),
                        },
                        "quad": {
                            3: np.array([1, 2, 5, 6]),
                        },
                    }

        cell_sets (dict): The sets of cells that share the same attributes.
            A dictionary of the form: "set_name": ID np.array
            The ID array contains the integer IDs of all cells that share the attribute "set_name".

            - If cells 1, 2, and 3 are all in a fuel pin, but only 1 and 2 are uranium:

                .. code:: python

                    cell_sets = {
                        "Fuel Pin": np.array([1, 2, 3]),
                        "Material Uranium": np.array([1, 2]),
                    }

    """

    def __init__(self, vertices, cells, cell_sets=None):
        """See class docstring."""
        self.vertices = vertices
        self.cells = cells
        self.cell_sets = {} if cell_sets is None else cell_sets
