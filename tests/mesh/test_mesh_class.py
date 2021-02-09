"""Test the mesh class and its functions."""
from unittest import TestCase

import numpy as np
import pytest

import mocmg
import mocmg.mesh

# linear triangle data
linear_triangle_vertices = {
    1: np.array([-1.00000005e00, 1.06043306e-15, -5.00000000e-08]),
    2: np.array([-1.0000001e00, -1.0000001e00, -1.0000000e-07]),
    3: np.array([-1.05896103e-13, -1.00000005e00, -5.00000000e-08]),
    4: np.array([1.0, 0.0, 0.0]),
    5: np.array([1.0000001e00, -1.0000001e00, -1.0000000e-07]),
    6: np.array([-1.0000001e00, 1.0000001e00, -1.0000000e-07]),
    7: np.array([-1.08549196e-13, 1.00000005e00, -5.00000000e-08]),
    8: np.array([1.0000001e00, 1.0000001e00, -1.0000000e-07]),
    9: np.array([-0.70710678, -0.70710678, 0.0]),
    10: np.array([0.70710678, -0.70710678, 0.0]),
    11: np.array([-0.70710678, 0.70710678, 0.0]),
    12: np.array([0.70710678, 0.70710678, 0.0]),
    13: np.array([-0.26876582, 0.11132644, 0.0]),
    14: np.array([0.36327769, -0.15047455, 0.0]),
    15: np.array([0.19024025, 0.44768302, 0.0]),
    16: np.array([-0.18203951, -0.45107992, 0.0]),
}
linear_triangle_cells = {
    "triangle": {
        1: np.array([1, 16, 13]),
        2: np.array([9, 16, 1]),
        3: np.array([12, 15, 4]),
        4: np.array([13, 15, 11]),
        5: np.array([11, 15, 7]),
        6: np.array([10, 16, 3]),
        7: np.array([4, 15, 14]),
        8: np.array([14, 16, 10]),
        9: np.array([1, 13, 11]),
        10: np.array([4, 14, 10]),
        11: np.array([7, 15, 12]),
        12: np.array([3, 16, 9]),
        13: np.array([14, 15, 13]),
        14: np.array([13, 16, 14]),
        15: np.array([2, 9, 1]),
        16: np.array([2, 3, 9]),
        17: np.array([10, 5, 4]),
        18: np.array([3, 5, 10]),
        19: np.array([1, 11, 6]),
        20: np.array([6, 11, 7]),
        21: np.array([12, 4, 8]),
        22: np.array([7, 12, 8]),
    },
}
linear_triangle_cell_sets = {
    "DISK": np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]),
    "MATERIAL_VOID": np.array([15, 16, 17, 18, 19, 20, 21, 22]),
}

