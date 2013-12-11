__author__ = 'martijn'
import os
import Configuration
import GLOBALS

configuration = Configuration.Configuration()

class ProgramSkeleton:
    def __init__(self):
        # explanation of self.structure usage
        # "directory": [("filename", error_function), ("secondfilename", error_function),
        # "second_directory": etc
        # If a directory is not found, it will be created.
        # if a file is not found, the error function associated with the file will be called.
        self.structure = {
            "/": [("current_song.txt", self.error_current_song_file)],
            "config": [("music_players.json", self.error_json), ("config.ini", self.error_config)],
            "resources": [("icon-16.png", self.error_resources), ("icon-32.png", self.error_resources)],
        }
        self.root = os.path.abspath(os.path.dirname(__file__))
        self.verify_structure()

    def get_root(self):
        """
        @return: absolute root to this file
        """
        return self.root

    def error_current_song_file(self):
        """Error handler for when current_song.txt is missing, create the file"""
        # TODO Error dialog
        open(os.path.join(self.root, "current_song.txt"), "w", encoding="utf-8")

    def verify_structure(self):
        """Use self.structure to check for all important files and directories.
        If a directory is missing, it will create the directory.
        If a file is missing, it will fire a function associated with that file missing"""
        for directory, files in self.structure.items():
            # creates the directory if it doesn't exist
            if not os.path.exists(directory):
                print("dir ", directory, " doesn't exist, creating.")
                os.makedirs(directory)
            # calls a given function if a file does not exist
            for file, error in files:
                filepath = os.path.join(directory, file)
                if not os.path.exists(filepath):
                    error()

    def error_config(self):
        """Error handler for when config.ini is missing, create the file with a default
        configuration"""
        # TODO Error dialog
        print("configuration file doesn't exist, creating config file")
        configuration.create_configuration_file()

    def error_resources(self):
        """Error handler for when any of the icons is missing, Won't really do anything"""
        # TODO Error dialog
        print("missing icons :(")

    def error_json(self):
        """Error handler for when music_players.json is missing, will create a new one
        with default configuration (located in GLOBALS.MUSIC_PLAYERS_JSON)"""
        # TODO Error dialog
        print("music_players.json file doesn't exist, creating the file")
        with open(os.path.join(self.root, "config", "music_players.json"), "w", encoding="utf-8") as f:
            f.write(GLOBALS.MUSIC_PLAYERS_JSON)