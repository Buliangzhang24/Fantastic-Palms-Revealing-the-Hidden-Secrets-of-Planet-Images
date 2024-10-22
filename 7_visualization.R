# download the package for visualization
if(!"leaflet" %in% installed.packages()){install.packages("leaflet")}
if(!"terra" %in% installed.packages()){install.packages("terra")}
if(!"raster" %in% installed.packages()){install.packages("raster")}
if(!"sp" %in% installed.packages()){install.packages("sp")}
if(!"sf" %in% installed.packages()){install.packages("sf")}

library(sp)
library(sf)
library(leaflet)
library(terra)
library(raster)
library(png)

#....................RFrediction.tif.........................
RF_pred <- rast("output/RFprediction.tif")
corner_coords <- c(xmin(RF_pred), ymin(RF_pred), xmax(RF_pred), ymax(RF_pred))
corner_coords
extent_to_crop <- extent(692000, 694000, 9570000, 9572000)
cropped_raster <- crop(RF_pred, extent_to_crop)

# resample the raster
resampled_raster_rf <- aggregate(cropped_raster, fact = 10, fun = mean)

# creating a color palette (pal) and applying it to the values
pal <- colorBin(
  palette = colorRamp(c("green", "grey")),
  domain = unique(values(resampled_raster_rf)),
  bins = 2,
  na.color = "transparent"
)

# create the interactive map for Random Forest Prediction
leaflet() %>% addTiles() %>%
  addRasterImage(resampled_raster_rf, colors = pal, opacity = 0.8) %>%
  addLegend(pal = pal, values = unique(values(resampled_raster_rf)),
            title = "Random Forest Prediction_pixel")

#....................SVMprediction.tif.........................
SVM_pred <- rast("output/SVMprediction.tif")

# resample the raster
resampled_raster_svm <- aggregate(SVM_pred, fact = 10, fun = mean)

# creating a color palette (pal) and applying it to the values
pal <- colorBin(
  palette = colorRamp(c("green", "grey")),
  domain = unique(values(resampled_raster_svm)),
  bins = 2,
  na.color = "transparent"
)

# create the interactive map for Random Forest Prediction
leaflet() %>% addTiles() %>%
  addRasterImage(resampled_raster_svm, colors = pal, opacity = 0.8) %>%
  addLegend(pal = pal, values = unique(values(resampled_raster_svm)),
            title = "Support Vector Machine Prediction_pixel")

#....................RFrediction.gpkg.........................
# Read the GeoJSON file
rf_geojson <- st_read("output/RFprediction_seg.gpkg")
# Create a color vector based on the "class" column
color_vector <- ifelse(rf_geojson$Class == 1, "grey", "green")

# Create a plot
plot(rf_geojson, col = color_vector, pch = 20, cex = 2)

# Add a title
title(main = "Random Forest Prediction_object")

# Add a legend
par(xpd = TRUE)
legend("topright", legend = c("MFtree","NotMFTree"), fill = c("green", "grey"))

# Add a North arrow
northArrow(x = 0.15, y = 0.1, len = 0.1, lab = "N", cex = 1.5)

# Add a scale bar
scaleBar(x = 0.8, y = 0.1, dist = 1000, units = "m", ratio = 0.2, cex = 1.2)

# Add layer source and copyright information
layerSource(x = 0.02, y = 0.02, label = "Data Source: Orthogonal RGB flights from the DJI Phantom 4 Pro RTK UAV")
copyrightLabel(x = 0.02, y = 0.05, label = "Copyright © 2023 lovely_palm_trees")

#....................SVMrediction.gpkg.........................
# Read the GeoJSON file
svm_geojson <- st_read("output/SVMprediction_seg.gpkg")

# Create a color vector based on the "class" column
color_vector <- ifelse(svm_geojson$Class == 1, "grey", "green")

# Create a plot
plot(svm_geojson, col = color_vector, pch = 20, cex = 2)

# Add a title
title(main = "Support Vector Machine Prediction_object")

# Add a legend
par(xpd = TRUE)
legend("topright", legend = c("MFtree","NotMFTree"), fill = c("green", "grey"))

# Add a North arrow
northArrow(x = 0.15, y = 0.1, len = 0.1, lab = "N", cex = 1.5)

# Add a scale bar
scaleBar(x = 0.8, y = 0.1, dist = 1000, units = "m", ratio = 0.2, cex = 1.2)

# Add layer source and copyright information
layerSource(x = 0.02, y = 0.02, label = "Data Source: Orthogonal RGB flights from the DJI Phantom 4 Pro RTK UAV")
copyrightLabel(x = 0.02, y = 0.05, label = "Copyright © 2023 lovely_palm_trees")

