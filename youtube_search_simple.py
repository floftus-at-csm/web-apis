
from pprint import pprint

import os

import googleapiclient.discovery
from googleapiclient.discovery import build
import subprocess
import requests

import youtube_dl
from yt_dlp import YoutubeDL
from youtube_dl.utils import DateRange
import time
from dotenv import load_dotenv
from pathlib import Path


def get_video_list(key, term, maxVals=20, live=False, order_v = "relevance"):
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
            maxResults=maxVals,
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
            maxResults=maxVals,
            order=order_v,
            q=term,
            safeSearch="none",
            type="video",
            videoCaption="any"
        )
    response = request.execute()
    return response

def get_video_list_before_year(key, term, date, maxVals=20, live=False, order_v = "relevance"):
    # ================================================
    # calling the API
    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = key)
    request = youtube.search().list(
        part="id",
        channelType="any",
        maxResults=maxVals,
        order=order_v,
        q=term,
        safeSearch="none",
        type="video",
        videoCaption="any",
        publishedBefore=date+'-01-01T00:00:00Z'
    )
    response = request.execute()
    print("the response is: ", response)
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
    print("full ids are: ", full_youtube_ids)
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

def download_videos_simple(url, output_loc, max="100M"):
    Path(output_loc).mkdir(parents=True, exist_ok=True)
    out = output_loc + "%(title)s-%(id)s.%(ext)s"
    ydl_opts = {
    'format': 'best',
    'max': '100M',
    'outtmpl': out,
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    # subprocess.run(['youtube-dl', '-o', output_loc, '-f', 'best', '--max-filesize', max, url], capture_output=True)
    print("video downloaded")

def download_videos_during_period(url, output_loc, before, after, max="100M"):
    Path(output_loc).mkdir(parents=True, exist_ok=True)
    out = output_loc + "%(title)s-%(id)s.%(ext)s"
    ydl_opts = {
    'format': 'best',
    'max': '100M',
    'outtmpl': out,
    'daterange':DateRange(after, before),
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    # subprocess.run(['youtube-dl', '-o', output_loc, '-f', 'best', '--max-filesize', max, '-dateafter', after, '-datebefore', before, url], capture_output=True)
    print("downloaded videos in playlist")

def download_videos_before(url, output_loc, before, max="100M"):
    subprocess.run(['youtube-dl', '-o', output_loc, '-f', 'best', '--max-filesize', max, '-datebefore', before, url], capture_output=True)
    print("downloaded videos in playlist")

def download_videos_in_list(list_v, output_loc, max="100M"):
    for video in list_v:
        download_videos_simple(video, output_loc, max)
    print("all videos downloaded")

def save_ids(ids, output_loc, filename):
    with open(output_loc + filename + '.txt', 'w') as txt_file:
        for line in ids:
            line_str = [str(n) for n in line] # create string list from integer list
            txt_file.write(" ".join(line_str) + "\n")
    print("file saved at: ", output_loc + filename + ".txt")

def load_urls_from_file(filepath):
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]
    print("the array is: ", lines)
    return lines

def set_up_environment():
    load_dotenv()
    key = os.environ.get("YOUTUBE_DATA_API_KEY") # Define the API Key. This should be in a hidden file
    return key


# =========================================================================
# Main Loop
if __name__ == "__main__":
    id_val = 0
    DEVELOPER_KEY = set_up_environment()
    term = input("what search term would you like to use?")
    year = input("Before which year?")
    maximum = int(input("how many videos would you like to download?"))
    output_location = input("what directory should you download the video to?")

    # output_loc = input("where do you want to download the videos to?")
    api_response = get_video_list_before_year(DEVELOPER_KEY, term, year, maximum) #final term could be rating, title, video count, date
    print("/nThe API Response is: ", api_response)

    the_ids = get_ids(api_response)
    print("the ids are: ", the_ids)

    download_videos_in_list(the_ids, output_location, max="100M")




# e.g. python youtube_search_simple.py
# funky odd dance
# 10
# content/intro/downloads/