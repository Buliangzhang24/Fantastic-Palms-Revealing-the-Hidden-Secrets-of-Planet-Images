#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 09:41:48 2023

@author: lovely_palm_tree
"""
#%% Convert tif to png
import rasterio
from PIL import Image
import functions as funcs

# read the trainning area
UAV_path = "outputclip/DMM_01_trainning area.tif"  
with rasterio.open(UAV_path) as src:
    # read four bands data
    band_1 = src.read(1)
    band_2 = src.read(2)
    band_3 = src.read(3)
    band_4 = src.read(4)

# merge three bands to the RGB image
rgb_image = Image.merge("RGB", (Image.fromarray(band_1), Image.fromarray(band_2), Image.fromarray(band_3)))

# write the png into disk
rgb_image.save('output/DMM_01_trainning area.png')


# read the prediction area 
UAV_path_1 = "outputclip/DMM_01_prediction area.tif"
with rasterio.open(UAV_path_1) as src_1:
    band_1_1 = src_1.read(1)
    band_2_1 = src_1.read(2)
    band_3_1 = src_1.read(3)
    band_4_1 = src_1.read(4)

# merge three bands to the RGB image
rgb_image_1 = Image.merge("RGB", (Image.fromarray(band_1_1), Image.fromarray(band_2_1), Image.fromarray(band_3_1)))

# write the png into disk
rgb_image_1.save('output/DMM_01_prediction area.png')

#%%
# Segement the trainning area tif
import rasterio
with rasterio.open("outputclip/DMM_01_trainning area.tif", driver="GTiff") as src:
    DMM_01_train = src.read()
    DMM_01_train_meta = src.meta

from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor
import numpy as np
import matplotlib.pyplot as plt
import cv2
#.....................Segment Anything Model....................

# from Segment Anything: https://github.com/facebookresearch/segment-anything/blob/main/notebooks/automatic_mask_generator_example.ipynb

# download the checkpoint
import requests

# URL of the file to be downloaded
url = "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth"

# Define the path to save the file
save_path = 'sam_vit_h_4b8939.pth'

# Stream the download and write chunks to the file
with requests.get(url, stream=True) as response:
    response.raise_for_status()  
    with open(save_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):  # 8KB chunks
            file.write(chunk)

sam = sam_model_registry["vit_h"](checkpoint="sam_vit_h_4b8939.pth")

# predict the model
predictor = SamPredictor(sam)

# uses the OpenCV library to read an image in the default BGR  
image = cv2.imread('output/DMM_01_trainning area.png')

# convert BGR in RGB
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

import sys
sys.path.append("..")

# set values for checkpoint and the type of model
sam_checkpoint = "sam_vit_h_4b8939.pth"
model_type = "vit_h"
device = 'cuda'   # if runtime error，change the device to cpu

# define the model and check the model by the checkpoint
sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to(device=device)

# instantiate the SamAutomaticMaskGenerator
mask_generator = SamAutomaticMaskGenerator(sam)

# ..............Segement the training area..............
# create the masks for the image
masks = mask_generator.generate(image)

# plot the outcome of classification
plt.figure(figsize=(20,20))
plt.imshow(image)

# instantiate the show_anns and get_anns
funcs.show_anns(masks)
mask = funcs.get_anns(masks)
mask[:,:,0]

# plot it 
plt.axis('off')
plt.show()

# transform the list into nparrays
classification_mask = funcs.get_anns(masks)
classification_data = classification_mask[:,:,0].astype(np.uint8)

# get the meta data from the training area
meta = DMM_01_train_meta.copy()
meta.update({
    'dtype': 'uint8',
    'count': 1
})

# write the classified image into the disk
with rasterio.open('output/DMM_01_training raster.tif', 'w', **meta) as file:
    file.write(classification_data,1)

# ..............Segement the prediction area.............

with rasterio.open("outputclip/DMM_01_prediction area.tif", driver="GTiff") as src_2:
    DMM_01_predict = src_2.read()
    DMM_01_predict_meta = src_2.meta
    
image_1 = cv2.imread('output/DMM_01_prediction area.png')
image_1 = cv2.cvtColor(image_1, cv2.COLOR_BGR2RGB)

masks_1 = mask_generator.generate(image_1)

# plot the outcome of classification
plt.figure(figsize=(20,20))
plt.imshow(image_1)
funcs.show_anns(masks_1)
mask_1 = funcs.get_anns(masks_1)
mask_1[:,:,0]
plt.axis('off')
plt.show()

# transform the list into ndarrays
classification_mask_1 = funcs.get_anns(masks_1)
classification_data_1 = classification_mask_1[:,:,0].astype(np.uint8)
meta = DMM_01_predict_meta.copy()
meta.update({
    'dtype': 'uint8',
    'count': 1
})

with rasterio.open('output/DMM_01_prediction raster.tif', 'w', **meta) as file:
    file.write(classification_data_1, 1)