# quadratic triangle mesh
quadratic_triangle_vertices = {
    1: np.array([-1.00000005e00, 1.06043306e-15, -5.00000000e-08]),
    2: np.array([-1.0000001e00, -1.0000001e00, -1.0000000e-07]),
    3: np.array([-1.05896103e-13, -1.00000005e00, -5.00000000e-08]),
    4: np.array([1.0, 0.0, 0.0]),
    5: np.array([1.0000001e00, -1.0000001e00, -1.0000000e-07]),
    6: np.array([-1.0000001e00, 1.0000001e00, -1.0000000e-07]),
    7: np.array([-1.08549196e-13, 1.00000005e00, -5.00000000e-08]),
    8: np.array([1.0000001e00, 1.0000001e00, -1.0000000e-07]),
    9: np.array([-1.00000010e00, -5.00841281e-01, -1.00000000e-07]),
    10: np.array([-0.70708298, -0.70713058, 0.0]),
    11: np.array([-0.91703972, -0.39879588, 0.0]),
    12: np.array([-0.39884673, -0.9170176, 0.0]),
    13: np.array([-5.00840823e-01, -1.00000010e00, -1.00000000e-07]),
    14: np.array([0.70708302, -0.70713055, 0.0]),
    15: np.array([0.39889911, -0.91699482, 0.0]),
    16: np.array([0.9170161, -0.39885019, 0.0]),
    17: np.array([1.0000001e00, -5.0084097e-01, -1.0000000e-07]),
    18: np.array([5.00840536e-01, -1.00000010e00, -1.00000000e-07]),
    19: np.array([-1.00000010e00, 5.00840994e-01, -1.00000000e-07]),
    20: np.array([-5.00840522e-01, 1.00000010e00, -1.00000000e-07]),
    21: np.array([-0.70708007, 0.7071335, 0.0]),
    22: np.array([-0.3988993, 0.91699474, 0.0]),
    23: np.array([-0.91701595, 0.39885053, 0.0]),
    24: np.array([0.70708387, 0.70712969, 0.0]),
    25: np.array([0.91703964, 0.39879607, 0.0]),
    26: np.array([0.39884522, 0.91701826, 0.0]),
    27: np.array([5.00840838e-01, 1.00000010e00, -1.00000000e-07]),
    28: np.array([1.0000001e00, 5.0084126e-01, -1.0000000e-07]),
    29: np.array([-0.26874902, 0.11131954, 0.0]),
    30: np.array([0.36325451, -0.15046501, 0.0]),
    31: np.array([0.19021621, 0.4476254, 0.0]),
    32: np.array([-0.182016, -0.45102208, 0.0]),
    33: np.array([-0.59112954, -0.22558921, 0.0]),
    34: np.array([-0.22540267, -0.16987674, 0.0]),
    35: np.array([-0.63443287, 0.05569767, 0.0]),
    36: np.array([-0.44461198, -0.57917949, 0.0]),
    37: np.array([0.44871232, 0.57747943, 0.0]),
    38: np.array([0.59523122, 0.22389143, 0.0]),
    39: np.array([-0.03926279, 0.27950473, 0.0]),
    40: np.array([-0.25847266, 0.57750255, 0.0]),
    41: np.array([-0.48799137, 0.4092244, 0.0]),
    42: np.array([0.09515393, 0.72394368, 0.0]),
    43: np.array([0.26257348, -0.57920237, 0.0]),
    44: np.array([-0.09105243, -0.72564101, 0.0]),
    45: np.array([0.27675898, 0.14860423, 0.0]),
    46: np.array([0.68170888, -0.07528174, 0.0]),
    47: np.array([0.0906191, -0.30077723, 0.0]),
    48: np.array([0.53526786, -0.42880511, 0.0]),
    49: np.array([0.04725594, -0.01957406, 0.0]),
    50: np.array([-8.47201857e-01, -8.47201870e-01, -1.00000000e-07]),
    51: np.array([8.47201868e-01, -8.47201877e-01, -1.00000000e-07]),
    52: np.array([-8.47201866e-01, 8.47201879e-01, -1.00000000e-07]),
    53: np.array([8.47201860e-01, 8.47201868e-01, -1.00000000e-07]),
}
quadratic_triangle_cells = {
    "triangle6": {
        1: np.array([1, 32, 29, 33, 34, 35]),
        2: np.array([10, 32, 1, 36, 33, 11]),
        3: np.array([24, 31, 4, 37, 38, 25]),
        4: np.array([29, 31, 21, 39, 40, 41]),
        5: np.array([21, 31, 7, 40, 42, 22]),
        6: np.array([14, 32, 3, 43, 44, 15]),
        7: np.array([4, 31, 30, 38, 45, 46]),
        8: np.array([30, 32, 14, 47, 43, 48]),
        9: np.array([1, 29, 21, 35, 41, 23]),
        10: np.array([4, 30, 14, 46, 48, 16]),
        11: np.array([7, 31, 24, 42, 37, 26]),
        12: np.array([3, 32, 10, 44, 36, 12]),
        13: np.array([30, 31, 29, 45, 39, 49]),
        14: np.array([29, 32, 30, 34, 47, 49]),
        15: np.array([2, 10, 1, 50, 11, 9]),
        16: np.array([2, 3, 10, 13, 12, 50]),
        17: np.array([14, 5, 4, 51, 17, 16]),
        18: np.array([3, 5, 14, 18, 51, 15]),
        19: np.array([1, 21, 6, 23, 52, 19]),
        20: np.array([6, 21, 7, 52, 22, 20]),
        21: np.array([24, 4, 8, 25, 28, 53]),
        22: np.array([7, 24, 8, 26, 53, 27]),
    },
}
quadratic_triangle_cell_sets = {
    "DISK": np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]),
    "MATERIAL_VOID": np.array([15, 16, 17, 18, 19, 20, 21, 22]),
}

