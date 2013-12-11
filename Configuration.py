__author__ = 'martijn'
from configparser import ConfigParser
import sys
import os
import GLOBALS


class Configuration(ConfigParser):
    def __init__(self):
        super().__init__()
        self.config_path = os.path.join("config", "config.ini")
        if self.exists():
            self.read_file(open(self.config_path, "r"))

    def set_config_file_path(self, config_path):
        """Set the relative filepath for the configuration file"""
        self.config_path = config_path

    def exists(self):
        """Return if the configuration file exists or not"""
        if os.path.exists(self.config_path):
            return True
        return False

    def save(self):
        """Write the current configuration object (self) to the configuration file."""
        try:
            open(self.config_path, "w")
            with open(self.config_path, "w") as f:
                super().write(f)
        except PermissionError:
            # TODO Error dialog
            print("No permission to write to config file.")
            sys.exit()

    def create_configuration_file(self):
        """Creates the configuration file from defaults"""
        self.default_configuration_file()

    def get_path_to_output_file(self):
        """Returns the path to the current_song.txt file"""
        return os.path.join(self.get("directories", "output_directory"), "current_song.txt")

    def default_configuration_file(self):
        """
        This method is called when the config.ini file needs to be reset
        It creates config.ini with default values.
        """
        import identifiers

        for section in ("directories", "active_players", "inactive_players"):
            self.add_section(section)
        # TODO Rename root_directory and output_directory to root and output
        self["directories"] = {
            "root_directory": GLOBALS.ROOT,
            "output_directory": GLOBALS.ROOT
        }
        self["active_players"] = dict(zip(identifiers.APPS, [app.name for app in identifiers.APPS]))
        print(self["directories"])
        self.save()