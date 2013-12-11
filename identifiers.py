import types
import re
import json
import os

import win32com
import win32com.client


APPS = []
BROWSERS = []


class App:
    def __init__(self, parameters={}):
        """
        @param identifiers: A list containing one or more windows title identifiers.
        A window title is the title of a window in windows, usually this
        text is used as the title on the application bar (the one with minimize, maximize and close)
        @param window_class_name: optional, name of the window class.
        @param gui_name: What will show up in the list of selectable programs in the GUI
        A window class is the name of a window in windows (windows windows windows)
        @param identify: Optional, a replacement function for the standard identify.
        @param replace_title: Optional, toggle on or off if identify should
        replace the identifier in the title with nothing or not.

        Note that optional parameters will NOT function when you replace the identify function by
        specifying the identify parameter.
        """
        self.name = parameters["name"]
        self.type = parameters["apptype"]

        try:
            self.replace_title = parameters["replace_title"]
        except KeyError:
            self.replace_title = True

        try:
            self.window_class_name = parameters["window_class_name"]
        except KeyError:
            self.window_class_name = ""

        try:
            self.remove_characters = parameters["remove_characters"]
        except KeyError:
            self.remove_characters = []

        try:
            if not parameters["apptype"] == "webbrowser":
                APPS.append(self)
        except KeyError:
            pass

        try:
            self.identifiers = [identifier for identifier in parameters["identifiers"]]
        except KeyError:
            self.identifiers = []

        try:
            self.gui_name = parameters["gui_name"]
        except KeyError:
            self.gui_name = self.name

        try:
            self.identify = types.MethodType(parameters["identify"], App)
        except KeyError:
            pass

    def identify(self, title, window_class_name):
        """Takes any window title (or any string, really) and tries to match it
        to some conditions, if it's correctly matched, the title will be returned.
        If not, it will return False.

        Valid title example: "Spotify - some song by some band",
         this contains a clearly identifyable music player (spotify)
        Invalid title example: "Python 3.3.2 Shell",
         contains no identifyable music player.

        @param title: The title of a window
        @param window_class_name: optional, can be empty. The class name of a window.
        """
        for identifier in self.identifiers:
            # removes unwanted characters, if any.
            for string in self.remove_characters:
                title = title.replace(string, "")
            # match title to the identifier, if it's a match, return the title.
            if identifier in title and self.window_class_name in window_class_name:
                # removes the identifier from the string if the option is set.
                # Example: title = "Spotify - some song by some band"
                # identifier = "Spotify - "
                # if set to True the result will be: "some song by some band"
                # if set to False, the result will be: "Spotify - some song by some band"
                if self.replace_title:
                    title = title.replace(identifier, '')
                return title
        return False

    def __repr__(self):
        return self.name