# Linear quadrilateral
linear_quadrilateral_vertices = {
    1: np.array([-1.00000005e00, 1.06043306e-15, -5.00000000e-08]),
    2: np.array([-1.0000001e00, -1.0000001e00, -1.0000000e-07]),
    3: np.array([-1.05896103e-13, -1.00000005e00, -5.00000000e-08]),
    4: np.array([1.0, 0.0, 0.0]),
    5: np.array([1.0000001e00, -1.0000001e00, -1.0000000e-07]),
    6: np.array([-1.0000001e00, 1.0000001e00, -1.0000000e-07]),
    7: np.array([-1.08549196e-13, 1.00000005e00, -5.00000000e-08]),
    8: np.array([1.0000001e00, 1.0000001e00, -1.0000000e-07]),
    9: np.array([-1.0000001e00, -5.0000005e-01, -1.0000000e-07]),
    10: np.array([-0.70710678, -0.70710678, 0.0]),
    11: np.array([-0.38268343, -0.92387953, 0.0]),
    12: np.array([-0.92387953, -0.38268343, 0.0]),
    13: np.array([-5.0000005e-01, -1.0000001e00, -1.0000000e-07]),
    14: np.array([0.70710678, -0.70710678, 0.0]),
    15: np.array([0.38268343, -0.92387953, 0.0]),
    16: np.array([0.92387953, -0.38268343, 0.0]),
    17: np.array([1.0000001e00, -5.0000005e-01, -1.0000000e-07]),
    18: np.array([5.0000005e-01, -1.0000001e00, -1.0000000e-07]),
    19: np.array([-1.0000001e00, 5.0000005e-01, -1.0000000e-07]),
    20: np.array([-5.0000005e-01, 1.0000001e00, -1.0000000e-07]),
    21: np.array([-0.70710678, 0.70710678, 0.0]),
    22: np.array([-0.38268343, 0.92387953, 0.0]),
    23: np.array([-0.92387953, 0.38268343, 0.0]),
    24: np.array([0.70710678, 0.70710678, 0.0]),
    25: np.array([0.38268343, 0.92387953, 0.0]),
    26: np.array([0.92387953, 0.38268343, 0.0]),
    27: np.array([5.0000005e-01, 1.0000001e00, -1.0000000e-07]),
    28: np.array([1.0000001e00, 5.0000005e-01, -1.0000000e-07]),
    29: np.array([-0.3792915, 0.15650978, 0.0]),
    30: np.array([0.38168151, -0.15842764, 0.0]),
    31: np.array([0.15872338, 0.37986656, 0.0]),
    32: np.array([-0.15649223, -0.38174939, 0.0]),
    33: np.array([-0.50784728, 0.42138252, 0.0]),
    34: np.array([-0.65722191, 0.06066527, 0.0]),
    35: np.array([-0.69553448, 0.28790546, 0.0]),
    36: np.array([0.50919023, -0.42239878, 0.0]),
    37: np.array([0.65850471, -0.061772, 0.0]),
    38: np.array([0.69644173, -0.28863769, 0.0]),
    39: np.array([0.42252446, 0.50821553, 0.0]),
    40: np.array([0.06197349, 0.65756204, 0.0]),
    41: np.array([0.2887463, 0.69579777, 0.0]),
    42: np.array([-0.42134337, -0.50931208, 0.0]),
    43: np.array([-0.06076066, -0.6585379, 0.0]),
    44: np.array([-0.28794272, -0.69650722, 0.0]),
    45: np.array([0.27370682, 0.11206271, 0.0]),
    46: np.array([0.56633144, 0.23392666, 0.0]),
    47: np.array([0.11443226, -0.27341729, 0.0]),
    48: np.array([0.23500879, -0.5662575, 0.0]),
    49: np.array([-0.27110596, -0.11440358, 0.0]),
    50: np.array([-0.56503275, -0.23508101, 0.0]),
    51: np.array([-0.11166725, 0.27156671, 0.0]),
    52: np.array([-0.23365889, 0.56524013, 0.0]),
    53: np.array([0.00136546, -0.00109045, 0.0]),
    54: np.array([-7.90828267e-01, -7.90828264e-01, -1.00000000e-07]),
    55: np.array([-5.69668535e-01, -9.09867896e-01, -1.00000000e-07]),
    56: np.array([-9.09867913e-01, -5.69668535e-01, -1.00000000e-07]),
    57: np.array([7.90828264e-01, -7.90828264e-01, -1.00000000e-07]),
    58: np.array([5.69668535e-01, -9.09867896e-01, -1.00000000e-07]),
    59: np.array([9.09867896e-01, -5.69668535e-01, -1.00000000e-07]),
    60: np.array([-7.90828292e-01, 7.90828292e-01, -1.00000000e-07]),
    61: np.array([-5.69668535e-01, 9.09867913e-01, -1.00000000e-07]),
    62: np.array([-9.09867913e-01, 5.69668535e-01, -1.00000000e-07]),
    63: np.array([7.90828264e-01, 7.90828264e-01, -1.00000000e-07]),
    64: np.array([5.69668535e-01, 9.09867896e-01, -1.00000000e-07]),
    65: np.array([9.09867896e-01, 5.69668535e-01, -1.00000000e-07]),
}

