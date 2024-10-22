#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 11:17:49 2023

@author: osboxes
"""
#%% clip the trainning area
# Load necessary package
import geopandas as gpd
import rasterio
from rasterio.mask import mask
from shapely.geometry import box
import functions as funcs

# read the polygon of Mflexuosa
vector_file = 'data/DMM-01/Ground data/Mflexuosa_DMM01_2019.shp'
gdf = gpd.read_file(vector_file)

# get the extent of image
bounds = gdf.total_bounds
bbox_polygon = box(*bounds)

# read the UAV image 
with rasterio.open('data/DMM-01/UAV/DMM-01_10_res.tif') as src:
    out_image, out_transform = mask(src, [bbox_polygon], crop=True)
    out_meta = src.meta.copy()

# update the meta    
out_meta.update({
    "driver": "GTiff",
    "height": out_image.shape[1],
    "width": out_image.shape[2],
    "transform": out_transform
})

# write the training area into disk
with rasterio.open('outputclip/DMM_01_trainning area.tif', 'w', **out_meta) as file:
    file.write(out_image)

# clip the study area (prediction area)
funcs.crop_using_smaller_tiff('data/DMM-01/UAV/DMM-01_10_res.tif', 'data/DMM-01/Ground data/DMM01_6_7_8_9_res.tif', 'outputclip/DMM_01_prediction area.tif')


