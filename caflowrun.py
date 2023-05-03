"""
caflowrun.py - Documentation

the most vanilla form of CA run.
This is used for post processing (run for combined dsm dem)
in urbanfeat.py

main.py in method form

"""

import numpy as np
import sys

import geotiffio as tio
import transfunc as tf


def ca_flow_run(folder_name, f_name, iters):
    # initialize directory of file to run CA flow algorithm
    run_dir = folder_name + '/' + f_name + '.tif'

    # read elevation levels and geo info
    elev, tiff_info = tio.read_geotiff(run_dir)

    # remove error data (negative value)
    elev[np.where(elev < 0)] = 0

    # initialize water array
    water = np.ones(elev.shape)
    tracer = np.zeros(elev.shape)

    # create neighborhood arrays
    elev_mod = tf.modified_arr(elev)
    nh_mod = tf.nh_3darr(elev, elev_mod)
    nh_prob = tf.nh_probmat(nh_mod, elev_mod)

    # folder directory
    run_dir = tio.folder_dir(folder_name)

    # loop
    n = 0
    while n < iters:
        water = tf.state_arr(nh_prob, water)
        tracer += water
        path1 = tio.create_dir(n, 'water_img', run_dir)
        path2 = tio.create_dir(n, 'tracer_img', run_dir)
        tio.write_geotiff(path1, water, tiff_info)
        tio.write_geotiff(path2, tracer, tiff_info)
        print('CA Flow run - ' + str(n + 1) + '/' + str(iters))
        n += 1

    print('-> CA flow run complete. -/')
    return
