"""
itaverage.py - Documentation

Required modules:
- numpy
- geotiffio (external python file)
- transfunc (external python file)
- matplotlib.pyplot
- matplotlib
- cv2

Note: matplotlib.pyplot must be imported before matplotlib
      even if it is unused
    -> due to errors from matplotlib.image.imsave

Contains methods for extracting urban features from DSM data.

* ca_run_n
- similar to main.py; runs the CA flow algorithm for a specified number of
iterations and saves them to a directory

* run_avg
- from the run sequence created from ca_run_n, the average of all iterations
is taken to produce a smooth gradient of values.

* ca_mask
- from the smooth CA flow output from run_avg, a binary mask is created.
takes a threshold value for the slope mask (in percentage (0-1)).

* mask_morph
- image processing method. includes specified erode and dilate processes.
subject to edits depending on the input data.

* int_dsm_dem
- from the mask produced in mask_morph, the DSM and DEM data are integrated.
The positive mask takes the values of the DSM and the negative mask takes the DEM
these are then added together and exported.

"""

import numpy as np
import os
import geotiffio as tio
import transfunc as tf
import matplotlib.pyplot as plt
import matplotlib as mpl
import cv2


# run CA algorithm at multiple iterations
def ca_run_n(filename, f_name, runs_n, iters):
    # read elevation levels and geo info
    elev, tiff_info = tio.read_geotiff(filename)

    # remove error data (negative value)
    elev[np.where(elev < 0)] = 0

    # start smoothen iterations
    for run_c in range(runs_n):
        # initialize water array
        water = np.ones(elev.shape)
        tracer = np.zeros(elev.shape)

        # create neighborhood arrays
        elev_mod = tf.modified_arr(elev)
        nh_mod = tf.nh_3darr(elev, elev_mod)
        nh_prob = tf.nh_probmat(nh_mod, elev_mod)

        # folder directory
        run_dir = f_name + '/' + str(run_c)
        tio.chk_dir(run_dir)

        # loop
        n_it = 0
        while n_it < iters:
            water = tf.state_arr(nh_prob, water)
            tracer += water
            path1 = tio.create_dir(n_it, 'water_img', run_dir)
            path2 = tio.create_dir(n_it, 'tracer_img', run_dir)
            tio.write_geotiff(path1, water, tiff_info)
            tio.write_geotiff(path2, tracer, tiff_info)
            print('CA flow iter-' + str(run_c + 1) + '/' + str(runs_n) + ' run-' + str(n_it + 1) + '/' + str(iters))
            n_it += 1
    print('-> Run CA algorithm for ' + str(runs_n) + ' iterations. -/')
    return


# smoothen results average
def run_avg(f_name, runs_n):
    state_tot = 0
    tiff_info_n = 0
    for f_n in range(runs_n):
        run_path = f_name + '/' + str(f_n) + '/tracer_img/24.tif'
        state_n, tiff_info_n = tio.read_geotiff(run_path)
        state_tot += state_n
    state_avg = state_tot / runs_n
    avg_dir = 'run_avg'
    tio.chk_dir(avg_dir)
    avg_dir = avg_dir + '/' + f_name + '-avg.tif'
    tio.write_geotiff(avg_dir, state_avg, tiff_info_n)
    print('-> Smoothened CA output from iterations. -/')
    return


# create raster mask from averaged CA output
def ca_mask(f_name, perc_thresh):
    # import averaged CA output
    avg_dir = 'run_avg/' + f_name + '-avg.tif'
    state_avg, tiff_info_avg = tio.read_geotiff(avg_dir)

    # set threshold for binary image
    state_avg[np.where(state_avg >= 1)] = 1
    state_avg[np.where(state_avg < 1)] = 0

    # import slope data
    slope_dir = 'tiff_data/' + f_name + '-dsm-slope.tif'
    slope, tiff_info_m = tio.read_geotiff(slope_dir)

    # set threshold and convert to binary values
    max_sl_val = np.amax(slope)
    sl_thresh = max_sl_val * perc_thresh
    slope[np.where(slope < 0)] = 0
    slope[np.where(slope > sl_thresh)] = 0
    slope_mask = np.logical_and(slope, slope).astype(int)

    # convert combined slope and ca data to binary
    ca_sl = np.logical_and(slope_mask, state_avg).astype(int)

    print('-> CA mask created. -/')
    return ca_sl


def mask_morph(mask_np):
    # save array as png for image processing
    tio.chk_dir('temp')
    mpl.image.imsave('temp/dummy.png', mask_np, cmap='gray')
    mask_img = cv2.imread('temp/dummy.png', 0)

    # erode and dilate
    kernel = np.ones((3, 3), np.uint8)
    e1 = cv2.erode(mask_img, kernel, iterations=1)
    d1 = cv2.dilate(e1, kernel, iterations=3)
    e2 = cv2.erode(d1, kernel, iterations=2)

    # open and close
    kernel2 = np.ones((5, 5), np.uint8)
    o1 = cv2.morphologyEx(e2, cv2.MORPH_OPEN, kernel2)
    c1 = cv2.morphologyEx(o1, cv2.MORPH_CLOSE, kernel2)

    # convert png to array and normalize (0,255) -> (0,1)
    arr = np.asarray(c1)
    mask_dsm = np.logical_and(arr, arr).astype(float)

    print('-> Morphological Image Processing for CA & slope mask. -/')
    return mask_dsm


# combine DSM and DEM using CA mask
def int_dsm_dem(f_name, mask_dsm):
    # create invert mask for dem
    mask_dem = 1 - mask_dsm

    # import dem and dsm data
    dem_dir = 'tiff_data/' + f_name + '-dem.tif'
    dsm_dir = 'tiff_data/' + f_name + '-dsm.tif'
    dem, tiff_info_dem = tio.read_geotiff(dem_dir)
    dsm, tiff_info_dsm = tio.read_geotiff(dsm_dir)

    # multiply mask to obtain data
    masked_dsm = np.multiply(dsm, mask_dsm, dtype='float32')
    masked_dem = np.multiply(dem, mask_dem, dtype='float32')

    # add masked dem and dsk
    feats = masked_dsm + masked_dem

    # save as tif
    tio.chk_dir('feats')
    feats_dir = 'feats/' + f_name + '-feats.tif'
    tio.write_geotiff(feats_dir, feats, tiff_info_dsm)

    print('-> Integrated DSM and DEM. -/')
    return
