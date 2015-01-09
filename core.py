# !/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import win32com
import win32com.client
import logging
import os
import ConfigParser
import re
import subprocess
import Constants
from Constants import CONFIG, TIMEOFFSET
from _winreg import OpenKey, HKEY_CURRENT_USER, EnumValue, QueryValueEx
from win32gui import GetClassName, GetWindowText, EnumWindows


def initialize():
    """ Initializes all directory dependencies for the program """
    __author__ = 'Martijn Brekelmans'
    # create logging directory
    if not os.path.exists(os.getcwd() + '\\logging'):
        os.makedirs(os.getcwd() + '\\logging')
    logging.basicConfig(filename='logging\\errors.log')
    Constants.CONFIG = Config()
    # creates or empties the current_song.txt file.
    directory = str(Constants.CONFIG.get('directories', 'current_song'))
    with open(directory + '\\current_song.txt', 'w') as fil:
        fil.write('')


class Wr:

    """ A class with write/read related methods """
    @staticmethod
    def write(text):
        """ writes the text string into the current_song.txt file """
        directory = str(Constants.CONFIG.get('directories', 'current_song'))
        try:
            with open(directory + '\\current_song.txt', 'w') as fil:
                fil.write(text.encode('utf-8'))
        except Exception, e:
            logging.exception(e)
            Constants.UI.set_playing('there was a problem with getting the'
                                     + ' song.')

    @staticmethod
    def read():
        """ reads the current_song.txt file and returns the file.read() """
        directory = str(Constants.CONFIG.get('directories', 'current_song'))
        try:
            with open(directory + '\\current_song.txt', 'r') as fil:
                return fil.read()
        except Exception, error:
            logging.exception(error)
            with open(directory + '\\current_song.txt', 'w') as fil:
                pass
            with open(directory + '\\current_song.txt', 'r') as fil:
                return fil.read()


