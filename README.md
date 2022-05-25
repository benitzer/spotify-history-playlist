# spotify-history-playlist
Python script for creating a Spotify playlist based on streaming history for a specific time period (data from "Download your data")

Partly based on: [How To Create Spotify Playlist Using Python! - Kalyan Codes](https://www.youtube.com/watch?v=jSOrEmKUd_c)

# Instruction
## Download data from Spotify
1. Download your data (including the streaming history) from the [Spotify Privacy Settings](https://www.spotify.com/account/privacy/) (at the bottom of the page).
## Configure Spotify Developer account and create app
2. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) and login with your Spotify account.
3. Create a new app called "spotify-history-playlist". App description: "Creating a playlist based on the listening history (data from "Download your data")".
4. Click EDIT SETTINGS, add http://127.0.0.1:8080/ as Redirect URI and save.
5. Note Client ID and Client Secret.
## Local configuration and execution
6. Place the "MyData"-folder (extracted from the requested and downloaded Spotify data) in the same folder like the spotify_history_playlist.py script and the config_template.py.
7. Rename config_template.py to config.py.
8. Fill config.py with your data (Spotify username (not mail adress), Client ID, Client Secret). If you don't know your username you can find it on the [Spotify Account Overview](https://www.spotify.com/account/overview/).
9. Execute spotify_history_playlist.py.
10. Follow the instructions in the program and in the browser (for giving access rights).
11. Enjoy the music listened in the history. :)

# Requirements
- [Python](https://www.python.org/downloads/)
- [spotipy](https://github.com/plamere/spotipy)
