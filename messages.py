__author__ = 'martijn'

from random import choice
from collections import namedtuple

_MessagesContainer = namedtuple("messages", ["no_song_playing",
                                             "get_groovemarklet",
                                             "visit_forums",
                                             "all_messages"])


class Messages(_MessagesContainer):
    """Container for some nice and sometimes helpful messages to the user."""
    def random_message(self):
        """Return a random message from all the messages this container contains.
        Except for the first message, No song is currently playing."""
        message = choice(self[1:]) # start from the second message
        if type(message) == list:
            return choice(message)

        return message


messages = Messages(
    "No song is currently playing",

    "Don't forget to get the " +
    "<a href='http://www.league-insanity.tk/Azeirah_content'>" +
    "Groovemarklet</a> for programs marked with an *",

    "Stop by the forums if you need any additional help. <a " +
    "href=" +
    "'http://www.obsproject.com/forum/viewtopic.php?f=22&t=4223'>OBS</a>," +
    "<a href='http://www.xsplit.com/forum/viewtopic.php?f=18&t=20331'> XSplit" +
    "</a>.",
    ["Have a nice day!",
     "Have any suggestions? Stop by the <a href=" +
     "'http://www.obsproject.com/forum/viewtopic.php?f=22&t=4223'>" +
     "obsforums</a> or send me an email.",
     "Found a bug? Send me an email.",
     "Your player isn't supported? Send me an email.",
     "Have a good day! :)",
     "Thanks for using my program.",
     "This program was made by Azeirah.",
     "Current webbrowsers supported are Google Chrome and Firefox.",
     "If you'd like to leave a donation <a href=" +
     "'http://www.league-insanity.tk/Azeirah_content/donate.html'>" +
     "you can do so here</a>",
     "You can enable/disable music apps in the Options tab!",
     "You can change your output directory in the Options tab!"]
)