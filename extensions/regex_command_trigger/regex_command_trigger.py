import datetime
import os
import re

from core.framework.extensions.bases.command_handler import CommandHandler
from core.framework.media_player import MediaPlayer

SCRIPT_BASE_PATH = os.path.dirname(__file__)
SOUNDS_FOLDER_PATH = os.path.join(SCRIPT_BASE_PATH, 'Sounds')
BLOWER_SOUND_PATH = os.path.join(SOUNDS_FOLDER_PATH, 'blower.mp3')

DELETE_MESSAGE_FORMAT = '/delete {message_id}'


class RegexCommandTrigger(CommandHandler):
    def __init__(self, send_message_func, cooldown_manager):
        super(RegexCommandTrigger, self).__init__(send_message_func, cooldown_manager)
        self.PATTERNS_TRIGGERS = {blower_trigger_word: [self.__blower] for blower_trigger_word in
                         ['happy', 'grats', 'versary', 'bday', 'birthday', 'b\\-day']}
        self.PATTERNS_TRIGGERS.update({'bigfollows': [self.__delete_message]})

    def should_handle_message(self, chat_message):
        return self.__get_matching_patterns(chat_message)

    def handle_message(self, chat_message):
        patterns = self.__get_matching_patterns(chat_message)
        for pattern in patterns:
            if not self._cooldown_manager.is_on_cooldown(pattern, chat_message.user, datetime.timedelta(seconds=10)):
                self._cooldown_manager.set_on_cooldown(pattern, chat_message.user)
                self.__trigger_command(chat_message, pattern)

    def __get_matching_patterns(self, chat_message):
        matching_regexes = []
        for pattern in self.PATTERNS_TRIGGERS:
            if re.match(pattern, chat_message.message.lower()):
                matching_regexes.append(pattern)
        return matching_regexes

    def __trigger_command(self, chat_message, pattern):
        for trigger in self.PATTERNS_TRIGGERS.get(pattern, []):
            trigger(self, chat_message, pattern)

    def __blower(self, chat_message, pattern):
        match = re.match(pattern, chat_message.message.lower()).group(1)
        self.send_message('{channel} said {match}!'.format(channel=chat_message.display_name, match=match))
        MediaPlayer.play(BLOWER_SOUND_PATH, 80)

    def __delete_message(self, chat_message, pattern):
        self.send_message(DELETE_MESSAGE_FORMAT.format(message_id=chat_message.message_id))


