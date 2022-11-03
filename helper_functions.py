import PIL
import json
import time
from pprint import pprint
from PIL import Image
from pathlib import Path
from dotenv import load_dotenv
import os
import argparse

def load_from_txt_file(txt_file_path):
    with open(txt_file_path) as file:
        array_from_txt_file = file.readlines()
        array_from_txt_file = [line.rstrip() for line in array_from_txt_file]
    return array_from_txt_file

def save_image_from_raw(output_loc, im_data):
    f = open(output_loc, 'wb')

    # save the raw image data to the file in chunks.
    for chunk in im_data:
        if chunk:
            # print(chunk)
            # print(type(chunk))
            # potentially resize here 
            f.write(chunk)
    print("image saved")
    f.close()