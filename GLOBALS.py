__author__ = 'martijn'
import os

# Root folder of the application
ROOT = os.path.abspath(os.path.dirname(__file__))

# The time waited until the next iteration of the loop checking
# for songs
# set it higher, and it will take longer to update the song when a new one comes up
# set it to a lot lower, and the it will take a lot of your processing power.
# I'd recommend staying above a minimum of 0.5s
# set it to very low, and your pc will hang. :)
TIMEOFFSET = 4

# the version of the program, used for checking for updates.
VERSION = 1337

# the default json file, in case the music_players.json file gets deleted
MUSIC_PLAYERS_JSON = """{
    "VLC": {
        "name": "VLC media player",
        "apptype": "music_player",
        "identifiers": ["VLC"],
        "window_class_name": "QWidget"
    },
    "SPOTIFY": {
        "name": "Spotify",
        "apptype": "music_player",
        "identifiers": ["Spotify -"],
        "window_class_name": "SpotifyMainWindow"
    },
    "AIMP3": {
        "name": "Aimp3",
        "apptype": "music_player",
        "identifiers": [" - "],
        "window_class_name": "TApplication",
        "replace_title":  "False"
    },
    "MUSICBEE":  {
        "name": "Musicbee",
        "apptype": "music_player",
        "identifiers": [" - MusicBee"],
        "window_class_name": "WindowsForms10.Window.8.app.0.2bf8098_r35_ad1"
    },
    "YOUTUBE": {
        "name": "Youtube",
        "apptype": "web_music_player",
        "identifiers": ["- YouTube"],
        "remove_characters": ["▶ "]
    },
    "GROOVESHARK": {
        "name": "Grooveshark",
        "apptype": "web_music_player",
        "identifiers": ["Grooveshark - "]

    },
    "SOUNDCLOUD": {
        "name": "Soundcloud",
        "apptype": "web_music_player",
        "identifiers": ["Soundcloud - "]

    },
    "PANDORA": {
        "name": "Pandora",
        "apptype": "web_music_player",
        "identifiers": ["Pandora - "]
    },
    "ZAYCEV": {
        "name": "Zaycev",
        "apptype": "web_music_player",
        "identifiers": ["Zaycev - "]
    },
    "GOOGLEPLAY": {
        "name": "Google play",
        "apptype": "web_music_player",
        "identifiers": [" - My Library - Google Play"]
    },
    "PLUGDJ": {
        "name": "Plug.dj",
        "apptype": "web_music_player",
        "identifiers": ["Plug.dj - "]
    },
    "EIGHTTRACKS": {
        "name": "8tracks",
        "apptype": "web_music_player",
        "identifiers": ["8tracks - "]
    },
    "RDIO": {
        "name": "Rdio",
        "apptype": "web_music_player",
        "identifiers": ["Rdio - "]
    }
}"""