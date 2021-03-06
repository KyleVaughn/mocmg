"""Functions for reading and writing XDMF files."""
import logging
import os
from copy import deepcopy

import h5py
import lxml.etree as etree
import numpy as np

from mocmg.mesh import GridMesh, Mesh

module_log = logging.getLogger(__name__)

numpy_to_xdmf_dtype = {
    "int32": ("Int", "4"),
    "int64": ("Int", "8"),
    "uint32": ("UInt", "4"),
    "uint64": ("UInt", "8"),
    "float32": ("Float", "4"),
    "float64": ("Float", "8"),
}

topo_to_xdmf_type = {
    "quad": ["Quadrilateral"],
    "quad8": ["Quadrilateral_8", "Quad_8"],
    "triangle": ["Triangle"],
    "triangle6": ["Triangle_6", "Tri_6"],
}

xdmf_int_to_topo_type = {
    4: "triangle",
    5: "quad",
    36: "triangle6",
    37: "quad8",
}

topo_type_to_xdmf_int = {v: k for k, v in xdmf_int_to_topo_type.items()}


def write_xdmf_file(filename, mesh, split_level=None, material_name_map=None, compression_opts=4):
    """Write a mesh object into an XDMF file.

    Note that if a mesh has any materials, it is assumed that every cell has a material.
    A :class:`mocmg.mesh.Mesh` is written as one uniform grid without a mesh hierarchy.
    A :class:`mocmg.mesh.GridMesh` is assumed to be partitioned by cell sets of the 'GRID' form.
    The GridMesh is written in the XDMF as a tree of the child meshes.
    See the GridMesh docstring for more info.

    Args:
        filename (str) : File name of the form 'name.xdmf'.

        mesh (mocmg.mesh.Mesh) : The mesh object to save as an XDMF file.

        split_level (int, optional) : Split the mesh into different files based on grid level provided.

        compression_opts (int, optional) : Compression level. May be an integer from 0 to 9, default is 4.

    """
    module_log.require(isinstance(mesh, Mesh), "Invalid type given as input.")

    if material_name_map is None and (isinstance(mesh, GridMesh) or mesh.cell_sets):
        module_log.info("Generating global material ID map.")
        material_name_map, material_ctr = _make_global_material_id_map(mesh)

    if split_level is not None:
        _handle_split_level(filename, mesh, split_level, material_name_map, compression_opts)
        return

    module_log.info(f"Writing mesh data to XDMF file '{filename}'.")
    if isinstance(mesh, Mesh) and not isinstance(mesh, GridMesh):
        h5_filename = os.path.splitext(filename)[0] + ".h5"
        h5_file = h5py.File(h5_filename, "w")

        xdmf_file = etree.Element("Xdmf", Version="3.0")
        domain = etree.SubElement(xdmf_file, "Domain")

        vertices = mesh.vertices
        cells = mesh.cells
        cell_sets = mesh.cell_sets

        if material_name_map:
            # print the material names before any grids
            material_names = list(material_name_map.keys())
            material_information = etree.SubElement(domain, "Information", Name="MaterialNames")
            material_information.text = " ".join(material_names)

        if mesh.name != "":
            name = mesh.name
        else:
            name = [os.path.splitext(filename)[0]][-1]

        _add_uniform_grid(
            name,
            domain,
            h5_filename,
            h5_file,
            vertices,
            cells,
            cell_sets,
            material_name_map,
            compression_opts,
        )

        tree = etree.ElementTree(xdmf_file)
        tree.write(filename, pretty_print=True, encoding="utf-8", xml_declaration=True)
        h5_file.close()

    else:
        module_log.require(isinstance(mesh, GridMesh), "Bad type.")
        h5_filename = os.path.splitext(filename)[0] + ".h5"
        h5_file = h5py.File(h5_filename, "w")

        xdmf_file = etree.Element("Xdmf", Version="3.0")
        domain = etree.SubElement(xdmf_file, "Domain")

        if material_name_map:
            # print the material names before any grids
            material_names = list(material_name_map.keys())
            material_information = etree.SubElement(domain, "Information", Name="MaterialNames")
            material_information.text = " ".join(material_names)

        # Add all grid levels
        _add_gridmesh_levels(
            [(domain, mesh)],
            h5_filename,
            h5_file,
            material_name_map,
            compression_opts=compression_opts,
        )

        tree = etree.ElementTree(xdmf_file)
        tree.write(filename, pretty_print=True, encoding="utf-8", xml_declaration=True)
        h5_file.close()


