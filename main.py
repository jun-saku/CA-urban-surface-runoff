"""
Python 3.6

Required modules:
- numpy
- time (for runtime measurement)
- geotiffio (external python file)
- transfunc (external python file)

Reads from a geotiff file and traces the surface runoff from the elevation data
Outputs sequences of geotiff files for an n number of iteration for water and trace
data and saves them in the 'runs/' directory.

"""

import numpy as np
import time

import geotiffio as tio
import transfunc as tf

# start timer
st = time.time()

# read elevation levels and geo info
elev, tiff_info = tio.read_geotiff("feats/roi-8-feats.tif")
iterations = 25

# remove error data (negative value)
elev[np.where(elev < 0)] = 0

# initialize water array
water = np.ones(elev.shape)
tracer = np.zeros(elev.shape)
water_arr = np.array([water])
tracer_arr = np.array([tracer])

# create neighborhood arrays
elev_mod = tf.modified_arr(elev)
nh_mod = tf.nh_3darr(elev, elev_mod)
nh_prob = tf.nh_probmat(nh_mod, elev_mod)

# folder directory
run_dir = tio.folder_dir('runs')

# loop
n = 0
while n < iterations:
    water = tf.state_arr(nh_prob, water)
    tracer += water
    path1 = tio.create_dir(n, 'water_img', run_dir)
    path2 = tio.create_dir(n, 'tracer_img', run_dir)
    tio.write_geotiff(path1, water, tiff_info)
    tio.write_geotiff(path2, tracer, tiff_info)
    print(n)
    n += 1

# end timer
et = time.time()
elapsed_time = et - st
print('Execution time:', elapsed_time, 'seconds')

print(tracer)