"""Functions for reading and writing Abaqus files."""
import logging

import numpy as np

from .mesh import Mesh

module_log = logging.getLogger(__name__)

abaqus_to_topo_type = {
    # 2D
    # triangle
    "CPS3": "triangle",
    "STRI3": "triangle",
    "CPS6": "triangle6",
    # quad
    "CPS4": "quad",
    "CPS8": "quad8",
}

abaqus_1d = {
    "T3D2": "line",
}


def read_abaqus_file(filepath):
    """Read an Abaqus file into a mesh object."""
    module_log.info(f"Reading mesh data from {filepath}")
    # read data in blocks based upon keyword
    nodes = {}
    elements = {}
    element_sets = {}
    with open(filepath) as f:
        line = f.readline()
        while True:
            # EOF
            if not line:
                break

            # Comment
            if line.startswith("**"):
                line = f.readline()
                continue

            # Keywords
            keyword = line.partition(",")[0].strip().replace("*", "").upper()
            if keyword == "NODE":
                nodes, line = _read_nodes(f, nodes)
            elif keyword == "ELEMENT":
                elem_type = _get_param(line, "TYPE")
                elem_block, line = _read_elements(f)
                if elem_type in elements:
                    elements[elem_type].update(elem_block)
                else:
                    elements[elem_type] = elem_block
            elif keyword == "ELSET":
                element_set_name = _get_param(line, "ELSET")
                elset, line = _read_element_set(f)
                # If an elset is split into multiple sections, uncomment this code.
                #                if element_set_name in element_sets:
                #                    element_sets[element_set_name] = np.concatenate(
                #                        element_sets[element_set_name], elset
                #                    )
                #                else:
                element_sets[element_set_name] = elset
            else:
                line = f.readline()

    _convert_abaqus_to_topo_type(elements)

    return Mesh(nodes, elements, element_sets)


def _convert_abaqus_to_topo_type(elements):
    # Remove 1D elements, since they are not currently used
    keys = [k for k in elements.keys()]
    for key in keys:
        if key in abaqus_1d:
            elements.pop(key)

    # convert abaqus types to mesh class topological types
    keys = [k for k in elements.keys()]
    for key in keys:
        module_log.require(key in abaqus_to_topo_type, f"Unrecognized mesh element type: '{key}'.")
        elements[abaqus_to_topo_type[key]] = elements.pop(key)


def _read_nodes(f, nodes):
    while True:
        line = f.readline()
        if not line or line.startswith("*"):
            break

        line = line.strip().split(",")
        point_id, coords = line[0], line[1:]
        coords = np.array([float(x) for x in coords])
        nodes[int(point_id)] = coords

    return nodes, line


def _read_elements(f):
    elem_block = {}
    while True:
        line = f.readline()
        if not line or line.startswith("*"):
            break

        line = line.strip().split(",")
        elem_id, node_ids = line[0], line[1:]
        node_ids = np.array([int(x) for x in node_ids], dtype=int)
        elem_block[int(elem_id)] = node_ids

    return elem_block, line


def _read_element_set(f):
    elset = []
    while True:
        line = f.readline()
        if not line or line.startswith("*"):
            break

        line = line.strip().strip(",").split(",")
        elems = [int(x) for x in line]
        elset.extend(elems)

    return np.array(elset, dtype=int), line


def _get_param(line, param):
    words = [w.strip().replace("*", "").upper() for w in line.split(",")]
    words = [w.split("=") for w in words]
    word_list = []
    for w in words:
        word_list.extend(w)

    if param == "ELSET":
        word_list = word_list[1:]

    idx = word_list.index(param)

    return word_list[idx + 1]