def _add_uniform_grid(
    name,
    xml_element,
    h5_filename,
    h5_group,
    vertices,
    cells,
    cell_sets,
    material_name_map,
    compression_opts,
):
    """Add a uniform grid to the xml element and write the h5 data."""
    # Name is basically group list
    grid = etree.SubElement(xml_element, "Grid", Name=name, GridType="Uniform")
    # Create group for name
    material_names, material_cells = _get_material_sets(cell_sets)
    this_h5_group = h5_group.create_group(name)
    _add_geometry(grid, h5_filename, this_h5_group, vertices, compression_opts)
    _add_topology(grid, h5_filename, this_h5_group, vertices, cells, compression_opts)

    if cell_sets:
        _add_cell_sets(grid, h5_filename, this_h5_group, cells, cell_sets, compression_opts)
    if material_cells:
        _add_materials(
            grid,
            h5_filename,
            this_h5_group,
            cells,
            material_name_map,
            material_names,
            material_cells,
            compression_opts,
        )


def _add_geometry(grid, h5_filename, h5_group, vertices, compression_opts):
    """Add XYZ vertex locations in the geometry block."""
    geom = etree.SubElement(grid, "Geometry", GeometryType="XYZ")
    vert_ids = list(vertices.keys())
    datatype, precision = numpy_to_xdmf_dtype[vertices[vert_ids[0]].dtype.name]
    dim = "{} {}".format(len(vert_ids), 3)
    vertices_data_item = etree.SubElement(
        geom,
        "DataItem",
        DataType=datatype,
        Dimensions=dim,
        Format="HDF",
        Precision=precision,
    )
    h5_group.create_dataset(
        "vertices",
        data=np.stack(list(vertices.values())),
        compression="gzip",
        compression_opts=compression_opts,
    )
    vertices_data_item.text = os.path.basename(h5_filename) + ":" + h5_group.name + "/vertices"


def _map_to_0_index(keys):
    """Map data from current ID to 0 index for hdf5."""
    list_keys = list(keys)
    key_map = {}
    for i, key in enumerate(list_keys):
        key_map[key] = i
    return key_map


def _make_global_material_id_map(mesh):
    """Generate a map from material name to integer ID."""
    material_name_map = {}
    material_ctr = 0
    if isinstance(mesh, GridMesh):
        # Get the leaves
        mesh_children = [mesh]
        next_mesh_children = []
        leaves_reached = False
        while not leaves_reached:
            for child_mesh in mesh_children:
                if child_mesh.children is not None:
                    next_mesh_children.extend(child_mesh.children)
                else:
                    leaves_reached = True
            if not leaves_reached:
                mesh_children = next_mesh_children
                next_mesh_children = []
    else:
        mesh_children = [mesh]

    for child_mesh in mesh_children:
        cell_sets = child_mesh.cell_sets
        if cell_sets:
            set_names = list(cell_sets.keys())
            for set_name in set_names:
                if ("MATERIAL" in set_name.upper()) and (set_name.upper() not in material_name_map):
                    material_name_map[set_name.replace(" ", "_").upper()] = material_ctr
                    material_ctr = material_ctr + 1

    _print_material_names_and_ids(material_ctr, material_name_map)

    return material_name_map, material_ctr


def _print_material_names_and_ids(material_ctr, material_name_map):
    if material_ctr > 0:
        module_log.info("Material Name        : Material ID")
        module_log.info("==================================")
        for mat_name in list(material_name_map.keys()):
            module_log.info(f"{mat_name.ljust(20)} : {material_name_map[mat_name]}")


def _get_material_sets(cell_sets):
    """Get the cell sets that are materials."""
    material_names = []
    material_cells = []
    if cell_sets:
        set_names = list(cell_sets.keys())
        for set_name in set_names:
            if "MATERIAL" in set_name.upper():
                material_names.append(set_name.replace(" ", "_").upper())
                material_cells.append(cell_sets.pop(set_name))

    return material_names, material_cells


