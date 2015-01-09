""" All constants for SMG """
from os import environ
from os.path import dirname, join
import sys
# The time waited until the next loop
UI = None
CONFIG = None
TIMEOFFSET = 4
# if ZuneNowPlaying is running or not
ZUNESTARTED = False
JRIVER = None
ITUNES = None
# the version of the program, used for checking for updates.
VERSION = 1

# All programs that are toggled on by user
ACTIVEITEMS = {}
# All programs that are toggled off by user
INACTIVEITEMS = {}
# All items
ITEMS = {
    'foobar2000': 'foobar',
    'winamp': 'winamp',
    'vlc media player': 'vlc',
    'spotify': 'spotify',
    'spotifyweb *': 'spotifyweb',
    'grooveshark': 'grooveshark',
    'youtube': 'youtube',
    'soundcloud': 'soundcloud',
    'pandora *': 'pandora',
    'itunes': 'itunes',
    'mediamonkey': 'mediamonkey',
    'zune': 'zune',
    'plug.dj *': 'plug',
    'jriver media payer': 'jrivermp',
    'zaycev *': 'zaycev',
    '8tracks *': '8tracks',
    'rdio *': 'rdio',
    'google play music *': 'googleplay',
    'musicbee': 'musicbee'
}
# Zune sup-process
SUBP = None

OPTIONS = {
    'splitText': False
}

update_dialog_lbl = None
update_dialog = None


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    filename = relative_path
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller >= 1.6
        # chdir(sys._MEIPASS)
        filename = join(sys._MEIPASS, filename)
    elif '_MEIPASS2' in environ:
        # PyInstaller < 1.6 (tested on 1.5 only)
        # chdir(environ['_MEIPASS2'])
        filename = join(environ['_MEIPASS2'], filename)
    else:
        # chdir(dirname(sys.argv[0]))
        filename = join(dirname(sys.argv[0]), filename)
    return filename
_timeOffset = 4
