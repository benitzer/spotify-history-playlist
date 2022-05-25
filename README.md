# spotify-history-playlist
Python script for creating a spotify playlist based on streaming history for a specific time period (data from "Download your data")

Partly based on: https://www.youtube.com/watch?v=jSOrEmKUd_c

# Instruction
## Download data
1. Download your data from the privacy settings on https://www.spotify.com.
## Configure Spotify Developer account and create app
2. Go to https://developer.spotify.com/, go to Dashboard and login with your spotify account.
3. Create a new app called "spotify-history-playlist". App description: "Creating a playlist based on the listening history (data from "Download your data")".
4. Edit App: add http://127.0.0.1:8080/ as Redirect URI.
5. Note Client ID and Client Secret.
## Local configuration
6. Place the (extracted) "MyData"-folder in the same folder like the spotify-history-playlist.py script and the config-template.py.
7. Rename config-template.py to config.py.
8. Fill config.py with your data (Spotify-username, Client ID, Client Secret).
10. Execute spotify-history-playlist.py.
11. Follow the instructions in the program and in the browser (for giving access rights).
