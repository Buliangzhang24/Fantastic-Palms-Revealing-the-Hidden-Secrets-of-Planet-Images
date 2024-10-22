#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 09:41:48 2023

@author: lovely_palm_tree
"""
#%%
# vectorize the raster
# Load necessary package
import functions as funcs

# instantiate the raster_to_vector function 
funcs.raster_to_vector("output/DMM_01_training raster.tif", "output/DMM_01_training_vector.shp")
funcs.raster_to_vector("output/DMM_01_prediction raster.tif", "output/DMM_01_prediction_vector.shp")
