from datetime import datetime
import json
from os import listdir
from typing import List

import spotipy
from spotipy.oauth2 import SpotifyOAuth

import config


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


def get_streaming_history() -> List[dict]:
    """
    reads streaming history data from json-file in MyData dump
    :return: list of streamings (dicts)
    """
    # parts of function from vlad-ds/spoty-records/history.py, but here enhanced

    files = ["MyData/" + filename for filename in listdir("MyData")
             if filename[:16] == "StreamingHistory"]

    streaming_history = []

    for filename in files:
        with open(filename, 'r', encoding='UTF-8') as file:
            streaming_history += json.load(file)

    # adding datetime field
    for streaming in streaming_history:
        streaming['datetime'] = datetime.strptime(streaming['endTime'], '%Y-%m-%d %H:%M')
    return streaming_history


def create_playlist(spotify_object):
    """
    creates a spotify playlist
    :return:
    """
    playlist_name = input("Enter the playlist name: ")
    playlist_description = input("Enter the playlist description: ")

    playlist = spotify_object.user_playlist_create(user=config.USERNAME, name=playlist_name,
                                                   public=True, description=playlist_description)
    # change config.SCOPE to "playlist-modify-private" for being able to create a private playlist

    try:
        playlist_id = playlist["id"]
        return playlist_id
    except:
        print("could not get the URI of the playlist apparently")
        return None


def search_track(spotify_object, title, artist):
    result = spotify_object.search(q=title+" "+artist)
    # print(json.dumps(result, indent=4))
    try:
        track_uri = result["tracks"]["items"][0]["uri"]
        return track_uri
    except:
        print("apparently could not access the search result for the song \"" + title + "\" by \"" + artist + "\"")
        return None



def main():
    """
    - starting point for script
    - realizes ablauf.txt
    :return:
    """
    # ask for wished time period
    start_datetime = get_datetime_from_user("start")
    end_datetime = get_datetime_from_user("end")

    # read data from JSON-files (data from "Download your data")
    streaming_history = get_streaming_history()

    # connect with spotify
    token = SpotifyOAuth(scope=config.SCOPE, username=config.USERNAME, client_id=config.CLIENT_ID, client_secret=config.CLIENT_SECRET, redirect_uri=config.REDIRECT_URI)
    spotify_object = spotipy.Spotify(auth_manager=token)

    # create playlist
    playlist_id = create_playlist(spotify_object)
    if playlist_id is None:
        print("playlist_id is None")
        return

    # search for the tracks on spotify
    track_list = []
    if track_list:
        print("Search for the tracks on Spotify:")
    for track in streaming_history:
        if start_datetime <= track["datetime"] <= end_datetime:
            track_uri = search_track(spotify_object, track["trackName"], track["artistName"])
            if track_uri is not None:
                track_list.append(track_uri)
                print(str(track["datetime"]) + ": " + track_uri + " - found \"" + track["trackName"] + "\" by \"" + track["artistName"] + "\" on Spotify")

    # add tracks to the spotify playlist / fill playlist
    print("Add tracks to the Spotify playlist")
    if track_list:
        n = 100  # max addable tracks per request
        for track_list_chunk in [track_list[i:i + n] for i in range(0, len(track_list), n)]:
            spotify_object.playlist_add_items(playlist_id=playlist_id, items=track_list_chunk, position=None)

    # confirm process
    print("\nDONE")

if __name__ == '__main__':
    main()