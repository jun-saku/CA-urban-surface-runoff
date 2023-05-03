import numpy as np

import geotiffio as tio
import transfunc as tf
import matplotlib.pyplot as plt
import matplotlib as mpl

roi = "roi-7"

# import smooth trace output and saga flow output for comparison
trace_path = "run_avg/" + roi + "-feats-avg.tif"
saga_path = "tiff_data/" + roi + "-saga-flow.tif"
trace, tiff_info_trace = tio.read_geotiff(trace_path)
saga, tiff_info_saga = tio.read_geotiff(saga_path)

# save png images of both for visual comparison
pn_path = 'output/' + roi + '-trace-output.png'
mpl.image.imsave(pn_path, trace, cmap='gray')
saga_norm = saga
saga_norm[np.where(saga_norm >= 25)] = 25
png_path = 'output/' + roi + '-saga-flow.png'
mpl.image.imsave(png_path, saga_norm, cmap='gray')



# set threshold for binary image (no flow trace values)
trace[np.where(trace < 1)] = 0
trace[np.where(trace >= 1)] = 1
saga[np.where(saga <= 1)] = 0
saga[np.where(saga > 1)] = 1

# compute difference in coverage percentage
dim = trace.shape[0]*trace.shape[1]    # number of cells
blank = np.ones(trace.shape)
diff_saga = blank - saga
diff_trace = blank - trace
diff = abs(np.sum(saga) - np.sum(trace))
print("---------- COVERAGE DIFFERENCE ----------")
print("Trace Output")
print("--> Covered Points:", (np.sum(trace)/dim)*100, "%")
print("--> Uncovered Points:", (np.sum(diff_trace)/dim)*100, "%")
print("SAGA Output")
print("--> Covered Points:", (np.sum(saga)/dim)*100, "%")
print("--> Uncovered Points:", (np.sum(diff_saga)/dim)*100, "%")
print("Coverage Difference:", (diff/dim)*100, "%")
print("-----------------------------------------")
print("")

# path difference calculation
diff = trace - saga
pos_count = np.count_nonzero(diff == 1)
neg_count = np.count_nonzero(diff == -1)
diff_count = np.sum(abs(diff))
print("------------ PATH DIFFERENCE ------------")
print("Type I error:", (pos_count/dim)*100, "%")
print("Type II error:", (neg_count/dim)*100, "%")
print("Difference Points:", (diff_count/dim)*100, "%")
print("-----------------------------------------")

# histogram of saga flow output
# y = np.histogram(saga, bins=10000, range=(1, 25))[0]
# x = np.linspace(1, 25, 10000)
# plt.plot(x, y)
# plt.show()


