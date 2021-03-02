"""Functions for reading and writing XDMF files."""
import logging
import os

import h5py
import lxml.etree as etree
import numpy as np

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


def write_xdmf_file(filename, mesh, compression_opts=4):
    """Write a mesh object into an XDMF file.

    Args:
        filename (str) : File name of the form 'name.xdmf'.

        mesh (mocmg.mesh.Mesh) : The mesh object to save as an XDMF file.

        compression_opts (int, optional) : Compression level. May be an integer from 0 to 9, default is 4.

    """
    module_log.info(f"Writing mesh data to XDMF file '{filename}'.")
    vertices = mesh.vertices
    cells = mesh.cells
    cell_sets = mesh.cell_sets

    h5_filename = os.path.splitext(filename)[0] + ".h5"
    h5_file = h5py.File(h5_filename, "w")

    xdmf_file = etree.Element("Xdmf", Version="3.0")
    domain = etree.SubElement(xdmf_file, "Domain")

    # If no cell sets, just write one uniform grid.
    if cell_sets == {}:
        _add_uniform_grid(
            [os.path.splitext(filename)[0]],
            domain,
            h5_filename,
            h5_file,
            vertices,
            cells,
            cell_sets,
            [],
            compression_opts,
        )
    else:
        material_names, material_cells = _get_material_sets(cell_sets)
        if material_names:
            # print the material names before any grids
            material_information = etree.SubElement(domain, "Information", Name="MaterialNames")
            material_information.text = " ".join(material_names)

        _add_uniform_grid(
            [os.path.splitext(filename)[0]],
            domain,
            h5_filename,
            h5_file,
            vertices,
            cells,
            cell_sets,
            material_cells,
            compression_opts,
        )

    tree = etree.ElementTree(xdmf_file)
    tree.write(filename, pretty_print=True)
    h5_file.close()


def _add_uniform_grid(
    name,
    xml_element,
    h5_filename,
    h5_group,
    vertices,
    cells,
    cell_sets,
    material_cells,
    compression_opts,
):
    """Add a uniform grid to the xml element and write the h5 data."""
    # Name is basically group list
    grid = etree.SubElement(xml_element, "Grid", Name=name[-1], GridType="Uniform")
    # Create group for name
    this_h5_group = h5_group.create_group(name[-1])
    _add_geometry(grid, h5_filename, this_h5_group, vertices, compression_opts)
    _add_topology(grid, h5_filename, this_h5_group, vertices, cells, compression_opts)
    if material_cells:
        _add_materials(grid, h5_filename, this_h5_group, cells, material_cells, compression_opts)


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


def _get_material_sets(cell_sets):
    """Get the cell sets that are materials."""
    material_names = []
    material_cells = []
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
        cell_arrays = list(cells[topo_type].values())
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


def _add_materials(grid, h5_filename, h5_group, cells, material_cells, compression_opts):
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
    # Add check for multiple mat cells.
    for cell_type in cells.keys():
        for cell in cells[cell_type].keys():
            for i, material in enumerate(material_cells):
                if cell in material:
                    material_array[mat_ctr] = i
                    mat_ctr = mat_ctr + 1

    module_log.require(
        mat_ctr == total_num_cells,
        "Total number of cells ({total_num_cells}) not equal to number of cells with a material ({mat_ctr}).",
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
