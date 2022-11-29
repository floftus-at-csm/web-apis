# 1. for each name in the community gardens list get images from google images, save into folder named by the list
# check for errors - log these errors so I can check them over
# if folder already exists do what?
# 2. compile into gif
# 3. use gif to form a set of composite images
# 4. save composite images in a folder
# 5. compile composite images into a gif
# 6. save gifs into folder
# =========================================================================
# Import necessary libraries
import PIL
import json
import time
import googlemaps
from pprint import pprint
from PIL import Image
from pathlib import Path
from dotenv import load_dotenv
import os
import argparse
from helper_functions import load_from_txt_file, save_image_from_raw
# =========================================================================
# create functions
# def load_from_txt_file(txt_file_path):
#     with open(txt_file_path) as file:
#         array_from_txt_file = file.readlines()
#         array_from_txt_file = [line.rstrip() for line in array_from_txt_file]
#     return array_from_txt_file

def create_folder_from_title(f_path, title):
    search_term_file_name = title.replace(" ", "_") #replace the spaces in the string with underscores
    path_s = f_path + search_term_file_name + "/"
    Path(path_s).mkdir(parents=True, exist_ok=True)
    return search_term_file_name

# def save_image_from_raw(output_loc, im_data):
#     f = open(output_loc, 'wb')

#     # save the raw image data to the file in chunks.
#     for chunk in im_data:
#         if chunk:
#             # print(chunk)
#             # print(type(chunk))
#             # potentially resize here 
#             f.write(chunk)
#     print("image saved")
#     f.close()

def get_urls_of_images(api_key, input_url, dictionary_v, fields):
    whats_been_left = api_key.places(query=input_url) # do initial query to get the id for each location
    pprint(whats_been_left['results'][0]['place_id'])  # pretty print the result
    
    digital_id = whats_been_left['results'][0]['place_id'] # get the list of ids

    # is this dictionary bit needed?
    dictionary_v[input_url] = digital_id # add digital id to dictionary next to the site name (land)
    print("the dictionary is: ", dictionary_v)

    place_details  = api_key.place(place_id= digital_id , fields= fields)# do second query, the details query, which allows you access to the photo urls
    print("the places details are: ", place_details['result'])
    return dictionary_v, place_details


def get_images(search_terms, key, output_path):
    my_fields = ['name', 'photo'] # fields needed to get photos
    photo_width = 5000 # I think this is max size                      
    photo_height = 5000
    dictionary_of_sites = {}
    for search_term in search_terms[0:2]:
        dictionary_of_sites, places_details = get_urls_of_images(key, search_term, dictionary_of_sites, my_fields)
        search_term_file_name = create_folder_from_title(output_path, search_term)
        # search_term_file_name = search_term.replace(" ", "_") #replace the spaces in the string with underscores
        path_s = output_path + search_term_file_name + "/"
        # Path(path_s).mkdir(parents=True, exist_ok=True)
        val = 0
        try:
            for photo in places_details['result']['photos']:
                photo_id = photo['photo_reference']
                print("the photo id is: ", photo_id)
                raw_image_data = gmaps.places_photo(photo_reference = photo_id, max_width = photo_width, max_height = photo_height) # request the image, using the Places Photot API.
                print("the raw image date is", type(raw_image_data))
                download_path_s = path_s + search_term_file_name + str(val) + ".png"
                save_image_from_raw(download_path_s, raw_image_data) # raw image data is returned so we will save that raw data to a JPG file.
                val = val + 1 
        except:
            print("********************************")
            print("no photos in: ", search_term)
            print("********************************")
# =========================================================================
# Main Loop
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="text files of urls")
    parser.add_argument("--output", help="set name of output folder")
    args=parser.parse_args()

    load_dotenv()
    API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY") # Define the API Key. This should be in a hidden file

    # Define the Client
    gmaps = googlemaps.Client(key = API_KEY)

    # load the list of names
    common_sites = load_from_txt_file(args.input)

    # get images
    get_images(common_sites, gmaps, 'static/downloaded/')
    # dictionary_of_sites = {}
    # for land in common_sites[0:2]:
    #     whats_been_left = gmaps.places(query=land) # do initial query to get the id for each location
    #     pprint(whats_been_left['results'][0]['place_id'])  # pretty print the result
        
    #     digital_id = whats_been_left['results'][0]['place_id'] # get the list of ids

    #     dictionary_of_sites[land] = digital_id # add digital id to dictionary next to the site name (land)
    #     print("the dictionary is: ", dictionary_of_sites)

    #     places_details  = gmaps.place(place_id= digital_id , fields= my_fields)# do second query, the details query, which allows you access to the photo urls
    #     print("the places details are: ", places_details['result'])
        
    #     val = 0
    #     land_file_name = land.replace(" ", "_") #replace the spaces in the string with underscores
    #     path_s = "static/downloaded/" + land_file_name + "/"
    #     Path(path_s).mkdir(parents=True, exist_ok=True)

    #     # for photo in places_details['result']['photos']:
    #     try:
    #         for photo in places_details['result']['photos']:
    #             photo_id = photo['photo_reference']
    #             raw_image_data = gmaps.places_photo(photo_reference = photo_id, max_width = photo_width, max_height = photo_height) # request the image, using the Places Photot API.
    #             print("the raw image date is", type(raw_image_data))
    #             download_path_s = path_s + land_file_name + str(val) + ".png"
    #             save_image_from_raw(download_path_s, raw_image_data) # raw image data is returned so we will save that raw data to a JPG file.
    #             val = val + 1 
    #     except:
    #         print("********************************")
    #         print("no photos in: ", land)
    #         print("********************************")

    # process images