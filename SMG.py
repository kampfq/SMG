__author__ = 'martijn'

import win32gui
import time
from PySide.QtCore import QThread, QObject, Signal

import messages
import ProgramSkeleton
import Configuration
import GLOBALS

programSkeleton = ProgramSkeleton.ProgramSkeleton()
configuration = Configuration.Configuration()

import identifiers


class MainProgramLoop(QObject):
    finished = Signal()

    def __init__(self):
        super().__init__()
        self.running = True

    def long_running(self):
        """Calls smg.enum_windows every GLOBALS.TIMEOFFSET seconds, will emit a finished
        signal when it is stopped."""
        time_now = time.time()
        smg.enum_windows()
        while self.running:
            if time.time() >= time_now + GLOBALS.TIMEOFFSET:
                smg.enum_windows()
                time_now = time.time()
            time.sleep(0.007) # reduces cpu load
        print("Worker finished")
        self.finished.emit()

    def stop(self):
        """Stops the main loop so this worker will emit a finished signal."""
        self.running = False


class SMG(QObject):
    songChanged = Signal()

    def __init__(self):
        super().__init__()
        self.active_programs = []
        self.inactive_programs = []
        self.active_song = messages.messages.no_song_playing
        self.selected_program = None
        self.running = False
        self.thread = QThread()
        self.worker = None

    def select_program(self, app):
        """Sets the currently selected program.
        @param app: an application
        @type app: <type 'App'>
        """
        self.selected_program = app

    def activate_application(self, prog):
        """Activates an application, it can now be called from the smg gui
        It will also write this change to the config file
        @param prog: a program
        @type prog: <type 'App'>
        """
        self.active_programs.append(prog)
        if prog in self.inactive_programs:
            # If it's in inactive programs, remove it.
            self.inactive_programs.pop(self.inactive_programs.index(prog))
        configuration["active_players"][prog.gui_name] = prog.name
        configuration.remove_option("inactive_players", prog.gui_name)
        configuration.save()

    def deactivate_application(self, prog):
        """
        Deactivates an application, this means that it cannot be called from the smg gui
        It will also write this change to the config file
        @param: prog is a program of <type 'App'>
        """
        self.inactive_programs.append(prog)
        if prog in self.active_programs:
            # If it's in active programs, remove it.
            self.active_programs.pop(self.active_programs.index(prog))
        configuration["inactive_players"][prog.gui_name] = prog.name
        configuration.remove_option("active_players", prog.gui_name)
        configuration.save()

    def start(self):
        """Start enumerating over windows"""
        self.worker = MainProgramLoop()
        self.worker.moveToThread(self.thread)
        self.worker.finished.connect(self.thread.quit)
        self.thread.started.connect(self.worker.long_running)
        self.thread.start()

    def stop(self):
        """Stop enumerating over windows"""
        self.worker.stop()
        self.write(messages.messages.no_song_playing)

    def enum_windows(self):
        """Enumerate over all windows, calls self.examine_window"""
        win32gui.EnumWindows(self.examine_window, None)

    def toggle_running(self):
        """
        Toggle the running variable on or off, and call self.stop or self.start accordingly.
        """
        if self.running:
            self.stop()
        else:
            self.start()
        self.running = not self.running

    def write(self, title):
        """
        Write a string to the current_song.txt file
        If the song name changed from last tick, Emit a signal that the song name has changed.
        @param title: The title to write
        """
        # title may also be empty string
        if title:
            filepath = configuration.get_path_to_output_file()
            # It shouldn't write to the file if the title is the same as the one in the file
            if not self.read() == title:
                print(self.read(), title, self.read() == title)
                self.active_song = title
                self.songChanged.emit()
                print("Emitted change song")
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(title)

    @staticmethod
    def read():
        """ Reads and returns what's in the current_song.txt"""
        filepath = configuration.get_path_to_output_file()
        try:
            with open(filepath, encoding="utf-8") as f:
                string = f.read()
                return string
        except IOError:
            pass

    def examine_window(self, hwnd, extra):
        """
        This function will be called for each window the win32gui.EnumWindows can find.
        It takes the window's title and the window's classname and matches it against
        a function associated with the currently selected program.
        If it matches, it will call write to update the title in the gui and in the file.

        @param hwnd: A window handle ID
        @param extra: This is a parameter required by win32gui.EnumWindows, it probably has something to do
        with lower programming languages, here we don't need it, so we don't use it.
        """
        window_title = win32gui.GetWindowText(hwnd)
        window_class = win32gui.GetClassName(hwnd)
        title = ""

        if self.selected_program.type == "misc_music_player":
            title = self.selected_program.identify()
        elif self.selected_program.type == "music_player":
            title = self.selected_program.identify(window_title, window_class)
        elif self.selected_program.type == "web_music_player":
            for browser in identifiers.BROWSERS:
                browser_title = browser.identify(window_title, window_class)
                if browser_title:
                    title = self.selected_program.identify(browser_title, window_class)
        if title:
            self.write(title)

    @staticmethod
    def find_application_by_name(name):
        """
        Looks for an application by name. Will return the application if it's found.
        @param name: The name of an <type 'App'> to find
        @type name: <type 'String'>
        @return: An application
        @rtype: <type 'App'>
        """
        for application in identifiers.APPS:
            if name == application.name:
                return application


smg = SMG()
for program in configuration["active_players"].values():
    smg.activate_application(smg.find_application_by_name(program))

for program in configuration["inactive_players"].values():
    smg.deactivate_application(smg.find_application_by_name(program))