"""The mesh class and related functions."""
import copy
import logging

import numpy as np
from anytree import Node  # , RenderTree

from .grid_mesh import GridMesh

module_log = logging.getLogger(__name__)


def make_gridmesh(mesh):
    """Turn a mesh with 'Grid_Ln_i_j' cell sets into :class:`mocmg.mesh.GridMesh` objects.

    Assumes that each grid cell sets is either partitioned by some combination of the next
    level of grid cell sets, or is the lowest level.

    Returns:
        mocmg.mesh.GridMesh: The root GridMesh object.
    """
    # Check that the mesh contains grid cell sets and that they partition eachother.
    set_names = list(mesh.cell_sets.keys())
    grid_names = list(mesh.cell_sets.keys())
    for set_name in set_names:
        if "GRID_" not in set_name.upper():
            grid_names.remove(set_name)

    module_log.require(len(grid_names) > 0, "No grid cell sets in mesh.")

    if mesh.name != "":
        name = mesh.name
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
                grid_cells = set(mesh.cell_sets[grid_name])
                for node in current_nodes:
                    node_cells = set(mesh.cell_sets[node.name])
                    if grid_cells.issubset(node_cells):
                        next_nodes.append(Node(grid_name, parent=node))
                        break
                grid_names.remove(grid_name)

    # Render the tree
    # for pre, fill, node in RenderTree(root):
    #     print("%s%s" % (pre, node.name))

    # Generate the highest level entities
    high_level_meshes = []
    for node in next_nodes:
        name = node.name
        # Get the cells
        cells_list = list(mesh.cell_sets[name])
        cells_type_and_id = {}
        # Categorize the cells by topological type
        for cell_type in list(mesh.cells.keys()):
            for cell in cells_list:
                # If the cell is of this type, add it to the cells dict.
                if cell in mesh.cells[cell_type]:
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
                cells[cell_type][cell] = mesh.cells[cell_type][cell]

        # Get the vertices for all of these cells
        vertices_set = set(np.concatenate(mesh.get_vertices_for_cells(cells_list)))
        vertices = {}
        for vertex in vertices_set:
            vertices[vertex] = mesh.vertices[vertex]

        # Get all the cell sets
        cell_sets = {}
        grid_cells_set = set(mesh.cell_sets[name])
        for set_name in set_names:
            # ignore the grid sets
            if "GRID_" in set_name.upper():
                continue
            else:
                cells_set = set(mesh.cell_sets[set_name])
                intersection_cells = grid_cells_set.intersection(cells_set)
                if intersection_cells:
                    cell_sets[set_name] = np.array(list(intersection_cells))

        # Initialize the mesh object
        high_level_meshes.append(GridMesh(vertices, cells, cell_sets, name=name))

    # Construct the mesh hierarchy
    child_nodes = next_nodes
    child_meshes = high_level_meshes
    parent_nodes = []
    parent_meshes = []
    for _level in range(max_level - 1, 0, -1):
        # Gather all parents
        for node in child_nodes:
            parent_node = node.parent
            if parent_node not in parent_nodes:
                parent_nodes.append(parent_node)
        # Create meshes for parent meshes
        for node in parent_nodes:
            node_children_names = [node_child.name for node_child in node.children]
            mesh_children = []
            for mesh in child_meshes:
                if mesh.name in node_children_names:
                    mesh_children.append(mesh)

            #            print(node.name, [child.name for child in mesh_children])
            parent_meshes.append(GridMesh(children=mesh_children, name=node.name))

        child_nodes = copy.deepcopy(parent_nodes)
        child_meshes = copy.deepcopy(parent_meshes)
        parent_nodes = []
        parent_meshes = []

    # Add L1 to root
    root_mesh = GridMesh(children=child_meshes, name=root.name)

    return root_mesh
