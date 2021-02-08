"""The mesh class and related functions."""
import logging

import numpy as np

module_log = logging.getLogger(__name__)

_has_quadratic_edges = {
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
            Dictionaries, where each key/value has the form: "cell_type": dict,
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

    def get_cells(self, cell_set_name):
        """Get the cell IDs for a given cell set name.

        Args:
            cell_set_name (str): Name of the cell set for which to retrieve cell IDs.

        Returns:
            cellIDs (numpy.array)
        """
        if cell_set_name in self.cell_sets:
            return self.cell_sets[cell_set_name]
        else:
            module_log.error(f"No cell set named '{cell_set_name}'.")

    def get_cell_area(self, cell):
        """Get the area of the cell with the given cell ID.

        Args:
            cell (int): The integer cell ID of the cell whose area will be calculated.

        Returns:
            area (float)
        """
        # Find the cell
        for cell_type in self.cells:
            if cell in self.cells[cell_type]:
                vertices = self.cells[cell_type][cell]
                # Has quadratic edges
                if _has_quadratic_edges[cell_type]:
                    # Get linear area and adjust for quadratic edges if it has them.
                    nvert = len(vertices)
                    module_log.require(nvert % 2 == 0, "Number of vertices in cell must be even.")
                    x_lin = np.array([self.vertices[v][0] for v in vertices[0 : int(nvert / 2)]])
                    y_lin = np.array([self.vertices[v][1] for v in vertices[0 : int(nvert / 2)]])
                    x_quad = np.array([self.vertices[v][0] for v in vertices[int(nvert / 2) :]])
                    y_quad = np.array([self.vertices[v][1] for v in vertices[int(nvert / 2) :]])

                    # Shoelace formula may be used for linear edges
                    # Assumes that vertices are in clockwise or counterclockwise order
                    x_ = x_lin - x_lin.mean()
                    y_ = y_lin - y_lin.mean()
                    correction = x_[-1] * y_[0] - y_[-1] * x_[0]
                    main_area = np.dot(x_[:-1], y_[1:]) - np.dot(y_[:-1], x_[1:])
                    area = 0.5 * np.abs(main_area + correction)

                    # Assumed points are in counterclockwise order. Area for the linear
                    # polygon is computed, then adjusted based on integrals for the quad edges.
                    # If a quadratic vertex is to the left of the linear edge, the area is added.
                    # Otherwise it is subtracted.
                    # Consider the following quadratic triangle with one quad edge:
                    #        2                   2
                    #       /  \                /| \
                    #      /    \              / |  \
                    #     5      4            5  |   \
                    #      \      \            \ |    \
                    #       \      \            \|     \
                    #        0---3--1            0------1
                    #     Quad edge (2,5,0)     Linear edges
                    # Since, point 5 is to the right of linear edge (2,0), the area of the polygon
                    # constructed by edges [(2,5,0), (0,2)] is added to the total area.
                    #
                    # For each edge, compute additional area using quadratic function
                    # Shift point to origin, rotate so line is x-axis, find quadratic function
                    # with 3 point fit, integrate, add or subtract based on right or left
                    for i in range(-1, int(nvert / 2) - 1):
                        x_e = np.array([x_lin[i], x_lin[i + 1], x_quad[i]])
                        y_e = np.array([y_lin[i], y_lin[i + 1], y_quad[i]])
                        # shift to origin
                        x_e = x_e - x_e[0]
                        y_e = y_e - y_e[0]
                        # rotate line to x-axis
                        if x_e[1] == 0.0:
                            if y_e[1] >= 0.0:
                                theta = np.pi / 2.0
                            else:
                                theta = -np.pi / 2.0
                        else:
                            theta = np.arctan(y_e[1] / x_e[1])

                        if x_e[1] < 0:
                            theta = theta + np.pi
                        rotation_matrix = np.array(
                            [
                                [np.cos(theta), np.sin(theta)],
                                [-np.sin(theta), np.cos(theta)],
                            ]
                        )
                        for j in range(1, 3):
                            v = np.array([[x_e[j]], [y_e[j]]])
                            v_ = np.dot(rotation_matrix, v)
                            x_e[j] = v_[0]
                            y_e[j] = v_[1]
                        # Get quadratic coefficients and integrate
                        # ax^2 + bx + c
                        p = np.poly1d(np.polyfit(x_e, y_e, 2))
                        p_int = np.polyint(p)
                        quadarea = p_int(x_e[1]) - p_int(0)
                        # quadarea will be opposite of correct sign
                        area = area - quadarea
                    return area

                # Does not have quadratic edges
                else:
                    # No quadratic edges shoelace formula may be used
                    # Assumes that vertices are in clockwise or counterclockwise order
                    x = np.array([self.vertices[v][0] for v in vertices])
                    y = np.array([self.vertices[v][1] for v in vertices])
                    x_ = x - x.mean()
                    y_ = y - y.mean()
                    correction = x_[-1] * y_[0] - y_[-1] * x_[0]
                    main_area = np.dot(x_[:-1], y_[1:]) - np.dot(y_[:-1], x_[1:])
                    area = 0.5 * np.abs(main_area + correction)
                return area
        module_log.error(f"Cell {cell} does not exist in this mesh")

    def get_set_area(self, cell_set_name):
        """Get the area of a cell set for a given cell set name.

        Args:
            cell_set_name (str): The name of the cell set.

        Returns:
            area (float)
        """
        module_log.info(f"Computing '{cell_set_name}' cell set area.")
        cells = self.get_cells(cell_set_name)
        area = 0.0
        for c in cells:
            area = area + self.get_cell_area(c)
        return area
