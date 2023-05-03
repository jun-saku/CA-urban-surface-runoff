"""
imggifseq.py - Documentation

before running this python file to create image sequence,
please create a path "sequence/" and insert the water state folder
"feats/.../water_img/" from "feats/" and inundation state folder "inun_img/" in the "inun"
folder from "roi-#/inun_img/".

the PNG files are saved in the png folder

"""

import glob
from PIL import Image as im
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import itaverage as itv
import geotiffio as tio

inun_iter = 20
water_iter = 25
n = 0
# enter folder name where water_img and inun_img is saved in sequence
roi = "roi-8"

tio.chk_dir("sequence")
seq_dir = "sequence/" + roi
tio.chk_dir(seq_dir)

# add smooth trace output to water iteration
while n < water_iter:
    path_n = seq_dir + "/water_img/" + str(n) + ".tif"
    trace_path = "run_avg/" + roi + "-avg.tif"
    water_n, tiff_info_water = tio.read_geotiff(path_n)
    trace, tiff_info_trace = tio.read_geotiff(trace_path)

    # add smooth trace path as background for water states
    trace[np.where(water_n > 0)] = water_iter

    # save sequence to tiffs folder
    path4 = tio.create_dir(n, 'tiff', seq_dir)
    tio.write_geotiff(path4, trace, tiff_info_trace)
    print(n)
    n += 1

# add smooth trace output to water iteration
c = 0
while c < inun_iter:
    path_c = seq_dir + "/inun_img/" + str(c) + ".tif"
    trace_path = "run_avg/" + roi + "-avg.tif"
    inun_n, tiff_info_inun = tio.read_geotiff(path_c)
    trace, tiff_info_trace = tio.read_geotiff(trace_path)

    # add smooth trace path as background for water states
    trace[np.where(inun_n > 0)] = water_iter

    # save sequence to tiffs folder
    n_c = n + c
    path4 = tio.create_dir(n_c, 'tiff', seq_dir)
    tio.write_geotiff(path4, trace, tiff_info_trace)
    print(n_c)
    c += 1

t = 0
while t <= n_c:
    path_im = "sequence/" + roi + "/tiff/" + str(t) + ".tif"
    im_seq, tiff_info_im = tio.read_geotiff(path_im)
    png_path = "sequence/" + roi + "/png"
    tio.chk_dir(png_path)
    path_seq = png_path + "/" + str(t+1) + ".png"
    if t < 10:
        path_seq = png_path + "/0" + str(t+1) + ".png"
    mpl.image.imsave(path_seq, im_seq, cmap='gray')
    print(t)
    t += 1


def make_gif(frame_folder):
    frames = [im.open(image) for image in glob.glob(f"sequence/roi-8/png/*.png")]
    frame_one = frames[0]
    frame_one.save("sequence/path_evolution_roi-8-feats.gif", format="GIF", append_images=frames,
                   save_all=True, duration=100, loop=0)

if __name__ == "__main__":
    make_gif("/path/to/images")


