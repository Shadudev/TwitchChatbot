import datetime
import os
import random
import re
from time import sleep

from core.framework.extensions.bases.command_handler import CommandHandler
from core.framework.media_player import MediaPlayer

SCRIPT_BASE_PATH = os.path.dirname(__file__)
SOUNDS_FOLDER_PATH = os.path.join(SCRIPT_BASE_PATH, 'Sounds')

BLOWER_SOUND_PATH = os.path.join(SOUNDS_FOLDER_PATH, 'blower.mp3')
BLOWER_TRIGGER_WORDS = ['happy', 'congratulations', 'congrats', 'grats', 'versary', 'bday', 'birthday', 'penis', 'diack', 'sosej', 'hotdug', 'hotduggy', '50percentgravy']
SEPARATE_WORDS_PATTERN = '[\\w]+'

DELETE_MESSAGE_FORMAT = '/delete {message_id}'


class RegexCommandTrigger(CommandHandler):
    def __init__(self, send_message_func, cooldown_manager):
        super(RegexCommandTrigger, self).__init__(send_message_func, cooldown_manager)
        self.PATTERNS_TRIGGERS = {
            '.*({words}).*'.format(words='|'.join(BLOWER_TRIGGER_WORDS)): [self.__blower],
            'bigfollows': [self.__delete_message]
        }

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
            trigger(chat_message, pattern)

    def __blower(self, chat_message, pattern):
        words = re.findall(SEPARATE_WORDS_PATTERN, chat_message.message)
        found_words = list(filter(lambda word: word in BLOWER_TRIGGER_WORDS, words))

        matches_str = ', '.join(found_words[:-1])
        if len(matches_str) > 1:
            matches_str += ' and '
        matches_str += found_words[-1]
        self.send_message('{user} said {matches_str}!'.format(user=chat_message.display_name, matches_str=matches_str))
        for i in range(len(found_words)):
            MediaPlayer.play(BLOWER_SOUND_PATH, 45, sync=False)
            sleep(0.1 * random.randrange(1, 4))

    def __delete_message(self, chat_message, pattern):
        self.send_message(DELETE_MESSAGE_FORMAT.format(message_id=chat_message.message_id))
