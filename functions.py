#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 06:34:14 2023

@author: lovely_palm_tree
"""

def show_anns(anns):
    '''Create an image and uses different colors to mark different objects within the annotations'''
    # Load necessary package
    import matplotlib.pyplot as plt
    import numpy as np
    
    if len(anns) == 0:
        return
    sorted_anns = sorted(anns, key=(lambda x: x['area']), reverse=True)
    ax = plt.gca()
    ax.set_autoscale_on(False)

    img = np.ones((sorted_anns[0]['segmentation'].shape[0], sorted_anns[0]['segmentation'].shape[1], 4))
    img[:,:,3] = 0
    for ann in sorted_anns:
        m = ann['segmentation']
        color_mask = np.concatenate([np.random.random(3), [0.35]])
        img[m] = color_mask
    ax.imshow(img)


def get_anns(anns):
    '''similar to the show_anns but it returns the image containing annotation information.'''
    # Load necessary package
    import matplotlib.pyplot as plt
    import numpy as np
    
    if len(anns) == 0:
        return
    sorted_anns = sorted(anns, key=(lambda x: x['area']), reverse=True) # maybe sort by stability_score
    ax = plt.gca()
    ax.set_autoscale_on(False)

    img = np.ones((sorted_anns[0]['segmentation'].shape[0], sorted_anns[0]['segmentation'].shape[1], 4))
    img[:,:,3] = 0
    for i in range(0, len(sorted_anns)):
        ann = sorted_anns[i]
        m = ann['segmentation']
        color_mask = np.concatenate([[i, i, i], [0.35]])
        img[m] = color_mask
    return(img)




def raster_to_vector(input_raster, output_vector):
    '''It uses the GDAL and OGR libraries to perform the conversion of the raster data into vector data.'''
    # Load necessary package
    from osgeo import gdal, ogr
    
    # Open the input raster
    src_ds = gdal.Open(input_raster)
    srcband = src_ds.GetRasterBand(1)
    
    # Define the layer name for the output vector data
    dst_layername = "POLYGONIZED_STUFF"
    
    # Create an ESRI Shapefile driver
    drv = ogr.GetDriverByName("ESRI Shapefile")
    
    # Create a new data source and layer for the vector data
    dst_ds = drv.CreateDataSource(output_vector)
    dst_layer = dst_ds.CreateLayer(dst_layername, srs=None)
    
    # Perform the polygonization of the raster data
    gdal.Polygonize(srcband, None, dst_layer, -1, [], callback=None)
    
    # Close and release resources
    src_ds = None
    dst_ds = None
    
    
def crop_using_smaller_tiff(large_tif_path, small_tif_path, output_path):
    """This function crops a large TIFF image using the extent of a smaller TIFF image and saves the cropped portion."""
    # Load necessary package
    import rasterio
    from rasterio.mask import mask
    
    # Open the smaller TIFF and get its bounds
    with rasterio.open(small_tif_path) as small_tif:
        small_tif_bounds = small_tif.bounds
        # Convert the bounds of the smaller TIFF to a geometry (used for masking)
        geom = [{
            'type': 'Polygon',
            'coordinates': [[
                [small_tif_bounds.left, small_tif_bounds.bottom],
                [small_tif_bounds.left, small_tif_bounds.top],
                [small_tif_bounds.right, small_tif_bounds.top],
                [small_tif_bounds.right, small_tif_bounds.bottom]
            ]]
        }]

    # Open the larger TIFF and crop it using the geometry of the smaller TIFF
    with rasterio.open(large_tif_path) as large_tif:
        out_image, out_transform = mask(large_tif, geom, crop=True)
        out_meta = large_tif.meta.copy()

        # Update metadata to reflect the new size
        out_meta.update({
            "driver": "GTiff",
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform
        })

        # Write the cropped image to the output path
        with rasterio.open(output_path, "w", **out_meta) as file:
            file.write(out_image)


def extract_pixel_values_to_dataframe(tif_path, polygon_path):
    '''This function extracts pixel values from a TIFF image for specified polygons and stores them in a pandas DataFrame.'''
    # Load necessary package
    import rasterio
    
    # load TIFF
    with rasterio.open(tif_path) as src:
        # load polygon data
        gdf = polygon_path
        
        # Initialize 4 empty lists to store all pixel values
        gdf['band_1'] = None
        gdf['band_2'] = None
        gdf['band_3'] = None
        gdf['band_4'] = None
        
        # Iterate over each polygon
        for idx, geometry in gdf.iterrows():
           # Extracting pixel values using polygons
           for band in range(1, 5):
               out_image = src.read(band, window=src.window(*geometry.geometry.bounds))
               gdf.at[idx, f'band_{band}'] = out_image[0][0]
    return gdf


def extract_pixel_values_to_geodataframe(tif_path):
    '''This function extracts pixel values from a TIFF image and stores them in a geopandas DataFrame.'''
    # Load necessary package
    import geopandas as gpd
    import rasterio as rs
    import pandas as pd
    from shapely.geometry import box
    
    # Reading TIFF files with rasterio
    with rs.open(tif_path) as src:
        array = src.read()
        
    # Convert the resulting pixel values to pandas DataFrame
    if array.shape[0] == 1:
        df = pd.DataFrame(array[0].ravel(), columns=['band_1'])
    else: 
        df = pd.DataFrame({f'band_{band+1}': array[band].ravel() for band in range(array.shape[0])})
        
    # Create GeoDataFrame with geometry information
    bounds = src.bounds
    num_pixels = len(df)
    
    # Match the length of the data by repeating the geometry information
    geometry = [box(*bounds)] * num_pixels
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs=src.crs)
    
    return gdf


def array_to_geotiff(data, output_file, geotransform=(0, 1, 0, 0, 0, 1), projection=None):
    '''This function converts a NumPy array containing data into a GeoTIFF file.'''
    # Load necessary package
    from osgeo import gdal
    
    # Extract the number of rows and cols of the data
    rows, cols = data.shape
    
    # Create a GDAL GeoTIFF driver
    driver = gdal.GetDriverByName("GTiff")
    
    # Create a new GeoTIFF dataset
    dataset = driver.Create(output_file, cols, rows, 1, gdal.GDT_Float32)
    
    # Write the input data array to the GeoTIFF's first band
    dataset.GetRasterBand(1).WriteArray(data)
    
    # Set the geotransformation parameters
    dataset.SetGeoTransform(geotransform)
    
    # Set the optional projection information if provided
    if projection:
        dataset.SetProjection(projection)

    dataset = None