def _add_topology(grid, h5_filename, h5_group, vertices, cells, compression_opts):
    """Add mesh cells in the topology block."""
    # Get map of vertex IDs to 0 index hdf5 data
    vert_map = _map_to_0_index(vertices.keys())

    # Single topology
    if len(cells) == 1:
        topo_type = list(cells.keys())[0]
        xdmf_type = topo_to_xdmf_type[topo_type][0]
        cell_arrays = list(deepcopy(cells[topo_type]).values())
        # convert vertices to hdf5 local 0 index
        for i in range(len(cell_arrays)):
            for j in range(len(cell_arrays[i])):
                cell_arrays[i][j] = vert_map[cell_arrays[i][j]]

        num_cells = len(cell_arrays)
        verts_per_cell = len(cell_arrays[0])
        topo = etree.SubElement(
            grid,
            "Topology",
            TopologyType=xdmf_type,
            NumberOfElements=str(num_cells),
            NodesPerElement=str(verts_per_cell),
        )
        datatype, precision = numpy_to_xdmf_dtype[cell_arrays[0].dtype.name]
        dim = "{} {}".format(num_cells, verts_per_cell)
        topo_data_item = etree.SubElement(
            topo,
            "DataItem",
            DataType=datatype,
            Dimensions=dim,
            Format="HDF",
            Precision=precision,
        )
        h5_group.create_dataset(
            "cells",
            data=np.stack(cell_arrays),
            compression="gzip",
            compression_opts=compression_opts,
        )
        topo_data_item.text = os.path.basename(h5_filename) + ":" + h5_group.name + "/cells"

    # Mixed topology
    else:
        total_num_cells = sum(len(cells[cell_type]) for cell_type in cells.keys())
        topo = etree.SubElement(
            grid,
            "Topology",
            TopologyType="Mixed",
            NumberOfElements=str(total_num_cells),
        )

        vert_map = _map_to_0_index(vertices.keys())
        topo_data = []
        total_num_verts = 0
        for cell_type in cells.keys():
            first_array = cells[cell_type][list(cells[cell_type].keys())[0]]
            verts_per_cell = len(first_array)
            num_cells = len(cells[cell_type].keys())
            total_num_verts += num_cells * verts_per_cell
            xdmf_int = topo_type_to_xdmf_int[cell_type]
            for cell in cells[cell_type].values():
                new_cell_verts = np.zeros(verts_per_cell + 1, dtype=np.int64)
                new_cell_verts[0] = xdmf_int
                for i, vert in enumerate(cell):
                    new_cell_verts[i + 1] = vert_map[vert]
                topo_data.append(new_cell_verts)

        dim = str(total_num_cells + total_num_verts)
        datatype, precision = numpy_to_xdmf_dtype[first_array.dtype.name]
        topo_data_item = etree.SubElement(
            topo,
            "DataItem",
            DataType=datatype,
            Dimensions=dim,
            Format="HDF",
            Precision=precision,
        )
        h5_group.create_dataset(
            "cells",
            data=np.concatenate(topo_data),
            compression="gzip",
            compression_opts=compression_opts,
        )
        topo_data_item.text = os.path.basename(h5_filename) + ":" + h5_group.name + "/cells"


def _add_materials(
    grid,
    h5_filename,
    h5_group,
    cells,
    material_name_map,
    material_names,
    material_cells,
    compression_opts,
):
    """Add materials in an attribute block."""
    material_attribute = etree.SubElement(
        grid,
        "Attribute",
        Center="Cell",
        Name="MaterialID",
    )
    total_num_cells = sum(len(cells[cell_type]) for cell_type in cells.keys())
    material_array = np.zeros(total_num_cells, dtype=np.int64) - 1
    mat_ctr = 0
    # If any cell has multiple materials this is going to give index out of bounds.
    # TODO: Add check for multiple mat cells, but no cell should have multiple materials
    for cell_type in cells.keys():
        for cell in cells[cell_type].keys():
            for i, material in enumerate(material_names):
                if cell in material_cells[i]:
                    material_array[mat_ctr] = material_name_map[material]
                    mat_ctr = mat_ctr + 1

    module_log.require(
        mat_ctr == total_num_cells,
        f"Total number of cells ({total_num_cells}) not equal to "
        + f"number of cells with a material ({mat_ctr}).",
    )
    module_log.require(all(material_array >= 0), "A cell was not assigned a material.")
    datatype, precision = numpy_to_xdmf_dtype[material_array[0].dtype.name]
    material_id_data_item = etree.SubElement(
        material_attribute,
        "DataItem",
        DataType=datatype,
        Dimensions=str(total_num_cells),
        Format="HDF",
        Precision=precision,
    )
    h5_group.create_dataset(
        "material_id",
        data=material_array,
        compression="gzip",
        compression_opts=compression_opts,
    )
    material_id_data_item.text = (
        os.path.basename(h5_filename) + ":" + h5_group.name + "/material_id"
    )


