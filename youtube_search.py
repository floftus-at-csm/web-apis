
from pprint import pprint

import os

import googleapiclient.discovery
from googleapiclient.discovery import build

import subprocess

import requests

import time
from dotenv import load_dotenv


def call_api(key, term, live=False, order_v = "relevance"):
    # ================================================
    # calling the API
    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = key)

    if live == True:
        request = youtube.search().list(
            part="id",
            channelType="any",
            eventType="live",
            maxResults=20,
            order=order_v,
            q=term,
            safeSearch="none",
            type="video",
            videoCaption="any"
        )
    if live == False:
        request = youtube.search().list(
            part="id",
            channelType="any",
            maxResults=20,
            order=order_v,
            q=term,
            safeSearch="none",
            type="video",
            videoCaption="any"
        )
    response = request.execute()
    return response

def get_title(id1, key):
	youtube = build('youtube', 'v3', developerKey=key)
	print("id1 is: ", id1)
	url = id1
	stripped_url = url.replace("https://www.youtube.com/watch?v=", '')
	print(stripped_url)
	title = ""
	results = youtube.videos().list(id=stripped_url, part='snippet').execute()
	print("the result is: ", results)
	for result in results.get('items', []):
		print("getting the title ")
		print(result['id'])
		print(result['snippet']['title'])
		title = result['snippet']['title']
	return title

def get_ids(resp):
    # ================================================
    # Getting the youtube IDs out of the API response
    
    items = resp["items"]

    youtube_ids = []
    for item in items:
        yt_id = item["id"]
        youtube_ids.append(yt_id['videoId'])

    print(youtube_ids)
    print("the first one is: ")
    print(youtube_ids[0])
    print(len(youtube_ids))

    url_basic = "https://www.youtube.com/watch?v="
    full_youtube_ids = []
    val = 0
    for x in youtube_ids:
        full_youtube_ids.append( url_basic + x )
        val=val+1
    # print(full_youtube_ids)
    return full_youtube_ids

def start_up_stream(ids, id_number):
	# ================================================
	# open video stream
	# ================================================

	command = 'timeout 15s streamlink -p "omxplayer --orientation 180" --player-fifo '
	
	command = command + ids[id_number] + ' best' 
	print("the command is " + command)
	os.system(command)


def start_up_stream_and_close_stream(ids):
	# ================================================
	# open video stream
	# ================================================

	command = 'streamlink -p "omxplayer --timeout 20" --player-fifo '
	
	command = command + ids[id_val] + ' best' 
	os.system(command)

def remove_unwanted(titles, ids, words_to_avaoid):
    # ================================================
    # removing unwanted titles
    # ================================================
    ids_size = len( the_ids)
    id_val = ids_size - 1
    for word in words_to_avaoid:
        if word in titles:
            # remove from list
            print("we need to remove this!")
            ids.remove(ids[id_val]) # check this
            ids_size = len(ids)
            print("the second id_size is: ", ids_size)
            id_val = ids_size - 1
    return ids, ids_size

id_val = 0
avoid_these = ["Meme", "meme", "MEME","Coffin","COFFIN", "Coffin", "Dance", "DANCE", "dance", "Cleanse", "CLEANSE", "cleanse", "Vibration", "VIBRATION", "vibration", "Sonic", "SONIC", "sonic", "Lightning", "LIGHTNING", "lightning", "McQueen","GTA", "gta", "Gta", "Minecraft", "MINECRAFT", "Memes", "MEMES", "memes", "Funny", "FUNNY", "funny", "Birds", "BIRDS", "birds", "TV", "tv", "Tv"]
load_dotenv()
DEVELOPER_KEY  = os.environ.get("GOOGLE_API_KEY") # Define the API Key. This should be in a hidden file

api_response = call_api(DEVELOPER_KEY, "another walk", False, "relevance") #final term could be rating, title, video count, date
print(api_response)

the_ids = get_ids(api_response)
print("the ids are: ", the_ids)

counter = 0
current_title = get_title(the_ids[id_val])
print("the current title is: ", current_title)

the_ids, id_size = remove_unwanted(current_title, the_ids, avoid_these)


