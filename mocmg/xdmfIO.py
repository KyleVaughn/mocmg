import h5py
import logging
import numpy as np
import os
import xml.etree.ElementTree as ET

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

def _writeXML(filename, root):
    tree = ET.ElementTree(root)
    tree.write(filename)

def writeXDMF(filename, nodes, elements, element_sets=None, compression_opts=4, multifile=False):
    h5_filename = os.path.splitext(filename)[0] + ".h5"
    h5_file = h5py.File(h5_filename, "w")

    xdmf_file = ET.Element("Xdmf", Version="3.0")
    domain = ET.SubElement(xdmf_file, "Domain")
    grid = ET.SubElement(domain, "Grid", Name="Grid")

    # nodes/geom
    geo = ET.SubElement(grid, "Geometry", GeometryType="XYZ")
    nkeys = list(nodes.keys())
    dt, prec = numpy_to_xdmf_dtype[ nodes[nkeys[0]].dtype.name ]
    dim = "{} {}".format(len(nkeys), 3)
    data_item = ET.SubElement(
        geo,
        "DataItem",
        DataType=dt,
        Dimensions=dim,
        Format="HDF",
        Precision=prec,
    )
    # node numbering lost in hdf5. Need to adjust dict keys in elements, sets
    h5_file.create_dataset(
        "nodes",
        data=np.stack(nodes.values()),
        compression="gzip",
        compression_opts=compression_opts,
    )
    del nodes
    data_item.text = os.path.basename(h5_filename) + ":/" + "nodes"

    # adjust elements node numbering to hdf5
    # create dict for map from node numbering to h5 number for fast lookup
    nodemap = {node: h5node for h5node, node in enumerate(nkeys)}
    del nkeys
    for eid, msh in enumerate(elements):
        ekeys = msh[1].keys()
        for k in ekeys:
            elements[eid][1][k] = np.array([nodemap[node] for node in msh[1][k]], dtype=int)
    del nodemap

    # adjust elsets element numbering to hdf5
    # elements are written in order of list
    # need to construct global elem map
    ecounter = 0
    elemmap = {}
    for eid, msh in enumerate(elements):
        ekeys = list(msh[1].keys())
        for h5elem, elem in enumerate(ekeys):
            elemmap[elem] = h5elem + ecounter
        ecounter += len(ekeys)
    # now that we have global map, iterate through each elset
    for sid, eset in enumerate(element_sets):
        element_sets[sid][1] = np.array([elemmap[elem] for elem in element_sets[sid][1]], dtype=int)            
    del elemmap, ekeys, ecounter

    # elements/topology
    if len(elements) == 1:
        topo_type = elements[0][0]
        xdmf_type = topo_to_xdmf_type[topo_type][0]
        num_cells = len(elements[0][1])
        # 1st array in dict
        first_array = elements[0][1][ list(elements[0][1].keys())[0]]
        nodes_per_elem = len(first_array)
        topo = ET.SubElement(
            grid,
            "Topology",
            TopologyType=xdmf_type,
            NumberOfElements=str(num_cells),
            NodesPerElement=str(nodes_per_elem),
        )
        dt, prec = numpy_to_xdmf_dtype[first_array.dtype.name]
        dim = "{} {}".format(num_cells, nodes_per_elem)
        data_item = ET.SubElement(
            topo,
            "DataItem",
            DataType=dt,
            Dimensions=dim,
            Format="HDF",
            Precision=prec,
        )
        h5_file.create_dataset(
            "elements",
            data=np.stack(elements[0][1].values()),
            compression="gzip",
            compression_opts=compression_opts,
        )
        del elements
        data_item.text = os.path.basename(h5_filename) + ":/" + "elements" 


    


    _writeXML(filename, xdmf_file)
