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
        self.points = points
        self.cells = cells
        self.cell_sets = {} if cell_sets is None else cell_sets

    def getCells(self, cell_set):
        for sname, array in self.cell_sets:
            if cell_set == sname:
                return array
        module_log.error(f'No cell set named {cell_set}') 
    

    def cellHasQuadraticEdges(self, cell_type):
        if cell_type in quadratic_edges:
            return quadratic_edges[cell_type]
        else:
            module_log.error(f'No cell type {cell_type} in quadratic edge dictionary.') 

    
    def getCellArea(self, cell):
        cell_exists = False
        # Find the cell
        for cell_type, cell_dict in self.cells:
            if cell in cell_dict:
                cell_exists = True
                # Compute area
                if self.cellHasQuadraticEdges(cell_type):
                    # Adjust area for quad edges
                    module_log.error(f'Quad edges not currently supported for cell type: {cell_type}')
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
                    correction = x_[-1] * y_[0] - y_[-1]* x_[0]
                    main_area = np.dot(x_[:-1], y_[1:]) - np.dot(y_[:-1], x_[1:])
                    return 0.5*np.abs(main_area + correction)
        if not cell_exists:
            module_log.error(f'Cell {c} does not exist')


    def getSetArea(self, cell_set):
        cells = self.getCells(cell_set) 
        area = 0.0
        for c in cells:
            area = area + self.getCellArea(c)
        return area
