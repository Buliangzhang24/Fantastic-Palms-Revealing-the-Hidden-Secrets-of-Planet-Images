if(!"terra" %in% installed.packages()){install.packages("terra")}
if(!"sf" %in% installed.packages()){install.packages("sf")}
if(!"ranger" %in% installed.packages()){install.packages("ranger")}
if(!"sp" %in% installed.packages()){install.packages("sp")}
if(!"raster" %in% installed.packages()){install.packages("raster")}
if(!"dplyr" %in% installed.packages()){install.packages("dplyr")}
library(raster)
library(terra)
library(sf)
library(ranger)
library(dplyr)

trueimage <- rast("outputclip/DMM_01_trainning area.tif")
# read classification vector
classvector <- st_read("output/DMM_01_training_vector.shp")
# read the crs from true image
raster_crs <- crs(trueimage)
# convert the crs of vector
st_crs(classvector) <- raster_crs

#calculate area
areao <- st_area(classvector$geometry)
# add the area column to classification image
classvector$area<- areao
classvector$area <- as.numeric(classvector$area)
# filter large region from image
treeshp<-classvector[classvector$area >= 10,]
summary(classvector$area >= 10)
# write it into disk
st_write(treeshp, "output/cleanedpolygon(10).shp", overwrite = TRUE)

# read the vector image of Mflexuosa tree
MFtree <- st_read("data/DMM-01/Ground data/Mflexuosa_DMM01_2019.shp")
masks <- rast("output/DMM_01_training raster.tif")
#delect the Mflexuosa from classification image
treesub <- mask(masks,MFtree,inverse = TRUE )
# convert it to sf data frame
treesub_sf <- as.polygons(treesub,dissolve = TRUE)
treesub_shp <-st_as_sf(treesub_sf)
# create the new column and set label to it 
treesub_shp <- treesub_shp %>% 
  dplyr::mutate(Class = "NotMFTree")
MFtree <- MFtree %>% 
  dplyr::mutate(Class = "MFTree")
# merge MFtree polygon to classification 
sf_data_list <- list(treesub_shp, MFtree)
merged_sf_data <- dplyr::bind_rows(sf_data_list)
# writing into the disk
st_write(merged_sf_data, "output/trainingdata.shp",overwrite = TRUE)
