""" The python file doing everything gui related. """
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PySide.QtGui import QMessageBox, QMainWindow, QWidget, \
    QApplication, QFileDialog, QListWidget, QFont, QPushButton, \
    QLabel, QComboBox, QIcon, QTabWidget, QFrame, QLineEdit, QSystemTrayIcon, \
    QCheckBox, QDialog
from PySide.QtCore import QObject, SIGNAL, QEvent, Qt
from random import randint
from urllib import urlopen
# My own library made for this project
from core import *
from threading import Thread
import threading
# from Constants import *
# File with all kinds of Constants
from Constants import resource_path, VERSION, SUBP, ITEMS
import pythoncom
import sys
import os

class Misc(object):

    """ Contains strings to use in the gui """
    # Additional messages to display whenever something specific happens

    # The message to display when no song is playing
    noSongPlaying = 'No song is currently playing'

    # When you select grooveshark/pandora/plug.dj
    GetGroovemarklet = "Don't forget to get the " +\
        "<a href='http://www.league-insanity.tk/Azeirah_content'>" +\
        "Groovemarklet</a> for programs marked with an *"
    VisitForums = "Stop by the forums if you need any additional help. <a " +\
        "href=" +\
        "'http://www.obsproject.com/forum/viewtopic.php?f=22&t=4223'>OBS</a>," +\
        "<a href='http://www.xsplit.com/forum/viewtopic.php?f=18&t=20331'> XSplit" +\
        "</a>."
    # When you select Zune
    ZuneNotification = "Got problems with Zune? Start this program as" +\
        " an administrator!"

    messages = [
        GetGroovemarklet,
        VisitForums,
        ZuneNotification,
        "Have a nice day!",
        "Have any suggestions? Stop by the <a href=" +
        "'http://www.obsproject.com/forum/viewtopic.php?f=22&t=4223'>" +
        "obsforums</a> or send me an email.",
        "Found a bug? Send me an email.",
        "Your player isn't supported? Send me an email.",
        "Have a good day! :)",
        "Thanks for using my program.",
        "This program was made by Azeirah.",
        "The program automatically updates whenever you restart it!",
        "Current webbrowsers supported are Google Chrome and Firefox.",
        "Only click the groovemarklet once. It will run slower :(",
        "If you'd like to leave a donation <a href=" +
        "'http://www.league-insanity.tk/Azeirah_content/donate.html'>" +
        "you can do so here</a>",
        "You can enable/disable music apps in the Options tab!",
        "You can change your output directory in the Options tab!"
    ]

    @staticmethod
    def misc_message():
        """ Returns one of the messages randomly from messages """
        return Misc.messages[randint(0, len(Misc.messages) - 1)]