def _add_cell_sets(grid, h5_filename, h5_group, cells, cell_sets, compression_opts):
    """Add cells_sets in set blocks."""
    set_names = list(cell_sets.keys())
    # Need to map the cell ids in cell sets to how the data appears in the h5 by mapping to
    # a 0 index array.
    cell_id_map = {}
    cell_ctr = 0
    for cell_type in cells.keys():
        for cell_id in cells[cell_type].keys():
            cell_id_map[cell_id] = cell_ctr
            cell_ctr = cell_ctr + 1

    for set_name in set_names:
        set_block = etree.SubElement(grid, "Set", Name=set_name, SetType="Cell")
        set_cells = cell_sets[set_name]
        set_cells_post_map = np.zeros(len(set_cells), dtype=np.int64)
        for i, cell_id in enumerate(set_cells):
            set_cells_post_map[i] = cell_id_map[cell_id]
        datatype, precision = numpy_to_xdmf_dtype[set_cells_post_map[0].dtype.name]
        dim = str(len(set_cells_post_map))
        set_data_item = etree.SubElement(
            set_block,
            "DataItem",
            DataType=datatype,
            Dimensions=dim,
            Format="HDF",
            Precision=precision,
        )
        h5_group.create_dataset(
            set_name,
            data=set_cells_post_map,
            compression="gzip",
            compression_opts=compression_opts,
        )
        set_data_item.text = os.path.basename(h5_filename) + ":" + h5_group.name + "/" + set_name


def _add_gridmesh_levels(
    xml_mesh_list, h5_filename, h5_group, material_name_map, compression_opts=4
):
    child_list = []
    for parent_xml_tree, mesh in xml_mesh_list:
        # If it has children, write the tree and add children to child list
        if mesh.children is not None:
            mesh_xml_tree = etree.SubElement(
                parent_xml_tree, "Grid", Name=mesh.name, GridType="Tree"
            )
            for child_mesh in mesh.children:
                child_list.append((mesh_xml_tree, child_mesh))
        else:
            # If there are not children, this must be the bottom level. Write the data
            _add_uniform_grid(
                mesh.name,
                parent_xml_tree,
                h5_filename,
                h5_group,
                mesh.vertices,
                mesh.cells,
                mesh.cell_sets,
                material_name_map,
                compression_opts,
            )

    if child_list:
        _add_gridmesh_levels(child_list, h5_filename, h5_group, material_name_map, compression_opts)


def _handle_split_level(filename, mesh, split_level, material_name_map, compression_opts):
    # Check that the level is appropriate
    module_log.require(split_level >= 0, "split_level must be greater than or equal to 0.")
    # If level is 0, write
    if split_level == 0:
        write_xdmf_file(
            filename,
            mesh,
            split_level=None,
            material_name_map=material_name_map,
            compression_opts=compression_opts,
        )

    # Otherwise call next level
    else:
        next_mesh = mesh
        for _i in range(split_level):
            module_log.require(
                next_mesh.children is not None,
                "split_level is too high. Not enough grid levels in mesh.",
            )
            next_mesh = next_mesh.children[0]
        for child in mesh.children:
            new_filename = os.path.splitext(filename)[0] + "_" + child.name + ".xdmf"
            write_xdmf_file(
                new_filename,
                child,
                split_level=split_level - 1,
                material_name_map=material_name_map,
                compression_opts=compression_opts,
            )
