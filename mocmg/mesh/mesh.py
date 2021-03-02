"""The mesh class and related functions."""
import copy
import logging

import numpy as np
from anytree import Node  # , RenderTree

module_log = logging.getLogger(__name__)

_has_quadratic_edges = {
    "quad": False,
    "quad8": True,
    "triangle": False,
    "triangle6": True,
}


class Mesh:
    """Class to represent a mesh and mesh data.

    Parameters:
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

        name (str): Name of the mesh.

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
    """

    def __init__(self, vertices, cells, cell_sets=None, name=""):
        """See class docstring."""
        self.vertices = vertices
        self.cells = cells
        self.cell_sets = {} if cell_sets is None else cell_sets
        self.name = name

    def get_cells(self, cell_set_name):
        """Get the cell ids for a given cell set name.

        args:
            cell_set_name (str): name of the cell set for which to retrieve cell ids.

        returns:
            numpy.ndarray: cell ids of the set.
        """
        if cell_set_name in self.cell_sets:
            return self.cell_sets[cell_set_name]
        else:
            module_log.error(f"no cell set named '{cell_set_name}'.")

    def get_vertices_for_cells(self, cells):
        """Get the vertex IDs from cells.

        Args:
            cells (Iterable): Integer cell IDs.

        Returns:
            list of Iterables: Vertices for each cell.
        """
        verts = []
        keys = self.cells.keys()
        for cell in cells:
            for k in keys:
                if cell in self.cells[k]:
                    verts.append(self.cells[k][cell])
                    break

        module_log.require(
            len(verts) == len(cells),
            "Could not find one or more cells in the mesh."
            + f" len(verts)={len(verts)}, len(cells)={len(cells)}",
        )
        return verts

    def get_vertices(self, cell_set_name):
        """Get the vertex IDs for a given cell set name.

        Args:
            cell_set_name (str): Name of the cell set for which to retrieve cell IDs.

        Returns:
            numpy.ndarray: vertex IDs of the set.
        """
        vert_set = set()
        if cell_set_name in self.cell_sets:
            cells = self.get_cells(cell_set_name)
            verts = self.get_vertices_for_cells(cells)
            vert_set = vert_set.union(*verts)
            return np.fromiter(vert_set, int, len(vert_set))
        else:
            module_log.error(f"no cell set named '{cell_set_name}'.")

    def get_cell_area(self, cell):
        """Get the area of the cell with the given cell ID.

        Args:
            cell (int): The integer cell ID of the cell whose area will be calculated.

        Returns:
            float: The area of the cell.
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
            float: The area of the set.
        """
        module_log.info(f"Computing '{cell_set_name}' cell set area.")
        cells = self.get_cells(cell_set_name)
        area = 0.0
        for c in cells:
            area = area + self.get_cell_area(c)
        return area

    def make_gridmesh(self):
        """Turn a mesh with 'Grid_Ln_i_j' cell sets into :class:`mocmg.mesh.GridMesh` objects.

        Assumes that each grid cell sets is either partitioned by some combination of the next
        level of grid cell sets, or is the lowest level.

        Returns:
            mocmg.mesh.GridMesh: The root GridMesh object.
        """
        # Check that the mesh contains grid cell sets and that they partition eachother.
        set_names = list(self.cell_sets.keys())
        grid_names = list(self.cell_sets.keys())
        for set_name in set_names:
            if "GRID_" not in set_name.upper():
                grid_names.remove(set_name)

        module_log.require(len(grid_names) > 0, "No grid cell sets in mesh.")

        if self.name != "":
            name = self.name
        else:
            name = "mesh_domain"

        # Get the number of grid levels
        max_level = 0
        for grid_name in grid_names:
            level = int(grid_name[6])
            if max_level < level:
                max_level = level

        # Create hierarchy
        root = Node(name)
        current_nodes = []
        next_nodes = []
        old_grid_names = copy.deepcopy(grid_names)
        # Do first level
        for grid_name in old_grid_names:
            grid_level = int(grid_name[6])
            if grid_level == 1:
                # Add to appropriate node (root)
                next_nodes.append(Node(grid_name, parent=root))
                grid_names.remove(grid_name)
        # Do all other levels:
        for level in range(2, max_level + 1):
            old_grid_names = copy.deepcopy(grid_names)
            current_nodes = next_nodes
            next_nodes = []
            for grid_name in old_grid_names:
                grid_level = int(grid_name[6])
                if grid_level == level:
                    # find the parent for this grid
                    grid_cells = set(self.cell_sets[grid_name])
                    for node in current_nodes:
                        node_cells = set(self.cell_sets[node.name])
                        if grid_cells.issubset(node_cells):
                            next_nodes.append(Node(grid_name, parent=node))
                            break
                    grid_names.remove(grid_name)

        # Render the tree
        # for pre, fill, node in RenderTree(root):
        #     print("%s%s" % (pre, node.name))

        # Generate the lowest level entities
        for node in next_nodes:
            name = node.name
            # Get the cells
            cells_list = self.cell_sets[name]
            cells_type_and_id = {}
            # Categorize the cells by topological type
            for cell_type in list(self.cells.keys()):
                for cell in cells_list:
                    # If the cell is of this type, add it to the cells dict.
                    if cell in self.cells[cell_type]:
                        # if type is already in dict add the cell
                        if cell_type in cells_type_and_id:
                            cells_type_and_id[cell_type].append(cell)
                        # otherwise, add the type and cell
                        else:
                            cells_type_and_id[cell_type] = []
                            cells_type_and_id[cell_type].append(cell)

            # Turn this info into normal cells info
            cells = {}
            for cell_type in list(cells_type_and_id.keys()):
                cells[cell_type] = {}
                for cell in cells_type_and_id[cell_type]:
                    cells[cell_type][cell] = self.cells[cell_type][cell]

            # Get the vertices for all of these cells
            vertices_set = set(np.concatenate(self.get_vertices_for_cells(cells_list)))
            vertices = {}
            for vertex in vertices_set:
                vertices[vertex] = self.vertices[vertex]

            # Get all the cell sets