class ProgramToken:

    """ A token defines what to do when a specific program is selected
        for most, it's to find some text in a title of a window.
        However, for some it's a little bit more.
    """

    class Webbrowser:

        """ indicates that the function is looking for a webbrowser """

        @staticmethod
        def chrome(title, className=None):
            """ Google chrome webbrowser """
            try:
                identifier = '- Google Chrome'.decode('utf-8')
                # if chrome is running
                if identifier in title:
                    title = title.replace(identifier, '')
                    return title
                return False
            except Exception, err:
                logging.exception(err)

        @staticmethod
        def chrome_application(title, className=None):
            """ Google chrome's application mode """
            try:
                class_identifier = 'Chrome_WidgetWin_1'
                identifier = '- Google Chrome'.decode('utf-8')
                if class_identifier in className:
                    if identifier in title:
                        title = title.replace(identifier, '')
                        return title
                    return title
                return False
            except Exception, err:
                raise
                logging.exception(err)

        @staticmethod
        def firefox(title, className=None):
            try:
                # if firefox is running
                identifier = '- Mozilla Firefox'.decode('utf-8')
                if identifier in title:
                    title = title.replace(identifier, '')
                    return title
                return False
            except Exception, err:
                logging.exception(err)

    class Program:

        """ indicates that the function is looking for a standalone-program """

        @staticmethod
        def vlc(title, className=None):
            # VLC is troubled by the fact that multiple languages (e.g. french)
            # give different titles.
            if 'VLC' in title and className == "QWidget":
                try:
                    # finds all '-' indexes, returns string up until last '-'
                    # this is because a song might have - inside of it already
                    # This will work regardless of language
                    indices = [m.start() for m in re.finditer('-', title)]
                    return title[:indices[-1]]
                except Exception, err:
                    logging.exception(err)
            else:
                return False

        @staticmethod
        def mediamonkey(title, classname=None):
            try:
                identifier = '- MediaMonkey'.decode('utf-8')
                if identifier in title:
                    title = title.replace(identifier, '')
                    title = re.sub('[0-9]+. ', '', title)
                    return title
                return False
            except Exception, err:
                logging.exception(err)

        @staticmethod
        def winamp(title, className=None):
            try:
                # if winamp is running
                identifier = ' - Winamp'.decode('utf-8')
                if identifier in title:
                    if not len(title) < 11:
                        title = title.replace(identifier, '')
                    title = re.sub('[0-9]+. ', '', title)
                    return title
                return False
            except Exception, err:
                logging.exception(err)

        @staticmethod
        def foobar(title, className=None):
            try:
                identifier = '[foobar2000'.decode('utf-8')
                # Foobar has a strange class, not sure why.
                class_identifier = '{97E27FAA-C0B3-4b8e-A693-ED7881E99FC1}'
                if identifier in title and className == class_identifier:
                    title = title[:title.find(identifier)]
                    first = title.find('['.decode('utf-8'))
                    second = title.find(']'.decode('utf-8'))
                    title = title[:first] + title[second + 1:]
                    return title
                return False
            except Exception, err:
                logging.exception(err)

        @staticmethod
        def spotify(title, classname=None):
            try:
                identifier = 'Spotify -'.decode('utf-8')
                class_identifier = 'SpotifyMainWindow'
                # if Spotify is running
                if identifier in title and class_identifier == classname:
                    # if a song is currently playing replace text
                    title = title.replace(identifier, '')
                    return title
                return False
            except Exception, err:
                logging.exception(err)

        @staticmethod
        def aimp3(title, classname=None):
            try:
                class_identifier = 'TApplication'.decode('utf-8')
                title_identifier = ' - '.decode('utf-8')
                if class_identifier in classname and title_identifier in title:
                    return title
                return False
            except Exception, err:
                logging.exception(err)

        @staticmethod
        def musicbee(title, classname=None):
            try:
                class_identifier = 'WindowsForms10.Window.8.app.0.' +\
                    '2bf8098_r35_ad1'
                title_identifier = ' - MusicBee'.decode('utf-8')
                if title_identifier in title and class_identifier in classname:
                    title = title.replace(title_identifier, '')
                    return title
            except Exception, err:
                logging.exception(err)

    class Webapp:

        """ indicates that the function is looking for a webapp
        inside a webbrowser """

        @staticmethod
        def youtube(title):
            try:
                identifier = '- YouTube'.decode('utf-8')
                if identifier in title:
                    title = title.replace(identifier, '')
                    return title
                return False
            except Exception, e:
                logging.exception(e)

        @staticmethod
        def spotifyweb(title):
            try:
                identifier = ' - Spotify'.decode('utf-8')
                play = '?'.decode('utf-8')
                if identifier in title:
                    title = title.replace(identifier, '')
                    if play in title:
                        title = title.replace('?', '')
                        title = "-".join(title.split(' - ')[::-1])
                    else:
                        title = "- ".join(title.split(' - ')[::-1])
                    return title
                return False
            except Exception, e:
                logging.exception(e)

        @staticmethod
        def grooveshark(title):
            try:
                identifier = 'Grooveshark - '.decode('utf-8')
                if identifier in title:
                    title = title.replace(identifier, '')
                    return title
                return False
            except Exception, e:
                logging.exception(e)

        @staticmethod
        def soundcloud(title):
            try:
                identifier = 'Soundcloud - '.decode('utf-8')
                if identifier in title:
                    title = title.replace(identifier, '')
                    return title
                return False
            except Exception, e:
                logging.exception(e)

        @staticmethod
        def pandora(title):
            try:
                identifier = 'Pandora - '.decode('utf-8')
                if identifier in title:
                    title = title.replace(identifier, '')
                    return title
                return False
            except Exception, e:
                logging.exception(e)

        @staticmethod
        def zaycev(title):
            try:
                identifier = 'Zaycev - '.decode('utf-8')
                if identifier in title:
                    title = title.replace(identifier, '')
                    return title
                return False
            except Exception, e:
                logging.exception(e)

        @staticmethod
        def googleplay(title):
            try:
                identifier = ' - My Library - Google Play'.decode('utf-8')
                if identifier in title:
                    title = title.replace(identifier, '')
                    return title
                return False
            except Exception, e:
                logging.exception(e)

        @staticmethod
        def plug(title):
            try:
                identifier = 'Plug.dj - '.decode('utf-8')
                if identifier in title:
                    title = title.replace(identifier, '')
                    return title
                return False
            except Exception, e:
                logging.exception(e)

        @staticmethod
        def eighttracks(title):
            try:
                identifier = '8tracks - '.decode('utf-8')
                if identifier in title:
                    # 8Tracks starts with ► , but python sees that as a ?
                    # It's the first two characters, so I simply replace those.
                    title = title.replace(identifier, '')
                    return title
                return False
            except Exception, e:
                logging.exception(e)

        @staticmethod
        def rdio(title):
            try:
                identifier = 'Rdio - '.decode('utf-8')
                if identifier in title:
                    title = title.replace(identifier, '')
                    return title
                return False
            except Exception, e:
                logging.exception(e)

    class Misc:

        """ indicates that the function is looking for anything else."""

        @staticmethod
        def jrivermp():
            """ uses the jriver api to find song name + artist """
            try:
                # checks if the module had been instantiated or not.
                # If it has, just return the current playing song
                # If not, instantiate it and return current playing song
                # This makes the program less stressfull, it'd instantiate
                # the module every 4 seconds
                if Constants.JRIVER:
                    playlist = Constants.JRIVER.GetCurPlaylist()
                    pos = playlist.position
                    track = playlist.GetFile(pos)
                    return track.Name + ' - ' +\
                        track.Artist
                else:
                    Constants.JRIVER = win32com.client.Dispatch\
                        ("MediaJukebox Application")
                    playlist = JRIVER.GetCurPlaylist()
                    pos = playlist.position
                    track = playlist.GetFile(pos)
                    return track.Name + ' - ' +\
                        track.Artist
            except Exception, err:
                logging.exception(err)
                return False

        @staticmethod
        def itunes():
            """ Uses the itunes api to find song name + artist """
            try:
                # checks if the module had been instantiated or not.
                # If it has, just return the current playing song
                # If not, instantiate it and return current playing song
                # This makes the program less stressfull, it'd instantiate
                # the module every 4 seconds
                if Constants.ITUNES:
                    return Constants.ITUNES.CurrentTrack.Name + ' - ' +\
                        Constants.ITUNES.CurrentTrack.Artist
                else:
                    Constants.ITUNES = win32com.client.gencache.EnsureDispatch\
                        ("iTunes.Application")
                    return Constants.ITUNES.CurrentTrack.Name + ' - ' +\
                        Constants.ITUNES.CurrentTrack.Artist
            except Exception, err:
                logging.exception(err)
                return False

        @staticmethod
        def zune():
            """ Uses the ZuneNowPlaying.exe app to get the songname + artist """
            if not Constants.ZUNESTARTED:
                Constants.SUBP = subprocess.Popen([
                    resource_path('ZuneNowPlaying.exe')])
                Constants.ZUNESTARTED = True
            try:
                exp = OpenKey(HKEY_CURRENT_USER, r"Software\ZuneNowPlaying")
                # list values owned by this registry key
                try:
                    i = 0
                    while 1:
                        name, value, type = EnumValue(exp, i)
                        i += 1
                except WindowsError:
                    pass
                title, type = QueryValueEx(exp, "Title")
                artist, type = QueryValueEx(exp, "Artist")

                returnstr = title + ' - ' + artist
                return returnstr
            except Exception, err:
                logging.exception(err)
                return False

    WebbrowserFunctions = {
        'chrome': Webbrowser.chrome,
        'chrome_application': Webbrowser.chrome_application,
        'firefox': Webbrowser.firefox
    }

    ProgramFunctions = {
        'vlc': Program.vlc,
        'winamp': Program.winamp,
        'foobar': Program.foobar,
        'spotify': Program.spotify,
        'mediamonkey': Program.mediamonkey,
        'aimp3': Program.aimp3,
        'musicbee': Program.musicbee
    }

    WebappFunctions = {
        'youtube': Webapp.youtube,
        'grooveshark': Webapp.grooveshark,
        'soundcloud': Webapp.soundcloud,
        'pandora': Webapp.pandora,
        'googleplay': Webapp.googleplay,
        'plug': Webapp.plug,
        'zaycev': Webapp.zaycev,
        '8tracks': Webapp.eighttracks,
        'rdio': Webapp.rdio,
        'spotifyweb': Webapp.spotifyweb
    }

    MiscFunctions = {
        'itunes': Misc.itunes,
        'zune': Misc.zune,
        'jrivermp': Misc.jrivermp
    }


