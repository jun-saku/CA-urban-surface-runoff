"""
transfunc.py - Documentation

Required modules:
- numpy

This file contains the necessary methods for calculating the probability
matrix from the elevation data using matrix operations instead of multiple
for loops.
"""

import numpy as np


# create modified elevation array
def modified_arr(a):
    # add zeros around elevation values
    b = np.insert(a, 0, np.zeros(a.shape[1]), axis=0)    # add number of columns (shape[1]) to row ([0])
    b = np.insert(b, 0, np.zeros(b.shape[0]), axis=1)    # vice versa
    b = np.insert(b, b.shape[0], np.zeros(b.shape[1]), axis=0)
    b = np.insert(b, b.shape[1], np.zeros(b.shape[0]), axis=1)
    return b


# creation of neighbor arrays (a = original elev, b = modified elev)
def nh_3darr(a, b):
    # create reference array size
    nh = np.array([b])

    nh_1 = np.insert(a, 0, np.zeros(a.shape[1]), axis=0)
    nh_1 = np.insert(nh_1, 0, np.zeros(nh_1.shape[1]), axis=0)
    nh_1 = np.insert(nh_1, 0, np.zeros(nh_1.shape[0]), axis=1)
    nh_1 = np.insert(nh_1, 0, np.zeros(nh_1.shape[0]), axis=1)
    nh = np.append(nh, [nh_1], axis=0)

    nh_2 = np.insert(a, 0, np.zeros(a.shape[1]), axis=0)
    nh_2 = np.insert(nh_2, 0, np.zeros(nh_2.shape[1]), axis=0)
    nh_2 = np.insert(nh_2, 0, np.zeros(nh_2.shape[0]), axis=1)
    nh_2 = np.insert(nh_2, nh_2.shape[1], np.zeros(nh_2.shape[0]), axis=1)
    nh = np.append(nh, [nh_2], axis=0)

    nh_3 = np.insert(a, 0, np.zeros(a.shape[1]), axis=0)
    nh_3 = np.insert(nh_3, 0, np.zeros(nh_3.shape[1]), axis=0)
    nh_3 = np.insert(nh_3, nh_3.shape[1], np.zeros(nh_3.shape[0]), axis=1)
    nh_3 = np.insert(nh_3, nh_3.shape[1], np.zeros(nh_3.shape[0]), axis=1)
    nh = np.append(nh, [nh_3], axis=0)

    nh_4 = np.insert(a, 0, np.zeros(a.shape[1]), axis=0)
    nh_4 = np.insert(nh_4, nh_4.shape[0], np.zeros(nh_4.shape[1]), axis=0)
    nh_4 = np.insert(nh_4, 0, np.zeros(nh_4.shape[0]), axis=1)
    nh_4 = np.insert(nh_4, 0, np.zeros(nh_4.shape[0]), axis=1)
    nh = np.append(nh, [nh_4], axis=0)

    nh_5 = np.insert(a, 0, np.zeros(a.shape[1]), axis=0)
    nh_5 = np.insert(nh_5, nh_5.shape[0], np.zeros(nh_5.shape[1]), axis=0)
    nh_5 = np.insert(nh_5, nh_5.shape[1], np.zeros(nh_5.shape[0]), axis=1)
    nh_5 = np.insert(nh_5, nh_5.shape[1], np.zeros(nh_5.shape[0]), axis=1)
    nh = np.append(nh, [nh_5], axis=0)

    nh_6 = np.insert(a, 0, np.zeros(a.shape[0]), axis=1)
    nh_6 = np.insert(nh_6, 0, np.zeros(nh_6.shape[0]), axis=1)
    nh_6 = np.insert(nh_6, nh_6.shape[0], np.zeros(nh_6.shape[1]), axis=0)
    nh_6 = np.insert(nh_6, nh_6.shape[0], np.zeros(nh_6.shape[1]), axis=0)
    nh = np.append(nh, [nh_6], axis=0)

    nh_7 = np.insert(a, 0, np.zeros(a.shape[0]), axis=1)
    nh_7 = np.insert(nh_7, nh_7.shape[1], np.zeros(nh_7.shape[0]), axis=1)
    nh_7 = np.insert(nh_7, nh_7.shape[0], np.zeros(nh_7.shape[1]), axis=0)
    nh_7 = np.insert(nh_7, nh_7.shape[0], np.zeros(nh_7.shape[1]), axis=0)
    nh = np.append(nh, [nh_7], axis=0)

    nh_8 = np.insert(a, a.shape[1], np.zeros(a.shape[0]), axis=1)
    nh_8 = np.insert(nh_8, nh_8.shape[1], np.zeros(nh_8.shape[0]), axis=1)
    nh_8 = np.insert(nh_8, nh_8.shape[0], np.zeros(nh_8.shape[1]), axis=0)
    nh_8 = np.insert(nh_8, nh_8.shape[0], np.zeros(nh_8.shape[1]), axis=0)
    nh = np.append(nh, [nh_8], axis=0)

    # delete reference array (index 0)
    nh = nh[1:]

    return nh