class UiMain(QMainWindow):

    """ The main gui interface, invokes all windows and ties everything
     together
    """

    def __init__(self):
        """ automatically called __init__ function """

        super(UiMain, self).__init__()

        # initialize all the variables that are going to be defined in the
        # future
        self.update_dialog = None
        self.update_dialog_lbl = None
        self.app_select_box = None
        self.selector_lbl = None
        self.current_playing_lbl = None
        self.current_playing = None
        self.misc_messages = None
        self.start_btn = None
        self.output_dir_lbl = None
        self.select_output_dir_btn = None
        self.output_cur_dir_lbl = None
        self.active_items_list = None
        self.inactive_items_list = None
        self.switch_active_item_button_off = None
        self.switch_active_item_button_on = None
        self.switch_output_split_btn = None
        self.switch_output_split_lbl = None

        # initialize the system tray
        # self.system_tray = QSystemTrayIcon(self)
        # self.system_tray.setIcon(QIcon(resource_path('icon.png')))
        # self.system_tray.show()
        # self.system_tray.setToolTip('SMG')
        # self.system_tray.activated.connect(self.on_systray_activated)

        # initialize the main window
        self.setObjectName('self')
        self.setWindowTitle('SMG - By Azeirah')
        self.resize(400, 250)

        # Gives the self an icon
        self.setWindowIcon(QIcon(resource_path('icon.png')))

        # create the tabs
        # the tab widget itself
        self.tabbed_windows = QTabWidget(self)
        self.tabbed_windows.resize(400, 300)

        # tab 1, contains the music player selection
        self.music_players = QFrame()

        # tab 2, contains options
        self.options = QFrame()
        self.tabbed_windows.addTab(self.music_players, 'Music players')
        self.tabbed_windows.addTab(self.options, 'Options')

        # initializes the two tabs, with all the code down below
        self.tab_music_players()
        self.tab_options()

        # shows the main window
        self.show()

        # self.update()
        CheckUpdateThread = Thread(target=self.update)
        CheckUpdateThread.setName('CheckUpdateThread')
        CheckUpdateThread.run()

    def closeEvent(self, event):
        """ an automatically called function when the program is about to
        close.
        """
        # Stops all Threads. These would continue to run in the background
        # Even if the window was closed.
        Main.running = False
        # close the ZuneNowPlaying.exe process
        if Constants.SUBP:
            Constants.SUBP.kill()

    def changeEvent(self, event):
        # if event.type() == QEvent.WindowStateChange:
        #     if self.isMinimized():
        #         event.ignore()
        #         self.hide()
        #         self.system_tray.showMessage('Running', 'Running in the
        #           background.')
        #         return

        super(UiMain, self).changeEvent(event)

    def on_systray_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()

    @staticmethod
    def toggle_split(event):
        # 0 = Qt.Unchecked The item is unchecked.
        # 1 = Qt.PartiallyChecked The item is partially checked. Items in
        # hierarchical models may be partially checked if some, but not all,
        # of
        # their children are checked.
        # 2 = Qt.Checked The item is checked.
        if event == 0:
            Constants.OPTIONS['splitText'] = False
        elif event == 2:
            Constants.OPTIONS['splitText'] = True

    def tab_music_players(self):
        """ Everything inside the Music players tab gets created here."""
        # self.music_players
        # Creates the box with all the music players inside of it
        self.app_select_box = QComboBox(self.music_players)
        self.app_select_box.setGeometry(135, 10, 150, 25)
        # Whenever you change the application, it runs the selectnewapp func
        self.app_select_box.activated[str].connect(self.select_new_app)

        # Creates the label for the selection combobox
        self.selector_lbl = QLabel(self.music_players)
        self.selector_lbl.setGeometry(10, 10, 150, 25)
        self.selector_lbl.setText('Select your music player: ')

        # Creates the label for the current playing song (and the current
        # playing song label)
        self.current_playing_lbl = QLabel(self.music_players)
        self.current_playing_lbl.setGeometry(10, 45, 150, 25)
        self.current_playing_lbl.setText('Current playing song: ')

        self.current_playing = QLabel(self.music_players)
        self.current_playing.setGeometry(117, 45, 250, 25)
        self.current_playing.setText(Misc.noSongPlaying)

        # Creates a label which displays any additional messages
        self.misc_messages = QLabel(self.music_players)
        self.misc_messages.setGeometry(10, 80, 390, 24)
        self.misc_messages.setText(Misc.misc_message())
        self.misc_messages.setOpenExternalLinks(True)

        # adds all the music players into the combobox
        self.app_select_box.addItem(None)
        for item in Constants.ACTIVEITEMS:
            if item == '__name__' or item == 'active':
                continue
            self.app_select_box.addItem(item)

        # creates the start button
        self.start_btn = QPushButton(self.music_players)
        self.start_btn.setGeometry(75, 120, 250, 35)
        self.start_btn.setText('Start')

        # links the start button to the self.start function
        QObject.connect(self.start_btn, SIGNAL("clicked()"),
                        lambda: Thread(target=self.start, name='startbutton').start())

    def tab_options(self):
        """ Everything inside the Options tab gets created here. """
        # self.options

        # This section is for selecting output dir
        # Creates the output dir label
        self.output_dir_lbl = QLabel(self.options)
        self.output_dir_lbl.setGeometry(10, 10, 125, 15)
        self.output_dir_lbl.setText('Change Output Directory: ')

        # Creates the output dir button
        self.select_output_dir_btn = QPushButton(self.options)
        self.select_output_dir_btn.setGeometry(137, 8, 30, 20)
        self.select_output_dir_btn.setText('...')

        # Creates the output dir currentdir Lineedit
        self.output_cur_dir_lbl = QLineEdit(self.options)
        self.output_cur_dir_lbl.setGeometry(170, 6, 210, 25)
        self.output_cur_dir_lbl.setReadOnly(True)
        self.output_cur_dir_lbl.setText(Constants.CONFIG.
                                        get('directories', 'current_song'))

        # when the '...' button is clicked, show a dialog (fire func
        # disp_dialog)
        QObject.connect(self.select_output_dir_btn, SIGNAL("clicked()"),
                        self.disp_dialog)

        # This section is for selecting what players you use
        # The box with all the active players
        self.active_items_list = QListWidget(self.options)
        self.active_items_list.setGeometry(10, 40, 150, 100)

        # The box with all the inactive players
        self.inactive_items_list = QListWidget(self.options)
        self.inactive_items_list.setGeometry(230, 40, 150, 100)
        # Populate the two boxes with active and inactive items
        for item in Constants.ACTIVEITEMS:
            if item == '__name__' or item == 'active':
                continue
            self.active_items_list.addItem(item)
        for item in Constants.INACTIVEITEMS:
            if item == '__name__' or item == 'active':
                continue
            self.inactive_items_list.addItem(item)

        # The buttons responsible for switching
        # off button
        self.switch_active_item_button_off = QPushButton(self.options)
        self.switch_active_item_button_off.setText('->'.decode('utf-8'))
        # Makes the -> readable and clear
        self.switch_active_item_button_off.setFont(QFont('SansSerif', 17))
        self.switch_active_item_button_off.setGeometry(175, 55, 40, 30)
        # on button
        self.switch_active_item_button_on = QPushButton(self.options)
        self.switch_active_item_button_on.setText('<-'.decode('utf-8'))
        # makes <- readable and clear
        self.switch_active_item_button_on.setFont(QFont('SansSerif', 17))
        self.switch_active_item_button_on.setGeometry(175, 90, 40, 30)

        QObject.connect(self.switch_active_item_button_on, SIGNAL
                       ("clicked()"), self.switch_item_on)
        QObject.connect(self.switch_active_item_button_off, SIGNAL
                       ("clicked()"), self.switch_item_off)

        # A button to toggle the split output in half option. It's a temporary
        # fix for the Foobar double output problem.
        self.switch_output_split_btn = QCheckBox(self.options)
        self.switch_output_split_btn.setCheckState(Qt.CheckState.Unchecked)
        self.switch_output_split_btn.setGeometry(10, 140, 40, 30)
        self.switch_output_split_btn.stateChanged.connect(self.toggle_split)

        # The label for the split toggle
        self.switch_output_split_lbl = QLabel(self.options)
        self.switch_output_split_lbl.setText(
            "Split the output text in half (don't use this if you don't need it)")
        self.switch_output_split_lbl.setGeometry(30, 140, 300, 30)

    def switch_item_on(self):
        """ Switches items (musicapps) on """
        try:
            # If an item from the active box is selected
            # Remove it and place it inside the inactive box
            item_taken = self.inactive_items_list.takeItem(
                self.inactive_items_list.currentRow())
            self.active_items_list.addItem(item_taken)
            active_items = {}
            inactive_items = {}
            for i in range(self.active_items_list.count()):
                active_items[self.active_items_list.item(i).text()] =\
                    ITEMS[self.active_items_list.item(i).text()
                          .encode('utf-8')]
            for i in range(self.inactive_items_list.count()):
                inactive_items[self.inactive_items_list.item(i).text()] =\
                    ITEMS[self.inactive_items_list.item(i).text()
                          .encode('utf-8')]
            Constants.ACTIVE_ITEMS = active_items
            Constants.INACTIVE_ITEMS = inactive_items
            # clear the selection combobox
            self.app_select_box.clear()
            # Repopulate the combobox
            self.app_select_box.addItem(None)
            for item in active_items:
                self.app_select_box.addItem(item)
            Constants.CONFIG.set('active', item_taken.text(),
                                 ITEMS[item_taken.text()])
            Constants.CONFIG.remove_option('inactive', item_taken.text())
            # Updates the config file to be up to date with activeItems
            Constants.CONFIG.update()
        except:
            raise

    def switch_item_off(self):
        """ Switches items (musicapps) off """
        try:
            # If an item from the inactive box is selected.
            # Remove it and place it inside the active box
            item_taken = self.active_items_list.takeItem(
                self.active_items_list.currentRow())
            self.inactive_items_list.addItem(item_taken)
            # update activeItems
            active_items = {}
            inactive_items = {}
            for i in range(self.active_items_list.count()):
                active_items[self.active_items_list.item(i).text()] =\
                    ITEMS[self.active_items_list.item(i).text()
                          .encode('utf-8')]
            for i in range(self.inactive_items_list.count()):
                inactive_items[self.inactive_items_list.item(i).text()] =\
                    ITEMS[self.inactive_items_list.item(i).text()
                          .encode('utf-8')]
            Constants.ACTIVE_ITEMS = active_items
            Constants.INACTIVE_ITEMS = inactive_items
            # clear the selection combobox
            self.app_select_box.clear()
            # Repopulate the combobox
            self.app_select_box.addItem(None)
            for item in active_items:
                self.app_select_box.addItem(item)
            # Updates the active items Constants property
            Constants.CONFIG.set('inactive', item_taken.text(),
                                 ITEMS[item_taken.text()])
            Constants.CONFIG.remove_option('active', item_taken.text())
            # Updates the config file to be up to date with activeItems
            Constants.CONFIG.update()
        except:
            raise

    def disp_dialog(self):
        """  displays the dialog which select a directory for output. """
        fname = QFileDialog.getExistingDirectory()
        Constants.CONFIG.set('directories', 'current_song', fname)
        self.output_cur_dir_lbl.setText(Constants.CONFIG.
                                        get('directories', 'current_song'))

    def select_new_app(self, text):
        """ Sets the new application to check for """
        try:
            Main.selectedProgram = ITEMS[text]
        except KeyError:
            # catches the empty option, it's obviously not in the dict
            pass
        # custom message for zune
        if Main.selectedProgram == 'zune':
            self.misc_messages.setText(Misc.ZuneNotification)
        # custom message for webplayers which require the groovemarklet
        elif text.find('*'):
            self.misc_messages.setText(Misc.GetGroovemarklet)

    def start(self):
        """ When the start button is pressed, start the main program loop """
        if Main.selectedProgram:
            if not Main.running:
                self.start_btn.setText('Stop')
                Main.running = True
                try:
                    pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
                except pythoncom.com_error:
                    # already initialized.
                    pass
                thread = Thread(
                    target=Main.enumWindows, name='enumWindows')
                thread.run()
            else:
                self.start_btn.setText('Start')
                Main.running = False
                self.set_playing(Misc.noSongPlaying)
                Wr.write('')

    def set_playing(self, title=''):
        """ Sets the text of the label of what song is playing """
        # print 'setting title: ', title
        self.current_playing.setText(title)

if __name__ == '__main__':
    initialize()
    pythoncom.CoInitialize()
    APP = QApplication(sys.argv)
    Constants.UI = UiMain()
    sys.exit(APP.exec_())