class Main:

    """ The Main class, containing methods to run the actual program """
    selectedProgram = ''
    running = False

    @staticmethod
    def enumWindows():
        """ Enumerates over all windows, passing handle and secondary var
            I've specified secondary var as none, since I don't need it.
        """
        EnumWindows(Main.examine_wind, None)
        while Main.running:
            time.sleep(TIMEOFFSET)
            EnumWindows(Main.examine_wind, None)

    @staticmethod
    def examine_wind(hwnd, *args):
        """ examines a window title accordingly to program tokens """
        del args
        if Main.running:
            window_title = GetWindowText(hwnd).decode('cp1252')
            window_class = GetClassName(hwnd).decode('cp1252')
            title = ''

            # If the selected program is in class Misc
            # Set title to what the function returns
            if Main.selectedProgram in ProgramToken.MiscFunctions:
                title = ProgramToken.MiscFunctions[Main.selectedProgram]()

            # if the selected program is a webapp
            elif Main.selectedProgram in ProgramToken.WebappFunctions.keys():
                for browser in ProgramToken.WebbrowserFunctions.values():
                    # a token returns Text if true or False if not true.
                    browser_title = browser(window_title, window_class)
                    # if the currently iterated browser is apparent
                    if browser_title:
                        # if the currently iterated webapp is apparent
                        title = ProgramToken.WebappFunctions\
                            [Main.selectedProgram](browser_title)

            # if the selected program is a standalone program
            elif Main.selectedProgram in ProgramToken.ProgramFunctions.keys():
                title = ProgramToken.ProgramFunctions[Main.selectedProgram]\
                    (window_title, window_class)

            oldtitle = Wr.read()
            # title is set to false if nothing could be found.
            if title:
                # oldtitle is <type 'str'>, title is <type 'unicode'>
                # so I had to decode oldtitle
                if not title == oldtitle.decode('utf-8'):
                    if Constants.OPTIONS['splitText']:
                        firsthalf = title[:int(len(title) / 2)]
                        title = firsthalf
                    Wr.write(title)
                    Constants.UI.set_playing(title)


