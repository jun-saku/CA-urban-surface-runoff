# CA-urban-surface-runoff
Urban surface runoff modeling using cellular automata
Urban Surface Runoff Modeling using Cellular Automata Approach

Program Documentation

-----------------------------------------------------------------------------
Program run on Python 3.6 

Packages required for install
- numpy
- os
- matplotlib
- pygdal
- cv2

Note: 
When using Anaconda Navigator, create a new environment using Python 3.6 to 
install pygdal from osgeo. Newer versions of Python has path issues in anaconda
when installing pygdal. This however limits the use of Image Processing modules.
The newer skimage module for morphology processes has compatibility issues with
Python 3.6. Thus, cv2 (OpenCV) is used for image processing.
---------------------------------------------------------------------------------
Python Files:

* main.py
- This contains the basic algorithm of the surface runoff modeling using CA. 

* geotiffio.py
- This contains methods used in file handling and the import and export of GeoTIFF
files. Credits to ... for the file handling for GeoTIFF files.

* transfunc.py
- This contains the methods used for the transition function. The transition function
optimization using numpy matrix operations is declared in this file. The inundation 
methods are also included.

* itaverage.py
- This contains the methods for smoothing the CA run due to the probabilistic methods.

* urbanfeat.py
- this contains the run program for identifying urban features from a DSM.

* caflowrun.py
- This contains the basic CA program in method form. This is used in mapping the final 
output from the integrated dsm and dem. 

* inundsink.py
- This contains the inundation program and the combination of trace output and the 
inundation output.
------------------------------------------------------------------------------------------------
How to use?

1. Create a folder named 'tiff_data' and include the following
	-> DEM GeoTIFF data
	-> DSM GeoTIFF data
	-> Slope data from DSM in GeoTIFF format

2. Change the file name and/or path accordingly in the python files and RUN!











