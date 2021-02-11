"""Functions for reading and writing XDMF files."""
import logging
import os
import xml.etree.ElementTree as ETree

import h5py
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
    0x4: "triangle",
    0x5: "quad",
    0x9: "hexahedron",
    0x24: "triangle6",
    0x25: "quad8",
}

topo_type_to_xdmf_int = {v: k for k, v in xdmf_int_to_topo_type.items()}


def write_xdmf_file(filename, mesh, compression_opts=4):
    """Write a mesh object into a mesh object.

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

    xdmf_file = ETree.Element("Xdmf", Version="3.0")
    domain = ETree.SubElement(xdmf_file, "Domain")

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
            compression_opts,
        )

    tree = ETree.ElementTree(xdmf_file)
    tree.write(filename)


def _add_uniform_grid(
    name, xml_element, h5_filename, h5_group, vertices, cells, cell_sets, compression_opts
):
    """Add a uniform grid to the xml element and write the h5 data."""
    # Name is basically group list
    grid = ETree.SubElement(xml_element, "Grid", Name=name[-1], GridType="Uniform")
    # Create group for name
    this_h5_group = h5_group.create_group(name[-1])
    _add_geometry(grid, h5_filename, this_h5_group, vertices, compression_opts)
    _add_topology(grid, h5_filename, this_h5_group, vertices, cells, compression_opts)


def _add_geometry(grid, h5_filename, h5_group, vertices, compression_opts):
    """Add XYZ vertex locations in the geometry block."""
    geom = ETree.SubElement(grid, "Geometry", GeometryType="XYZ")
    vert_ids = list(vertices.keys())
    datatype, precision = numpy_to_xdmf_dtype[vertices[vert_ids[0]].dtype.name]
    dim = "{} {}".format(len(vert_ids), 3)
    vertices_data_item = ETree.SubElement(
        geom,
        "DataItem",
        DataType=datatype,
        Dimensions=dim,
        Format="HDF",
        Precision=precision,
    )
    h5_group.create_dataset(
        "VERTICES",
        data=np.stack(list(vertices.values())),
        compression="gzip",
        compression_opts=compression_opts,
    )
    vertices_data_item.text = os.path.basename(h5_filename) + ":" + h5_group.name + "/VERTICES"


def _map_to_0_index(keys):
    """Map data from current ID to 0 index for hdf5."""
    list_keys = list(keys)
    key_map = {}
    for i, key in enumerate(list_keys):
        key_map[key] = i
    return key_map


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
        topo = ETree.SubElement(
            grid,
            "Topology",
            TopologyType=xdmf_type,
            NumberOfElements=str(num_cells),
            NodesPerElement=str(verts_per_cell),
        )
        datatype, precision = numpy_to_xdmf_dtype[cell_arrays[0].dtype.name]
        dim = "{} {}".format(num_cells, verts_per_cell)
        topo_data_item = ETree.SubElement(
            topo,
            "DataItem",
            DataType=datatype,
            Dimensions=dim,
            Format="HDF",
            Precision=precision,
        )
        h5_group.create_dataset(
            "CELLS",
            data=np.stack(cell_arrays),
            compression="gzip",
            compression_opts=compression_opts,
        )
        topo_data_item.text = os.path.basename(h5_filename) + ":" + h5_group.name + "/CELLS"

    # Mixed topology
    else:
        module_log.error("Mixed topology not supported rn.")
