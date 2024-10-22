#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 10:16:46 2023

@author: osboxes
"""

import os
import requests
import zipfile

# URL of the direct download link from OneDrive 
# the URL sometimes needs to update. if the link doesn't work, please try the one: https://1drv.ms/u/s!AmYNuJYQSpMvgqZWyiFBoNyUAQdysw?e=phJjab
url = "https://public.dm.files.1drv.com/y4mO71NLg-dLlNPX0npbwriODKDaR9bjxSlZpiJghoeCmOshCBztrq97uEnoHl4jm1r3pMDXLBqxbJe33yOJdpn7exxEupbvzM0LqYvcBKy_19Py8BNUk2-45kobpUd7dt-VKKa2lYLah9aCxIk8qhl47YTluCh9IWET1dzaTCQCPp0XRrgWjGnK_UiAmPVoyYA4HvhP0d7wtVGldsazir3_UqD0APFjfC9Sdn4w5MITQk?AVOverride=1"

# Ensure the 'data' directory exists
if not os.path.exists('data'):
    os.makedirs('data')

# Define the path to save the file
save_path = os.path.join('data', 'downloaded_file.zip')

# Stream the download and write chunks to the file
with requests.get(url, stream=True) as response:
    response.raise_for_status()  # Check for any download issues
    with open(save_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):  # 8KB chunks
            file.write(chunk)

print(f"File downloaded to {save_path}")

# Create the DMM-01 folder inside 'data'
extraction_path = os.path.join('data', 'DMM-01')
if not os.path.exists(extraction_path):
    os.makedirs(extraction_path)

# If the file is a ZIP, extract it in the 'DMM-01' directory
if zipfile.is_zipfile(save_path):
    with zipfile.ZipFile(save_path, 'r') as zip_ref:
        zip_ref.extractall(extraction_path)
        print(f"ZIP file extracted in the '{extraction_path}' folder")