linear_quadrilateral_cells = {
    "quad": {
        1: np.array([1, 34, 35, 23]),
        2: np.array([21, 23, 35, 33]),
        3: np.array([29, 33, 35, 34]),
        4: np.array([4, 37, 38, 16]),
        5: np.array([14, 16, 38, 36]),
        6: np.array([30, 36, 38, 37]),
        7: np.array([7, 40, 41, 25]),
        8: np.array([24, 25, 41, 39]),
        9: np.array([31, 39, 41, 40]),
        10: np.array([3, 43, 44, 11]),
        11: np.array([10, 11, 44, 42]),
        12: np.array([32, 42, 44, 43]),
        13: np.array([4, 26, 46, 37]),
        14: np.array([30, 37, 46, 45]),
        15: np.array([31, 45, 46, 39]),
        16: np.array([24, 39, 46, 26]),
        17: np.array([32, 43, 48, 47]),
        18: np.array([30, 47, 48, 36]),
        19: np.array([14, 36, 48, 15]),
        20: np.array([3, 15, 48, 43]),
        21: np.array([32, 49, 50, 42]),
        22: np.array([10, 42, 50, 12]),
        23: np.array([1, 12, 50, 34]),
        24: np.array([29, 34, 50, 49]),
        25: np.array([21, 33, 52, 22]),
        26: np.array([7, 22, 52, 40]),
        27: np.array([31, 40, 52, 51]),
        28: np.array([29, 51, 52, 33]),
        29: np.array([30, 45, 53, 47]),
        30: np.array([32, 47, 53, 49]),
        31: np.array([29, 49, 53, 51]),
        32: np.array([31, 51, 53, 45]),
        33: np.array([10, 54, 55, 11]),
        34: np.array([3, 11, 55, 13]),
        35: np.array([2, 13, 55, 54]),
        36: np.array([2, 54, 56, 9]),
        37: np.array([1, 9, 56, 12]),
        38: np.array([10, 12, 56, 54]),
        39: np.array([5, 57, 58, 18]),
        40: np.array([3, 18, 58, 15]),
        41: np.array([14, 15, 58, 57]),
        42: np.array([14, 57, 59, 16]),
        43: np.array([4, 16, 59, 17]),
        44: np.array([5, 17, 59, 57]),
        45: np.array([6, 60, 61, 20]),
        46: np.array([7, 20, 61, 22]),
        47: np.array([21, 22, 61, 60]),
        48: np.array([21, 60, 62, 23]),
        49: np.array([1, 23, 62, 19]),
        50: np.array([6, 19, 62, 60]),
        51: np.array([24, 63, 64, 25]),
        52: np.array([7, 25, 64, 27]),
        53: np.array([8, 27, 64, 63]),
        54: np.array([8, 63, 65, 28]),
        55: np.array([4, 28, 65, 26]),
        56: np.array([24, 26, 65, 63]),
    },
}
linear_quadrilateral_cell_sets = {
    "DISK": np.array(
        [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
            26,
            27,
            28,
            29,
            30,
            31,
            32,
        ]
    ),
    "MATERIAL_VOID": np.array(
        [
            32,
            33,
            34,
            35,
            36,
            37,
            38,
            39,
            40,
            41,
            42,
            43,
            44,
            45,
            46,
            47,
            48,
            49,
            50,
            51,
            52,
            53,
            54,
            56,
        ]
    ),
}

