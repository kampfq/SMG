#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

from PySide.QtGui import QMainWindow, QLineEdit, QTabWidget, QApplication, \
    QIcon, QFrame, QLabel, QComboBox, QPushButton, QDialog, QListWidget, QFont, QFileDialog
from messages import messages
import GLOBALS
import SMG


class ErrorDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UiOptionsFrame(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # This section is for selecting output dir
        #Creates the output dir label
        self.output_dir_lbl = QLabel(self)
        self.output_dir_lbl.setGeometry(10, 10, 125, 15)
        self.output_dir_lbl.setText('Change Output Directory: ')

        #Creates the output dir button
        self.select_output_dir_btn = QPushButton(self)
        self.select_output_dir_btn.setGeometry(137, 8, 30, 20)
        self.select_output_dir_btn.setText('...')

        #Creates the output dir currentdir Lineedit
        self.output_cur_dir_lbl = QLineEdit(self)
        self.output_cur_dir_lbl.setGeometry(170, 6, 210, 25)
        self.output_cur_dir_lbl.setReadOnly(True)
        self.output_cur_dir_lbl.setText(SMG.configuration["directories"]["output_directory"])

        #when the '...' button is clicked, show a dialog (fire func disp_dialog)
        self.select_output_dir_btn.clicked.connect(self.disp_dialog)

        # This section is for selecting what players you use
        # The box with all the active players
        self.active_items_list = QListWidget(self)
        self.active_items_list.setGeometry(10, 40, 150, 100)

        # The box with all the inactive players
        self.inactive_items_list = QListWidget(self)
        self.inactive_items_list.setGeometry(230, 40, 150, 100)
        # Populate the two boxes with active and inactive items
        for item in SMG.smg.active_programs:
            self.active_items_list.addItem(item.name)
        for item in SMG.smg.inactive_programs:
            self.inactive_items_list.addItem(item.name)

        #The buttons responsible for switching
        #off button
        self.switch_active_item_button_off = QPushButton(self)
        self.switch_active_item_button_off.setText('->')
        #Makes the -> readable and clear
        self.switch_active_item_button_off.setFont(QFont('SansSerif', 17))
        self.switch_active_item_button_off.setGeometry(175, 55, 40, 30)
        #on button
        self.switch_active_item_button_on = QPushButton(self)
        self.switch_active_item_button_on.setText('<-')
        #makes <- readable and clear
        self.switch_active_item_button_on.setFont(QFont('SansSerif', 17))
        self.switch_active_item_button_on.setGeometry(175, 90, 40, 30)

        self.switch_active_item_button_on.clicked.connect(self.switch_item_on)
        self.switch_active_item_button_off.clicked.connect(self.switch_item_off)

    def disp_dialog(self):
        """  displays the dialog which selects a directory for output. """
        fname = QFileDialog().getExistingDirectory()
        SMG.configuration["directories"]["output_directory"] = fname
        self.output_cur_dir_lbl.setText(fname)
        SMG.configuration.save()

    def switch_item_on(self):
        """Takes an item from the inactive items box, and places it in the active items box.
        Also activates this item via smg.activate_application"""
        item = self.inactive_items_list.takeItem(self.inactive_items_list.currentRow())
        application = SMG.smg.find_application_by_name(item.text())

        # Saves changes to file
        SMG.smg.activate_application(application)
        self.active_items_list.addItem(item)

    def switch_item_off(self):
        """Takes an item from the active items box, and places it in the inactive items box.
        Also deactivates this item via smg.deactivate_application"""
        item = self.active_items_list.takeItem(self.active_items_list.currentRow())
        application = SMG.smg.find_application_by_name(item.text())

        # Saves changes to file
        SMG.smg.deactivate_application(application)
        self.inactive_items_list.addItem(item)


class UiMusicPlayersFrame(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Creates the box with all the music players inside of it
        self.app_select_box = QComboBox(self)
        self.app_select_box.setGeometry(135, 10, 150, 25)
        # Whenever you change the application, it runs the selectnewapp func
        self.app_select_box.activated[str].connect(self.select_new_app)

        # Creates the label for the selection combobox
        self.selector_lbl = QLabel(self)
        self.selector_lbl.setGeometry(10, 10, 150, 25)
        self.selector_lbl.setText('Select your music player: ')

        # Creates the label for the current playing song (and the current
        # playing song label)
        self.current_playing_lbl = QLabel(self)
        self.current_playing_lbl.setGeometry(10, 45, 150, 25)
        self.current_playing_lbl.setText('Current playing song: ')

        self.current_playing = QLabel(self)
        self.current_playing.setGeometry(117, 45, 250, 25)
        self.current_playing.setText(messages.no_song_playing)

        # Creates a label which displays any additional messages
        self.misc_messages = QLabel(self)
        self.misc_messages.setGeometry(10, 80, 390, 24)
        self.misc_messages.setText(messages.random_message())
        self.misc_messages.setOpenExternalLinks(True)

        # adds all the music players into the combobox
        self.app_select_box.addItem(None)
        for program in SMG.smg.active_programs:
            self.app_select_box.addItem(program.name)
            # creates the start button
        self.start_btn = QPushButton(self)
        self.start_btn.setGeometry(75, 120, 250, 35)
        self.start_btn.setText('Start')

        self.start_btn.clicked.connect(self.start)
        SMG.smg.songChanged.connect(self.change_song)

    def change_song(self):
        """Sets the current playing song in the gui"""
        self.current_playing.setText(SMG.smg.active_song)

    def start(self):
        """Called when the start button is clicked, will start or stop the program
        depending on what it was previously doing, also alters the start button text"""
        if SMG.smg.selected_program:
            if not SMG.smg.running:
                self.start_btn.setText('Stop')
            else:
                self.start_btn.setText('Start')
            SMG.smg.toggle_running()

    def select_new_app(self, programName):
        """ Sets the new application to check for """
        program = SMG.smg.find_application_by_name(programName)
        SMG.smg.select_program(program)
        # custom message for webplayers which require the groovemarklet
        if program.type == "web_music_player":
            self.misc_messages.setText(messages.get_groovemarklet)


class UiMain(QMainWindow):
    def __init__(self):
        super().__init__()

        # initialize the main window
        self.setWindowTitle('SMG - By Azeirah v' + str(GLOBALS.VERSION))
        self.resize(400, 250)

        # Sets the icon
        self.setWindowIcon(QIcon(os.path.join(os.getcwd(), "resources\icon-16.png")))

        self.tabbed_windows = QTabWidget(self)
        self.tabbed_windows.resize(400, 300)

        # tab 1, contains music player selection
        self.music_players = UiMusicPlayersFrame()

        # tab 2, contains options
        self.options = UiOptionsFrame()

        # links the two tabs
        self.tabbed_windows.addTab(self.music_players, "Music players")
        self.tabbed_windows.addTab(self.options, "Options")

        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    UI = UiMain()
    sys.exit(app.exec_())