# restore neighbors to original matrix shape
def restore(nh_p, a):
    # reference shape
    up = np.array([a])

    p_1 = np.delete(nh_p[0], 0, axis=0)
    p_1 = np.delete(p_1, 0, axis=0)
    p_1 = np.delete(p_1, 0, axis=1)
    p_1 = np.delete(p_1, 0, axis=1)
    up = np.append(up, [p_1], axis=0)

    p_2 = np.delete(nh_p[1], 0, axis=0)
    p_2 = np.delete(p_2, 0, axis=0)
    p_2 = np.delete(p_2, 0, axis=1)
    p_2 = np.delete(p_2, p_2.shape[1] - 1, axis=1)
    up = np.append(up, [p_2], axis=0)

    p_3 = np.delete(nh_p[2], 0, axis=0)
    p_3 = np.delete(p_3, 0, axis=0)
    p_3 = np.delete(p_3, p_3.shape[1] - 1, axis=1)
    p_3 = np.delete(p_3, p_3.shape[1] - 1, axis=1)
    up = np.append(up, [p_3], axis=0)

    p_4 = np.delete(nh_p[3], 0, axis=0)
    p_4 = np.delete(p_4, p_4.shape[0] - 1, axis=0)
    p_4 = np.delete(p_4, 0, axis=1)
    p_4 = np.delete(p_4, 0, axis=1)
    up = np.append(up, [p_4], axis=0)

    p_5 = np.delete(nh_p[4], 0, axis=0)
    p_5 = np.delete(p_5, p_5.shape[0] - 1, axis=0)
    p_5 = np.delete(p_5, p_5.shape[1] - 1, axis=1)
    p_5 = np.delete(p_5, p_5.shape[1] - 1, axis=1)
    up = np.append(up, [p_5], axis=0)

    p_6 = np.delete(nh_p[5], 0, axis=1)
    p_6 = np.delete(p_6, 0, axis=1)
    p_6 = np.delete(p_6, p_6.shape[0] - 1, axis=0)
    p_6 = np.delete(p_6, p_6.shape[0] - 1, axis=0)
    up = np.append(up, [p_6], axis=0)

    p_7 = np.delete(nh_p[6], 0, axis=1)
    p_7 = np.delete(p_7, p_7.shape[1] - 1, axis=1)
    p_7 = np.delete(p_7, p_7.shape[0] - 1, axis=0)
    p_7 = np.delete(p_7, p_7.shape[0] - 1, axis=0)
    up = np.append(up, [p_7], axis=0)

    p_8 = np.delete(nh_p[7], nh_p[7].shape[0] - 1, axis=1)
    p_8 = np.delete(p_8, p_8.shape[1] - 1, axis=1)
    p_8 = np.delete(p_8, p_8.shape[0] - 1, axis=0)
    p_8 = np.delete(p_8, p_8.shape[0] - 1, axis=0)
    up = np.append(up, [p_8], axis=0)

    # delete reference shape
    up = np.delete(up, 0, axis=0)
    return up


# create probability matrix
def nh_probmat(nh, b):
    # get height difference
    nh_loc = np.logical_and(nh, nh).astype(int)  # create neighbor locators
    nh_h = np.multiply(np.subtract(b, nh), nh_loc)

    # get depression heights
    nh_h[np.where(nh_h < 0)] = 0

    # # sum of neighbor arrays
    nh_sum = np.sum(nh_h, axis=0)

    # divide depression heights by sum of nh array
    nh_p = np.nan_to_num(np.divide(nh_h, nh_sum), nan=0)

    return nh_p


# from probability matrix and water state, output future state
def state_arr(nh_p, w):
    # filter probabilities with water
    new_state = np.multiply(nh_p, modified_arr(w))

    # remove zeroes from modified
    decomp = restore(new_state, w)

    # random choice
    mod_state = (np.random.random(size=decomp.shape) < decomp).astype(int)

    # flatten state
    state = np.sum(mod_state, axis=0)
    norm_state = np.logical_and(state, state).astype(int)  # change nonzero to 1

    return norm_state


# create inundation identified neighbors given a threshold
def inun_prob(nh, b, thresh):
    # get height differences
    nh_loc = np.logical_and(nh, nh).astype(int)  # create neighbor locators
    nh_h = np.multiply(np.subtract(b, nh), nh_loc)

    # get height difference threshold
    nh_h[np.where(abs(nh_h) > thresh)] = 0

    # surviving heights are inundation neighbors
    in_p = np.logical_and(nh_h, nh_h).astype(int)

    return in_p


# from identified inundation neighbors, identify if sinks align
def inun_state(in_p, sinks):
    # use sinks as state and multiply to inundation nh
    in_st = np.multiply(in_p, modified_arr(sinks))

    # remove zeroes from modified
    in_decomp = restore(in_st, sinks)

    # flatten state
    in_state = np.sum(in_decomp, axis=0)
    norm_in_state = np.logical_and(in_state, in_state).astype(int)  # change nonzero to 1

    return norm_in_state
