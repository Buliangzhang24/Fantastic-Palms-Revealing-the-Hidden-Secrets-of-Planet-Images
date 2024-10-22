#!/bin/bash
# Run all parts of the project one by one
# create directory
mkdir output
mkdir outputclip

# install these packages are not exist in the conda-forge channel
conda install torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
pip install opencv-python 

chmod u+x 1_download and extract_modified.py 2_clip_modified.py 3_segment_modified.py 4_vectorize_modified.py 5_set_label.R 6_1_prediction_segment.py6_2_prediction_nosegment.py 7_visualization_leaflet.R

python3 1_download_and_extract_modified.py || exit 1
python3 2_clip_modified.py || exit 1
python3 3_segment_modified.py || exit 1
python3 4_vectorize_modified.py || exit 1
Rscript 5_set_label.R || exit 1
python3 6_1_prediction_segment.py || exit 1
python3 6_2_prediction_nosegment.py || exit 1
Rscript 7_visualization_leaflet.R || exit 1

rm -r outputclip
