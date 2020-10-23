import logging
import numpy as np

module_log = logging.getLogger(__name__)

quadratic_edges = {
    "quad": False,
    "quad8": True,
    "triangle": False,
    "triangle6": True,
}


class Mesh:

    def __init__(self, points, cells, cell_sets):
        # points is a dictionary with integer keys and numpy array values, corresponding
        # to point ID and spatial coordinates respectively
        # ex: {1: np.array([ 1.,  0.,  0.])}
        self.points = points
        # Cells is a list of lists. Each sublist has the form:
        # ['type_string', dictionary]
        # where the type string is triangle, quad8, etc.
        # The dictionary has integer keys and numpy array values.
        # This dictionary denotes cell ID and the vertex ID that make up the cell.
        # ex:
        # [
        #    ['triangle', {
        #              1: np.array([1, 2, 3]),
        #              2: np.array([2, 3, 4]),
        #              }
        #    ],
        #    ['quad', {
        #          3: np.array([1, 2, 5, 6]),
        #          }
        #    ]
        # ]
        self.cells = cells
        # cell_sets is a list of lists. Each sublist is of the form
        # ['label', np.array]
        # where label is the name of the cell set and the numpy array contains the integer IDs
        # of the cells in that set
        # ex:
        # [
        #     ['Material_UO2', np.array([1, 2, 3])],
        #     ['Material_MOX', np.array([4, 5])],
        # ]
        self.cell_sets = {} if cell_sets is None else cell_sets

    # input name of cell set, return the cell IDs
    def getCells(self, cell_set):
        for sname, array in self.cell_sets:
            if cell_set == sname:
                return array
        module_log.error(f'No cell set named {cell_set}')
        raise ValueError(f'No cell set named {cell_set}')

    # input cell type, return True if has quad edges, False if not
    def cellHasQuadraticEdges(self, cell_type):
        if cell_type in quadratic_edges:
            return quadratic_edges[cell_type]
        else:
            module_log.error(f'No cell type {cell_type} in quadratic edge dictionary.')
            raise ValueError(f'No cell type {cell_type} in quadratic edge dictionary.')

    # Input cell ID, return area of cell
    def getCellArea(self, cell):
        cell_exists = False
        # Find the cell
        for cell_type, cell_dict in self.cells:
            if cell in cell_dict:
                cell_exists = True
                # Compute area
                if self.cellHasQuadraticEdges(cell_type):
                    # Get linear area and adjust area for quad edges
                    vertices = cell_dict[cell]
                    if cell_type == 'triangle6':
                        x_lin = np.array([self.points[v][0] for v in vertices[0:3]])
                        y_lin = np.array([self.points[v][1] for v in vertices[0:3]])
                        x_quad = np.array([self.points[v][0] for v in vertices[3:6]])
                        y_quad = np.array([self.points[v][1] for v in vertices[3:6]])
                    elif cell_type == 'quad8':
                        x_lin = np.array([self.points[v][0] for v in vertices[0:4]])
                        y_lin = np.array([self.points[v][1] for v in vertices[0:4]])
                        x_quad = np.array([self.points[v][0] for v in vertices[4:8]])
                        y_quad = np.array([self.points[v][1] for v in vertices[4:8]])
                    else: # pragma: no cover
                        module_log.error('Unsupported cell type in quadratic area calculation')
                        raise ValueError('Unsupported cell type in quadratic area calculation')

                    # No quadratic edges shoelace formula may be used
                    # https://en.wikipedia.org/wiki/Shoelace_formula
                    # Assumes that vertices are in clockwise or counterclockwise order
# https://stackoverflow.com/questions/24467972/calculate-area-of-polygon-given-x-y-coordinates
                    x_ = x_lin - x_lin.mean()
                    y_ = y_lin - y_lin.mean()
                    correction = x_[-1]*y_[0] - y_[-1]*x_[0]
                    main_area = np.dot(x_[:-1], y_[1:]) - np.dot(y_[:-1], x_[1:])
                    area = 0.5*np.abs(main_area + correction)
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
                    # Assume all edges quad
                    # For each edge, compute additional area using quadratic function
                    # Shift point to origin, rotate so line is x-axis, find quadratic function
                    # with 3 point fit, integrate, add or subtract based on right or left
                    nvert = len(x_lin)
                    for i in range(-1, nvert-1):
                        x_e = np.array([x_lin[i], x_lin[i+1], x_quad[i]])
                        y_e = np.array([y_lin[i], y_lin[i+1], y_quad[i]])
                        # shift to origin
                        x_e = x_e - x_e[0]
                        y_e = y_e - y_e[0]
                        # rotate line to x-axis
                        theta = np.arctan(y_e[1]/x_e[1])
                        if x_e[1] < 0:
                            theta = theta + np.pi
                        R = np.array([
                                [np.cos(theta), np.sin(theta)],
                                [-np.sin(theta), np.cos(theta)]
                                ])
                        for j in range(1, 3):
                            v = np.array([
                                [x_e[j]],
                                [y_e[j]]
                                ])
                            v_ = np.dot(R, v)
                            x_e[j] = v_[0]
                            y_e[j] = v_[1]
                        # Get quadratic coefficients and integrate
                        # ax^2 + bx + c
                        p = np.poly1d(np.polyfit(x_e, y_e, 2))
                        P = np.polyint(p)
                        quadarea = P(x_e[1]) - P(0)
                        # quadarea will be opposite of correct sign
                        area = area - quadarea
                    return area
                else:
                    # No quadratic edges shoelace formula may be used
                    # https://en.wikipedia.org/wiki/Shoelace_formula
                    # Assumes that vertices are in clockwise or counterclockwise order
                    # https://stackoverflow.com/questions/24467972/calculate-area-of-polygon-given-x-y-coordinates
                    vertices = cell_dict[cell]
                    x = np.array([self.points[v][0] for v in vertices])
                    y = np.array([self.points[v][1] for v in vertices])
                    x_ = x - x.mean()
                    y_ = y - y.mean()
                    correction = x_[-1]*y_[0] - y_[-1]*x_[0]
                    main_area = np.dot(x_[:-1], y_[1:]) - np.dot(y_[:-1], x_[1:])
                    return 0.5*np.abs(main_area + correction)
        if not cell_exists: # pragma: no cover
            module_log.error(f'Cell {cell} does not exist in this mesh')
            raise ValueError(f'Cell {cell} does not exist in this mesh')

    def getSetArea(self, cell_set):
        module_log.info(f"Computing '{cell_set}' cell set area")
        cells = self.getCells(cell_set)
        area = 0.0
        for c in cells:
            area = area + self.getCellArea(c)
        return area
