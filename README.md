# Geoscripting project repository

- Title: Fantastic Palms: The Secret Hidden in Planet Images
- Team name： lovely palm trees
- Challenge number: 10

# Research Question
**Mauritia flexuosa Extraction in Aguajales**
This model is designed to extract Mauritia flexuosa in the aguajales training region and predict its density and distribution in the prediction area.

## Steps to Achieve the Objective

### 1. Data Retrieval
Download and extract the raw data.

### 2. Data Preparation
Clip the data to define the training and prediction areas.

### 3. Object Segmentation
Utilize the [segment-anything](https://github.com/facebookresearch/segment-anything) model to generate masks for all objects in the UAV image for both the training and prediction areas.

### 4. Raster-to-Vector Conversion
Convert the raster images into vector format.

### 5. Classification in Training Area
Classify and label all the polygons in the training area to prepare for the subsequent prediction step.

### 6. Prediction
Based on whether the segmentation from step 3 was performed:
- **Based on Pixel**: Utilize SVM (Support Vector Machine) and RF (Random Forest) for modeling and prediction.
- **Based on Object**: Similarly, utilize SVM and RF for modeling and prediction.

### 7. Visualization
Visualize the extracted and predicted Mauritia flexuosa density and distribution in both training and prediction areas.

## Notes
Ensure that the appropriate libraries and dependencies for the above tools (like segment-anything, SVM, RF) are installed and set up correctly.

# Result
![Random Forest Prediction Pixel](https://git.wur.nl/geoscripting-2023-september/staff/project/Project_Starter-lovely_palm_trees/-/raw/main/Random_Forest_Prediction_pixel.png)

![SVM Prediction Pixel](https://git.wur.nl/geoscripting-2023-september/staff/project/Project_Starter-lovely_palm_trees/-/raw/main/SVMPrediction_pixel.png)

![RF Prediction Object](https://git.wur.nl/geoscripting-2023-september/staff/project/Project_Starter-lovely_palm_trees/-/raw/main/RF_prediction_object.png)

![SVM Prediction Object](https://git.wur.nl/geoscripting-2023-september/staff/project/Project_Starter-lovely_palm_trees/-/raw/main/SVM_prediction_object.png)

# Testing

## To set up the project environment, create a virtual environment based on `finalproject.yaml`. Then installation dependencies: 
```
mamba env create --file finalproject.yaml
source activate finalproject
```
## execute the program
```
./main.sh
```

# Packages Usage

## Python Dependencies

- **Download and extract modified_1**: 
  - os
  - requests
  - zipfile

- **Clip_modified_2**: 
  - geopandas
  - rasterio
  - shapley

- **Segment_modified_3**: 
  - pillow
  - segment_anything
  - numpy
  - matplotlib
  - requests
  - opencv-python

- **Vectorize_modified_4**: 
  - gdal
  - ogr

## R Dependencies

- **Set_label_5**: 
  - raster
  - terra
  - sf
  - ranger
  - dplyr

- **Model_of_prediction_6 (Python)**: 
  - sklearn

- **Visualization_leaflet_7**: 
  - leaflet
  - png
  - sp

# License
The code is licensed under the MIT License.

# Contributors
- Xinyi He
- Xiaoyu Yang
- Dong Liang
- Qin Xu


