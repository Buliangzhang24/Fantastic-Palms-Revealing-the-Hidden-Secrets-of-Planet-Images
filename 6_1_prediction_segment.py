#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 09:03:11 2023

@author: lovely_palm_tree
"""
# Load packages
import functions as funcs
import rasterio
import geopandas as gpd
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import fiona
from shapely.geometry import mapping

# Load the data
training_poly = gpd.read_file('output/trainingdata.shp') 
with rasterio.open('outputclip/DMM_01_trainning area.tif') as dmm_clipped:
     dmm_clipped = dmm_clipped.read()
     
with rasterio.open("outputclip/DMM_01_prediction area.tif", driver="GTiff") as src:
    prediction_area = src.read()
    prediction_area_meta = src.meta

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
y_train_seg = training_data[['Code']]

# Create RF model
rf_seg = RandomForestClassifier()
rf_seg.fit(X_train, y_train_seg)

# Prepare the data for prediction
tif_path = 'outputclip/DMM_01_prediction area.tif'
polygon_path = gpd.read_file('output/DMM_01_prediction_vector.shp')
X_pred_rf_seg = funcs.extract_pixel_values_to_dataframe(tif_path, polygon_path)
X_pred_rf_seg = X_pred_rf_seg[['band_1','band_2','band_3','band_4']]

# Predict by RF model
y_pred_rf_seg = rf_seg.predict(X_pred_rf_seg)
y_pred_rf_seg = y_pred_rf_seg[:, np.newaxis]
y_pred_rf_seg = pd.DataFrame(y_pred_rf_seg)
y_pred_rf_seg.rename(columns={y_pred_rf_seg.columns[0]: 'Class'}, inplace=True)
y_pred_rf_seg['geometry'] = polygon_path['geometry']
y_pred_rf_seg = gpd.GeoDataFrame(y_pred_rf_seg, geometry='geometry')

# Save prediction result
meta = prediction_area_meta.copy()
schema = {
    'geometry': y_pred_rf_seg.geometry.type.iloc[0],  
    'properties': {col: 'str' for col in y_pred_rf_seg.columns if col != 'geometry'}
}

# Remove 'driver' from meta if it exists
if 'driver' in meta:
    del meta['driver']

with fiona.open("output/RFprediction_seg.gpkg", "w", 
                driver="GPKG", 
                schema=schema, 
                **meta) as dst:
    for _, row in y_pred_rf_seg.iterrows():
        dst.write({
            'geometry': mapping(row['geometry']),
            'properties': {k: v for k, v in row.items() if k != 'geometry'}
        })


# Create SVM model
svm_seg = SVC(kernel='rbf')
svm_seg.fit(X_train, y_train_seg)

# Prepare the prediction data
X_pred_svm_seg = X_pred_rf_seg

# Predict using SVM model
y_pred_svm_seg = svm_seg.predict(X_pred_svm_seg)

# Reshape the prediction result
y_pred_svm_seg = y_pred_svm_seg[:, np.newaxis]
y_pred_svm_seg = pd.DataFrame(y_pred_svm_seg)
y_pred_svm_seg.rename(columns={y_pred_svm_seg.columns[0]: 'Class'}, inplace=True)
y_pred_svm_seg['geometry'] = polygon_path['geometry']
y_pred_svm_seg = gpd.GeoDataFrame(y_pred_svm_seg, geometry='geometry')

# Save prediction result
meta = prediction_area_meta.copy()
schema = {
    'geometry': y_pred_svm_seg.geometry.type.iloc[0],  
    'properties': {col: 'str' for col in y_pred_svm_seg.columns if col != 'geometry'}  
}

# Remove 'driver' from meta if it exists
if 'driver' in meta:
    del meta['driver']

with fiona.open("output/SVMprediction_seg.gpkg", "w", 
                driver="GPKG", 
                schema=schema, 
                **meta) as dst:
    for _, row in y_pred_svm_seg.iterrows():
        dst.write({
            'geometry': mapping(row['geometry']),
            'properties': {k: v for k, v in row.items() if k != 'geometry'}
        })