class Browser(App):
    """Almost the same as an App, but will append itself to BROWSERS
    instead of APPS"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        BROWSERS.append(self)


def mediamonkey_identify(self, title, window_class_name):
    for identifier in self.identifiers:
        if identifier in title and self.window_class_name in window_class_name:
            title = title.replace(identifier, '')
            title = re.sub('[0-9]+. ', '', title)
            return title
    return False


def winamp_identify(self, title, window_class_name):
    for identifier in self.identifiers:
        if identifier in title and self.window_class_name in window_class_name:
            if not len(title) < 11:
                title = title.replace(identifier, '')
            title = re.sub('[0-9]+. ', '', title)
            return title
    return False


def foobar_identify(self, title, window_class_name):
    for identifier in self.identifiers:
        if identifier in title and self.window_class_name in window_class_name:
            title = title[:title.find(identifier)]
            first = title.find('['.decode('utf-8'))
            second = title.find(']'.decode('utf-8'))
            title = title[:first] + title[second + 1:]
            return title
    return False


def jrivermp():
    """ uses the jriver api to find song name + artist """
    # checks if the module had been instantiated or not.
    # If it has, just return the current playing song
    # If not, instantiate it and return current playing song
    # This makes the program less stressfull, it'd instantiate
    # the module every 4 seconds
    if jrivermp.jriver:
        playlist = jrivermp.jriver.GetCurPlaylist()
        pos = playlist.position
        track = playlist.GetFile(pos)
        return track.Name + ' - ' + track.Artist
    else:
        jrivermp.jriver = win32com.client.Dispatch("MediaJukebox Application")
        playlist = jrivermp.jriver.GetCurPlaylist()
        pos = playlist.position
        track = playlist.GetFile(pos)
        return track.Name + ' - ' + track.Artist


def itunes():
    """ Uses the itunes api to find song name + artist """
    # checks if the module had been instantiated or not.
    # If it has, just return the current playing song
    # If not, instantiate it and return current playing song
    # This makes the program less stressfull, it'd instantiate
    # the module every 4 seconds
    if itunes.itunes:
        return (itunes.itunes.CurrentTrack.Name + ' - ' +
                itunes.itunes.CurrentTrack.Artist)
    else:
        itunes.itunes = win32com.client.gencache.EnsureDispatch("iTunes.Application")
        return (itunes.itunes.CurrentTrack.Name + ' - ' +
                itunes.itunes.CurrentTrack.Artist)

# Everything that is commented out is commented out because I started loading those apps
# from music_players.json
#-- browsers --#
CHROME = Browser({"name": "Google Chrome", "apptype": "webbrowser", "identifiers": ['- Google Chrome']})
CHROME_APPLICATION_MODE = Browser({"name": "Google Chrome Application mode", "apptype": "webbrowser",
                                   "identifiers": ['- Google Chrome'],
                                   "window_class_name": 'Chrome_WidgetWin_1'})
FIREFOX = Browser({"name": "Mozilla Firefox", "apptype": "webbrowser", "identifiers": ['- Mozilla Firefox']})

#-- music programs --#
#VLC = App("name": "VLC media player", "apptype": "music_player", "identifiers": ['VLC'], "window_class_name": "QWidget")
MEDIAMONKEY = App({"name": "Media monkey", "apptype": "music_player", "identifiers": ['- MediaMonkey'],
                   "identify": mediamonkey_identify})
WINAMP = App({"name": "Winamp", "apptype": "music_player", "identifiers": [' - Winamp'], "identify": winamp_identify})
FOOBAR = App({"name": "Foobar2000", "apptype": "music_player", "identifiers": ['[foobar2000'],
              "window_class_name": '{97E27FAA-C0B3-4b8e-A693-ED7881E99FC1}', "identify": foobar_identify})
#SPOTIFY = App("name": "Spotify", "apptype": "music_player", "identifiers": ['Spotify -'],
#              "window_class_name": 'SpotifyMainWindow')
#AIMP3 = App("name": "Aimp3", "apptype": "music_player", "identifiers": [' - '], "window_class_name": 'TApplication',
#            "replace_title": False)
#MUSICBEE = App("name": "Musicbee", "apptype": "music_player", "identifiers": [' - MusicBee'],
#               "window_class_name": 'WindowsForms10.Window.8.app.0.2bf8098_r35_ad1')

#-- webapps --#
#YOUTUBE = App("name": "Youtube", "apptype": "web_music_player", "identifiers": ['- YouTube'], remove_characters=["▶ "])
#GROOVESHARK = App("name": "Grooveshark", "apptype": "web_music_player", "identifiers": ['Grooveshark - '])
#SOUNDCLOUD = App("name": "Soundcloud", "apptype": "web_music_player", "identifiers": ['Soundcloud - '])
#PANDORA = App("name": "Pandora", "apptype": "web_music_player", "identifiers": ['Pandora - '])
#ZAYCEV = App("name": "Zaycev", "apptype": "web_music_player", "identifiers": ['Zaycev - '])
#GOOGLEPLAY = App("name": "Google play", "apptype": "web_music_player", "identifiers": [' - My Library - Google Play'])
#PLUGDJ = App("name": "Plug.dj", "apptype": "web_music_player", "identifiers": ['Plug.dj - '])
#EIGHTTRACKS = App("name": "8tracks", "apptype": "web_music_player", "identifiers": ['8tracks - '])
#RDIO = App("name": "Rdio", "apptype": "web_music_player", "identifiers": ['Rdio - '])

#-- apps which won't work with "identifiers":  misc --#
JRIVER = App({"name": "Jriver media center", "apptype": "misc_music_player", "identify": jrivermp})
ITUNES = App({"name": "iTunes", "apptype": "misc_music_player", "identify": itunes})
# I'd love to implement Zune and WMP, but microsoft sucks : )
# bit.ly/17zarM4 -- Stackoverflow post about this issue

# Load apps from music_players.json
try:
    json_obj = json.load(open(os.path.join("config", "music_players.json"), encoding="utf-8"))
except FileNotFoundError:
    pass
    # TODO Error dialog
for var in json_obj:
    # Bit of a hack, but that's necessary when loading python arguments from json :>

    # sets all parameters to their defaults or None
    name = None
    apptype = None
    identifiers = None
    window_class_name = ""
    replace_title = True
    remove_characters = []
    for parameter in json_obj[var].items():
        # Assigns to some/all variables above by changing the vars() object
        vars()[parameter[0]] = parameter[1]
    # print(name, apptype, identifiers, window_class_name, replace_title, remove_characters)

    # Create a new application from all the data gathered from the json
    vars()[var] = App(
        {"name": name, "apptype": apptype, "identifiers": identifiers, "window_class_name": window_class_name,
         "replace_title": replace_title, "remove_characters": remove_characters})

