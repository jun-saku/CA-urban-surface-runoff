import numpy as np

import geotiffio as tio
import transfunc as tf
import matplotlib.pyplot as plt
import matplotlib as mpl

# change this variable to the specified region of interest
roi = "roi-8"

# import feature, trace, and sink data
feats_path = "feats/" + roi + "-feats.tif"
trace_path = "run_avg/" + roi + "-avg.tif"
water_path = roi + "-feats/0/water_img/20.tif"
feats, tiff_info_feats = tio.read_geotiff(feats_path)
trace, tiff_info_trace = tio.read_geotiff(trace_path)
sinks, tiff_info_sinks = tio.read_geotiff(water_path)

# calculate inundation neighbors
feats_mod = tf.modified_arr(feats)
nh_mod = tf.nh_3darr(feats, feats_mod)
in_p = tf.inun_prob(nh_mod, feats_mod, 0.1)

# folder directory
inun_path = roi + "-feats/inun_img"
tio.chk_dir(inun_path)

# loop
n = 0
iters = 20
while n < iters:
    sinks = tf.inun_state(in_p, sinks)
    # path3 = tio.create_dir(n, 'inun_img', run_dir)
    path3 = roi + "-feats/inun_img/" + str(n) + ".tif"
    tio.write_geotiff(path3, sinks, tiff_info_sinks)
    print('Inundation run - ' + str(n + 1) + '/' + str(iters))
    n += 1

# export inundation data
tio.chk_dir("inun")
in_dir = 'inun/' + roi + '-inun.tif'
tio.write_geotiff(in_dir, sinks, tiff_info_sinks)

# combine sink and trace data
inv_sink = 1 - sinks
masked_trace = np.multiply(trace, inv_sink)
final = masked_trace + (sinks*25)     # max iter = 25

tio.chk_dir('output')
output_path = 'output/' + roi + '-feats-flow-final'
png_path = 'output/' + roi + '-feats-flow-final.png'
tio.write_geotiff(output_path, final, tiff_info_sinks)
mpl.image.imsave(png_path, final, cmap='gray')

