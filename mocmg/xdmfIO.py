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

xdmf_idx_to_topo_type = {
    0x4: "triangle",
    0x5: "quad",
    0x9: "hexahedron",
    0x24: "triangle6",
    0x25: "quad8",
}
topo_type_to_xdmf_idx = {v: k for k, v in xdmf_idx_to_topo_type.items()}

def _writeXML(filename, root):
    tree = ET.ElementTree(root)
    tree.write(filename)

def writeXDMF(filename, nodes, elements, element_sets=None, compression_opts=4, multifile=False):
    module_log.info('Writing mesh data to XDMF file')
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
    nodes_data_item = ET.SubElement(
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
    nodes_data_item.text = os.path.basename(h5_filename) + ":/" + "nodes"

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
    if element_sets != None:
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
    # if all surfaces same topology, merge into one dict
    if len(elements) > 1:
        topos = [elem[0] for elem in elements]
        if topos.count(topos[0]) == len(topos):
            for eid in range(1,len(topos)):
                elements[0][1].update(elements[1][1])
                del elements[1] 
        del topos    

    # if all elements same topology, write more efficient format
    if len(elements) == 1:
        topo_type = elements[0][0]
        xdmf_type = topo_to_xdmf_type[topo_type][0]
        num_elems = len(elements[0][1])
        # 1st array in dict
        first_array = elements[0][1][ list(elements[0][1].keys())[0]]
        nodes_per_elem = len(first_array)
        topo = ET.SubElement(
            grid,
            "Topology",
            TopologyType=xdmf_type,
            NumberOfElements=str(num_elems),
            NodesPerElement=str(nodes_per_elem),
        )
        dt, prec = numpy_to_xdmf_dtype[first_array.dtype.name]
        dim = "{} {}".format(num_elems, nodes_per_elem)
        topo_data_item = ET.SubElement(
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
        topo_data_item.text = os.path.basename(h5_filename) + ":/" + "elements" 
        del elements

    # mixed topology
    else:
        assert len(elements) > 1
        total_num_elements = sum(len(e[1].keys()) for e in elements) 
        topo = ET.SubElement(
            grid,
            "Topology",
            TopologyType="Mixed",
            NumberOfElements=str(total_num_elements),
        )

        total_num_elements_nodes = 0 
        for e in elements:
            first_array = e[1][ list(e[1].keys())[0]]
            nodes_per_elem = len(first_array)
            elems = len(e[1].keys())
            total_num_elements_nodes += elems * nodes_per_elem

        dim = str(total_num_elements_nodes + total_num_elements)
        dt, prec = numpy_to_xdmf_dtype[first_array.dtype.name]
        topo_data_item = ET.SubElement(
            topo,
            "DataItem",
            DataType=dt,
            Dimensions=dim,
            Format="HDF",
            Precision=prec,
        )

        elem_data = {}
        for eid, e in enumerate(elements):
            key = e[0]
            xdmf_key = np.array(topo_type_to_xdmf_idx[key])
            elem_data[eid] = [np.concatenate((xdmf_key, array), axis=None) for array in e[1].values()]

        elem_data = np.concatenate(list(elem_data.values()), axis=None)
        h5_file.create_dataset(
            "elements",
            data=elem_data,
            compression="gzip",
            compression_opts=compression_opts,
        )
        topo_data_item.text = os.path.basename(h5_filename) + ":/" + "elements"
        del elements
        del elem_data

    # Element set data
    if element_sets != None:
        # split elsets into material and non-material
        materials = []
        other_sets = []
        for sid in range(len(element_sets)):
            if element_sets[0][0][0:8] == 'MATERIAL':
                materials.append(element_sets[0])
            else: 
                other_sets.append(element_sets[0])
            del element_sets[0]
            
        # Just write material for now.
        # All elements must have a material, so material is written as attribute to save space
        # integer to represent unique names of elsets
        mat_len = len(materials)
        materials_id = np.zeros(mat_len, dtype=np.uint32) - 1
        materials_name = []
        mat_ctr = 0
        for i in range(mat_len):
            if materials_id[i] == 4294967295:
                # new material. Set to next int and find sets with same mat.
                materials_id[i] = mat_ctr
                mat_name = materials[i][0]
                materials_name.append(mat_name)
                for j in range(i,mat_len):
                    if materials[j][0] == mat_name:
                        materials_id[j] = mat_ctr 
                mat_ctr += 1

        # Construct ordered list of material numbers for each cell
        num_elems = 0
        for i in range(mat_len):
            num_elems += len(materials[i][1])

        material_array = np.zeros(num_elems, dtype=np.uint32) - 1
        for i in range(mat_len):
            mat_id = materials_id[i] 
            for eid in materials[0][1]:
                material_array[eid] = mat_id
            del materials[0]

        # Write materials data to file
        material_attribute = ET.SubElement(
            grid,
            "Attribute",
            Center="Cell",
            Name="Material_ID",
        )
        dt, prec = numpy_to_xdmf_dtype[material_array.dtype.name ]
        mat_data_item = ET.SubElement(
            material_attribute,    
            "DataItem",
            DataType=dt,
            Dimensions=str(len(material_array)),
            Format="HDF",
            Precision=prec,
        )
        h5_file.create_dataset(
            "Material_ID",
            data=material_array,
            compression="gzip",
            compression_opts=compression_opts,
        )
        mat_data_item.text = os.path.basename(h5_filename) + ":/" + "Material_ID"

        # Info section for material ID to material name
        

    _writeXML(filename, xdmf_file)
