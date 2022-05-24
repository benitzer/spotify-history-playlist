import ast
import json

import spotipy
from typing import List
from os import listdir
from datetime import datetime
from spotipy.oauth2 import SpotifyOAuth

import config
from config import *


def get_datetime_from_user(kind_of_datetime: str) -> datetime:
    """
    asks user for date and time and creates datetime-object
    :return: datetime-object
    """
    datetime_obj_set = False
    while not datetime_obj_set:
        try:
            datetime_str = input("Enter " + kind_of_datetime +" date and time (in UTC, 24h per day) in format \"YYYY-MM-DD HH:MM\": ")
            datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
            datetime_obj_set = True
        except ValueError as exception:
            print(exception)
            print("Try again!")
    return datetime_obj


def get_streaming_history(path: str = 'MyData',
                          ) -> List[dict]:
    '''Returns a list of streamings form spotify MyData dump.
    Will not acquire track features.'''
    # method from vlad-ds/spoty-records history.py

    files = ['MyData/' + x for x in listdir(path)
             if x.split('.')[0][:-1] == 'StreamingHistory']

    all_streamings = []

    for file in files:
        with open(file, 'r', encoding='UTF-8') as f:
            new_streamings = ast.literal_eval(f.read())
            all_streamings += [streaming for streaming in new_streamings]

    # adding datetime field
    for streaming in all_streamings:
        streaming['datetime'] = datetime.strptime(streaming['endTime'], '%Y-%m-%d %H:%M')
    return all_streamings


def create_playlist(spotify_object):
    """
    creates a spotify playlist
    :return:
    """
    playlist_name = input("Enter the playlist name: ")  # TODO script could name the playlist based on the wished time period
    playlist_description = input("Enter the playlist description: ")

    playlist = spotify_object.user_playlist_create(user=config.USERNAME, name=playlist_name, public=True, description=playlist_description)  # change config.SCOPE to "playlist-modify-private" for being able to create a private playlist
    try:
        playlist_id = playlist["id"]
        return playlist_id
    except:
        print("could not get the URI of the playlist apparently")
        return


def search_track(spotify_object, title, artist):
    result = spotify_object.search(q=title+" "+artist)
    # print(json.dumps(result, indent=4))
    try:
        track_uri = result["tracks"]["items"][0]["uri"]
        return track_uri
    except:
        print("apparently could not access the search result for the song \"" + title + "\" by \"" + artist + "\"")
        return



def main():
    """
    - starting point for script
    - realizes ablauf.txt
    :return:
    """
    # ask for wished time period
    start_datetime = get_datetime_from_user("start")
    end_datetime = get_datetime_from_user("end")

    # read data from JSON-files ("Request my data")
    streaming_history = get_streaming_history()

    # connect with spotify
    token = SpotifyOAuth(scope=config.SCOPE, username=config.USERNAME, client_id=config.CLIENT_ID, client_secret=config.CLIENT_SECRET, redirect_uri=config.REDIRECT_URI)
    spotify_object = spotipy.Spotify(auth_manager=token)

    # create playlist
    # TODO ask user "playlist already existing?" -> if yes: ask for playlist_id (or name and script has to search) and don't create new one
    playlist_id = create_playlist(spotify_object)
    if playlist_id is None:
        print("playlist_id is None")
        return

    # search for the tracks at spotify
    track_list = []
    for track in streaming_history:
        if start_datetime <= track["datetime"] <= end_datetime:
            track_uri = search_track(spotify_object, track["trackName"], track["artistName"])
            if track_uri is not None:
                track_list.append(track_uri)
    print(track_list)

    # add tracks to the spotify playlist / fill playlist
    if track_list:
        n = 100  # max addable tracks per request
        for track_list_chunk in [track_list[i:i + n] for i in range(0, len(track_list), n)]:
            spotify_object.playlist_add_items(playlist_id=playlist_id, items=track_list_chunk, position=None)

    # confirm process
    print("DONE")

if __name__ == '__main__':
    main()