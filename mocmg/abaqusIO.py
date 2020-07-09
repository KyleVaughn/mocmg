import logging
import numpy as np
import os

module_log = logging.getLogger(__name__)

abaqus_to_topo_type = {
    # 2D
    # triangle
    "CPS3": "triangle",
    "STRI3": "triangle",
    "CPS6": "triangle6",
    # quad
    "CPS4": "quad",
    "CPS8": "quad8"
}

def readAbaqusINP(filepath):
    module_log.info(f'Reading mesh data from {filepath}') 
    if not os.path.isfile(filepath):
        module_log.error(f'File {filepath} not found')
    # read data in blocks based upon keyword
    nodes = {}
    elements = [] 
    element_sets = []
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
                nodes, line = _readNodes(f, nodes, floatbits)
            elif keyword == "ELEMENT":
                elem_type = _getParam(line, 'TYPE')
                elem_block, line = _readElements(f)
                elements.append([elem_type, elem_block])
            elif keyword == "ELSET":    
                element_set_name = _getParam(line, 'ELSET')
                elset, line = _readElementSet(f)
                element_sets.append([element_set_name, elset])
            else:
                line = f.readline()

    # convert abaqus types to topological types
    for e in elements:
        if e[0] in abaqus_to_topo_type.keys():
            e[0] = abaqus_to_topo_type[e[0]]
        else:
            module_log.error(f'Unrecognized mesh element type: {e[0]}')

    return nodes, elements, element_sets

def _readNodes(f, nodes, floatbits):
    while True:
        line = f.readline()
        if not line or line.startswith("*"):
            break

        line = line.strip().split(",")
        point_id, coords = line[0], line[1:]
        coords = np.array([float(x) for x in coords])
        nodes[int(point_id)] = coords

    return nodes, line

def _readElements(f):
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

def _readElementSet(f):
    elset = []
    while True:
        line = f.readline()
        if not line or line.startswith("*"):
            break

        line = line.strip().strip(",").split(",")
        elems = [int(x) for x in line]
        elset.extend(elems) 

    return np.array(elset, dtype=int), line

def _getParam(line, param):
    words = [w.strip().replace("*", "").upper() for w in line.split(",")]
    words = [w.split("=") for w in words]
    wordList = []
    for w in words:
        wordList.extend(w)

    if param == 'ELSET':
        wordList = wordList[1:]

    idx = wordList.index(param)
    
    return wordList[idx + 1]