class Config(ConfigParser.RawConfigParser):

    """ Initiates and handles the config file. Grants access to some config
    utilities
    """

    def __init__(self):
        ConfigParser.RawConfigParser.__init__(self)
        # If the dir /config exists, do nothing, else create it.
        if not os.path.exists('config'):
            os.makedirs('config')
        # If config.ini exists, set config object to config.ini file
        try:
            fil = open(os.getcwd() + r'\config\config.ini', 'r')
            self.read(r'config\config.ini')
            fil.close()
            try:
                Constants.ACTIVEITEMS = self._sections['active']
                Constants.INACTIVEITEMS = self._sections['inactive']
            except:
                raise
        except IOError:
            active_items = Constants.ITEMS
            # creates the config.ini file
            with open(r'config\\config.ini', 'w'):
                pass
            self.add_section('directories')
            self.set('directories', 'current_song', os.getcwd())
            self.set('directories', 'install', os.getcwd())

            self.add_section('active')
            for item in active_items:
                self.set('active', item,
                         Constants.ITEMS[item])
            self.add_section('inactive')

            self.update()

    def update(self):
        """ Overwrites the old config file with the new contents """
        try:
            with open(os.getcwd() + r'\config\config.ini', 'wb') as configfile:
                self.write(configfile)
        except:
            raise