# Quadratic quadrilateral
quadratic_quadrilateral_vertices = {
    1: np.array([-1.00000005e00, 1.06043306e-15, -5.00000000e-08]),
    2: np.array([-1.0000001e00, -1.0000001e00, -1.0000000e-07]),
    3: np.array([-1.05896103e-13, -1.00000005e00, -5.00000000e-08]),
    4: np.array([1.0, 0.0, 0.0]),
    5: np.array([1.0000001e00, -1.0000001e00, -1.0000000e-07]),
    6: np.array([-1.0000001e00, 1.0000001e00, -1.0000000e-07]),
    7: np.array([-1.08549196e-13, 1.00000005e00, -5.00000000e-08]),
    8: np.array([1.0000001e00, 1.0000001e00, -1.0000000e-07]),
    9: np.array([-1.00000010e00, -4.98511454e-01, -1.00000000e-07]),
    10: np.array([-1.00000010e00, -2.52365176e-01, -1.00000000e-07]),
    11: np.array([-1.00000010e00, -7.51512278e-01, -1.00000000e-07]),
    12: np.array([-0.70710673, -0.70710683, 0.0]),
    13: np.array([-0.91479328, -0.40392235, 0.0]),
    14: np.array([-0.4039225, -0.91479321, 0.0]),
    15: np.array([-4.98511453e-01, -1.00000010e00, -1.00000000e-07]),
    16: np.array([-7.51512278e-01, -1.00000010e00, -1.00000000e-07]),
    17: np.array([-2.52365179e-01, -1.00000010e00, -1.00000000e-07]),
    18: np.array([0.70710602, -0.70710754, 0.0]),
    19: np.array([0.40392263, -0.91479315, 0.0]),
    20: np.array([0.91479409, -0.40392051, 0.0]),
    21: np.array([1.00000010e00, -4.98511455e-01, -1.00000000e-07]),
    22: np.array([1.00000010e00, -7.51512278e-01, -1.00000000e-07]),
    23: np.array([1.00000010e00, -2.52365135e-01, -1.00000000e-07]),
    24: np.array([4.98511459e-01, -1.00000010e00, -1.00000000e-07]),
    25: np.array([2.52365169e-01, -1.00000010e00, -1.00000000e-07]),
    26: np.array([7.51512278e-01, -1.00000010e00, -1.00000000e-07]),
    27: np.array([-1.00000010e00, 4.98511454e-01, -1.00000000e-07]),
    28: np.array([-1.00000010e00, 7.51512278e-01, -1.00000000e-07]),
    29: np.array([-1.00000010e00, 2.52365177e-01, -1.00000000e-07]),
    30: np.array([-4.98511454e-01, 1.00000010e00, -1.00000000e-07]),
    31: np.array([-2.52365177e-01, 1.00000010e00, -1.00000000e-07]),
    32: np.array([-7.51512278e-01, 1.00000010e00, -1.00000000e-07]),
    33: np.array([-0.70710673, 0.70710683, 0.0]),
    34: np.array([-0.4039225, 0.91479321, 0.0]),
    35: np.array([-0.91479328, 0.40392235, 0.0]),
    36: np.array([0.70710602, 0.70710754, 0.0]),
    37: np.array([0.91479409, 0.40392051, 0.0]),
    38: np.array([0.40392263, 0.91479315, 0.0]),
    39: np.array([4.98511459e-01, 1.00000010e00, -1.00000000e-07]),
    40: np.array([7.51512278e-01, 1.00000010e00, -1.00000000e-07]),
    41: np.array([2.52365169e-01, 1.00000010e00, -1.00000000e-07]),
    42: np.array([1.00000010e00, 4.98511455e-01, -1.00000000e-07]),
    43: np.array([1.00000010e00, 2.52365135e-01, -1.00000000e-07]),
    44: np.array([1.00000010e00, 7.51512278e-01, -1.00000000e-07]),
    45: np.array([9.40648347e-09, 1.55599465e-11, 0.00000000e00]),
    46: np.array([0.34876797, -0.34876795, 0.0]),
    47: np.array([-0.34876795, -0.34876795, 0.0]),
    48: np.array([-0.34876795, 0.34876795, 0.0]),
    49: np.array([0.34876797, 0.34876795, 0.0]),
    50: np.array([-7.35485354e-01, -7.35485333e-01, -1.00000000e-07]),
    51: np.array([-8.76962152e-01, -6.28131775e-01, -1.00000000e-07]),
    52: np.array([-7.19452931e-01, -7.19452916e-01, -1.00000000e-07]),
    53: np.array([-6.28131780e-01, -8.76962143e-01, -1.00000000e-07]),
    54: np.array([7.35485298e-01, -7.35485357e-01, -1.00000000e-07]),
    55: np.array([6.28131775e-01, -8.76962123e-01, -1.00000000e-07]),
    56: np.array([7.19453006e-01, -7.19452939e-01, -1.00000000e-07]),
    57: np.array([8.76962194e-01, -6.28131808e-01, -1.00000000e-07]),
    58: np.array([-7.35485351e-01, 7.35485352e-01, -1.00000000e-07]),
    59: np.array([-7.19452905e-01, 7.19452905e-01, -1.00000000e-07]),
    60: np.array([-8.76962150e-01, 6.28131775e-01, -1.00000000e-07]),
    61: np.array([-6.28131775e-01, 8.76962150e-01, -1.00000000e-07]),
    62: np.array([7.35485298e-01, 7.35485357e-01, -1.00000000e-07]),
    63: np.array([8.76962194e-01, 6.28131808e-01, -1.00000000e-07]),
    64: np.array([7.19453006e-01, 7.19452939e-01, -1.00000000e-07]),
    65: np.array([6.28131775e-01, 8.76962123e-01, -1.00000000e-07]),
}
quadratic_quadrilateral_cells = {
    "quad8": {
        1: np.array([3, 18, 45, 12, 19, 46, 47, 14]),
        2: np.array([1, 12, 45, 33, 13, 47, 48, 35]),
        3: np.array([7, 33, 45, 36, 34, 48, 49, 38]),
        4: np.array([4, 36, 45, 18, 37, 49, 46, 20]),
        5: np.array([1, 9, 50, 12, 10, 51, 52, 13]),
        6: np.array([2, 15, 50, 9, 16, 53, 51, 11]),
        7: np.array([3, 12, 50, 15, 14, 52, 53, 17]),
        8: np.array([3, 24, 54, 18, 25, 55, 56, 19]),
        9: np.array([4, 18, 54, 21, 20, 56, 57, 23]),
        10: np.array([5, 21, 54, 24, 22, 57, 55, 26]),
        11: np.array([1, 33, 58, 27, 35, 59, 60, 29]),
        12: np.array([6, 27, 58, 30, 28, 60, 61, 32]),
        13: np.array([7, 30, 58, 33, 31, 61, 59, 34]),
        14: np.array([4, 42, 62, 36, 43, 63, 64, 37]),
        15: np.array([7, 36, 62, 39, 38, 64, 65, 41]),
        16: np.array([8, 39, 62, 42, 40, 65, 63, 44]),
    },
}

