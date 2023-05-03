"""
geotiffio.py - Documentation

Required modules:
- gdal
- datetime
- numpy
- os

This file contains the input and output methods for GeoTIFF files and
for directory creation and management.

* read_geotiff
- imports the GeoTIFF file and outputs the raster data values as a numpy
array for calculation and the  projections and geo transform info for
geo referencing which will be used for exporting GeoTIFF files
of the same area.

* write_geotiff
- uses a numpy array and tiff info from read_geotiff to export a GeoTIFF
file.

* create_dir
- creates a directory if the existing path does not exist. Uses n for file
name

* folder_dir
- creates separate folders based on time and date for run iterations

* chk_dir
- check if directory exists, otherwise create the directory

"""

from osgeo import gdal
import numpy as np
from datetime import datetime
import os


# read and write to GeoTIFF file
def read_geotiff(filename):
    ds = gdal.Open(filename)
    band = ds.GetRasterBand(1)
    arr = band.ReadAsArray()
    return arr, ds


def write_geotiff(filename, arr, in_ds):
    if arr.dtype == np.float32:
        arr_type = gdal.GDT_Float32
    else:
        arr_type = gdal.GDT_Int32

    driver = gdal.GetDriverByName("GTiff")
    out_ds = driver.Create(filename, arr.shape[1], arr.shape[0], 1, arr_type)
    out_ds.SetProjection(in_ds.GetProjection())
    out_ds.SetGeoTransform(in_ds.GetGeoTransform())
    band = out_ds.GetRasterBand(1)
    band.WriteArray(arr)
    band.FlushCache()
    band.ComputeStatistics(False)


# save file
def create_dir(n, path, main_dir):
    f_dir = main_dir + '/' + path
    if not os.path.exists(f_dir):
        os.makedirs(f_dir)
    file_path = f_dir + '/' + str(n) + '.tif'
    return file_path


def folder_dir(h_dir):
    time_stamp = datetime.now()
    run_dir = h_dir + '/' + time_stamp.strftime('%m-%d-%Y_%H-%M-%S')
    if not os.path.exists(run_dir):
        os.makedirs(run_dir)
    return run_dir


def chk_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    return
