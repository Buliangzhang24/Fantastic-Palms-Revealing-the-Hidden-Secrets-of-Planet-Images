#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 09:03:11 2023

@author: lovely_palm_tree
"""
# Load packages
import functions as funcs
import rasterio as rs
import geopandas as gpd
import pandas as pd
import numpy as np
from osgeo import gdal
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

# Load the data
training_poly = gpd.read_file('output/trainingdata.shp') 
with rs.open('outputclip/DMM_01_trainning area.tif') as dmm_clipped:
     dmm_clipped = dmm_clipped.read()

# Remove unused columns
training_poly = training_poly.loc[:,['Class','geometry']]

# Change Class column to categorical level
training_poly['Class'] = training_poly['Class'].astype('category',copy=False)

# Extract values from tif based on polygons
tif_path = 'outputclip/DMM_01_trainning area.tif'
polygon_path = training_poly 
training_data = funcs.extract_pixel_values_to_dataframe(tif_path, polygon_path)

# Prepare training data
training_data = training_data.loc[:,['band_1','band_2','band_3','band_4','Class']]
training_data['Class'] = training_data['Class'].astype('category')
training_data['Code'] = pd.Categorical(training_data['Class']).codes
training_data = training_data.dropna()
X_train = training_data[['band_1','band_2','band_3','band_4']]
y_train_noseg = np.ravel(training_data[['Code']])

# Create RF model
rf_noseg = RandomForestClassifier()
rf_noseg.fit(X_train, y_train_noseg)

# Prepare the data for prediction
X_pred_rf_noseg = funcs.extract_pixel_values_to_geodataframe('outputclip/DMM_01_prediction area.tif')
X_pred_rf_noseg = X_pred_rf_noseg[['band_1','band_2','band_3','band_4']]

# Predict by RF model
y_pred_rf_noseg = rf_noseg.predict(X_pred_rf_noseg)

# Reshape the prediction result
y_pred_rf_noseg = y_pred_rf_noseg[:, np.newaxis]
with rs.open('outputclip/DMM_01_prediction area.tif') as src:
    array = src.read()
    band,num_rows,num_cols = array.shape
y_pred_rf_noseg = y_pred_rf_noseg.reshape((num_rows, num_cols))

# Convert the prediction result into geotiff
dataset = gdal.Open('outputclip/DMM_01_prediction area.tif', gdal.GA_ReadOnly)
transform = dataset.GetGeoTransform()
crs = dataset.GetProjection()

# Convert the prediction result into geotiff
funcs.array_to_geotiff(y_pred_rf_noseg, 'output/RFprediction_noseg.tif', geotransform=transform, projection=crs)

# Create SVM model
svm_noseg = SVC(kernel='rbf')
svm_noseg.fit(X_train, y_train_noseg)

# Prepare the prediction data
X_pred_svm_noseg = X_pred_rf_noseg

# Predict using SVM model
y_pred_svm_noseg = svm_noseg.predict(X_pred_svm_noseg)

# Reshape the prediction result
y_pred_svm_noseg = y_pred_svm_noseg[:, np.newaxis]

# Reshape the variable to match the dimensions of the tiff file
with rs.open('outputclip/DMM_01_prediction area.tif') as src:
    array = src.read()
    band,num_rows,num_cols = array.shape
y_pred_svm_noseg = y_pred_svm_noseg.reshape((num_rows, num_cols))

# Convert the prediction result into geotiff
funcs.array_to_geotiff(y_pred_svm_noseg, 'output/SVMprediction_noseg.tif', geotransform=transform, projection=crs)