quadratic_quadrilateral_cell_sets = {
    "DISK": np.array([1, 2, 3, 4]),
    "MATERIAL_VOID": np.array([5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]),
}


class TestMesh(TestCase):
    """Test the mesh class and its functions."""

    def test_linear_triangle(self):
        """Test the mesh class functions on a linear triangle mesh."""
        ref_vertices = linear_triangle_vertices
        ref_cells = linear_triangle_cells
        ref_cell_sets = linear_triangle_cell_sets
        mocmg.initialize()
        mesh = mocmg.mesh.Mesh(ref_vertices, ref_cells, ref_cell_sets)
        self.assertEqual(mesh.vertices, ref_vertices)
        self.assertEqual(mesh.cells, ref_cells)
        self.assertEqual(mesh.cell_sets, ref_cell_sets)
        # get_cells
        cell_set = mesh.get_cells("DISK")
        self.assertTrue(np.array_equal(cell_set, linear_triangle_cell_sets["DISK"]))
        # get_cell_area
        cell_area_ref = 0.210453
        cell_area = mesh.get_cell_area(1)
        self.assertAlmostEqual(cell_area, cell_area_ref, 6)
        # Try w/ name that doesnt exist.
        with pytest.raises(SystemExit):
            cell_set = mesh.get_cells("BAD NAME")
        # get_set_area
        set_area_ref = 2.828427
        set_area = mesh.get_set_area("DISK")
        self.assertAlmostEqual(set_area, set_area_ref, 6)

    def test_quadratic_triangle(self):
        """Test the mesh class functions on a quadratic triangle mesh."""
        ref_vertices = quadratic_triangle_vertices
        ref_cells = quadratic_triangle_cells
        ref_cell_sets = quadratic_triangle_cell_sets
        mocmg.initialize()
        mesh = mocmg.mesh.Mesh(ref_vertices, ref_cells, ref_cell_sets)
        self.assertEqual(mesh.vertices, ref_vertices)
        self.assertEqual(mesh.cells, ref_cells)
        self.assertEqual(mesh.cell_sets, ref_cell_sets)
        # get_cells
        cell_set = mesh.get_cells("DISK")
        self.assertTrue(np.array_equal(cell_set, quadratic_triangle_cell_sets["DISK"]))
        # get_cell_area
        cell_area_ref = 0.261949
        cell_area = mesh.get_cell_area(2)
        self.assertAlmostEqual(cell_area, cell_area_ref, 6)
        # get_set_area
        set_area_ref = 3.1391725
        set_area = mesh.get_set_area("DISK")
        self.assertAlmostEqual(set_area, set_area_ref, 6)

    def test_linear_quadrilateral(self):
        """Test the mesh class functions on a linear quadrilateral mesh."""
        ref_vertices = linear_quadrilateral_vertices
        ref_cells = linear_quadrilateral_cells
        ref_cell_sets = linear_quadrilateral_cell_sets
        mesh = mocmg.mesh.Mesh(ref_vertices, ref_cells, ref_cell_sets)
        self.assertEqual(mesh.vertices, ref_vertices)
        self.assertEqual(mesh.cells, ref_cells)
        self.assertEqual(mesh.cell_sets, ref_cell_sets)
        # get_cells
        cell_set = mesh.get_cells("DISK")
        self.assertTrue(np.array_equal(cell_set, linear_quadrilateral_cell_sets["DISK"]))
        # get_cell_area
        cell_area_ref = 0.0874078
        cell_area = mesh.get_cell_area(1)
        self.assertAlmostEqual(cell_area, cell_area_ref, 6)
        # get_set_area
        set_area_ref = 3.0614675
        set_area = mesh.get_set_area("DISK")
        self.assertAlmostEqual(set_area, set_area_ref, 6)

    def test_quadratic_quadrilateral(self):
        """Test the mesh class functions on a quadratic quadrilateral mesh."""
        ref_vertices = quadratic_quadrilateral_vertices
        ref_cells = quadratic_quadrilateral_cells
        ref_cell_sets = quadratic_quadrilateral_cell_sets
        mesh = mocmg.mesh.Mesh(ref_vertices, ref_cells, ref_cell_sets)
        self.assertEqual(mesh.vertices, ref_vertices)
        self.assertEqual(mesh.cells, ref_cells)
        self.assertEqual(mesh.cell_sets, ref_cell_sets)
        # get_cells
        cell_set = mesh.get_cells("DISK")
        self.assertTrue(np.array_equal(cell_set, quadratic_quadrilateral_cell_sets["DISK"]))
        # get_cell_area
        cell_area_ref = 0.7847974
        cell_area = mesh.get_cell_area(1)
        self.assertAlmostEqual(cell_area, cell_area_ref, 6)
        # get_set_area
        set_area_ref = 3.1391907
        set_area = mesh.get_set_area("DISK")
        self.assertAlmostEqual(set_area, set_area_ref, 6)
