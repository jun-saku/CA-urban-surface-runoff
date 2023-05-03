import itaverage as itv
import caflowrun as cfr

roi = "roi-8"

# only run once (takes time)
dsm_path = 'tiff_data/' + roi + '-dsm.tif'
itv.ca_run_n(dsm_path, roi, 10, 25)
itv.run_avg(roi, 10)

# create mask from averaged
mask_arr = itv.ca_mask(roi, 0.7)
mask_dsm = itv.mask_morph(mask_arr)

# combine dsm and dem to create feature
itv.int_dsm_dem(roi, mask_dsm)

# Create smoothed output from integrated elevation model
roi_feat = roi + '-feats'
dsm_path = 'feats/' + roi_feat + '.tif'
itv.ca_run_n(dsm_path, roi_feat, 10, 25)
itv.run_avg(roi_feat, 10)

# from here, run inundsink.py to create inundation areas
