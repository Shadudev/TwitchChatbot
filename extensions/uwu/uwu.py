import datetime
import os
import tempfile

from core.framework import configuration
from core.framework.extensions.bases.command_handler import CommandHandler
from core.framework.media_player import MediaPlayer
from extensions.uwu import tts
from extensions.uwu.dynamic_dictionary import DynamicDictionary

COMMAND_ID = '!uwu'

CHARACTER_COOLDOWN_MULTIPLIER = datetime.timedelta(seconds=5)


class UwUHandler(CommandHandler):
    def __init__(self, send_message_func, cooldown_manager):
        super(UwUHandler, self).__init__(send_message_func, cooldown_manager)
        self._tts = tts.UwUTTS()
        self._cooldowns = {}

    def should_handle_message(self, chat_message):
        return self.__is_uwu_redeem(chat_message)

    def is_user_on_cooldown(self, user):
        user_cooldown = self._cooldowns.get(user, 0)
        return self._cooldown_manager.is_on_cooldown(COMMAND_ID, user, user_cooldown) and user != 'shadudev'

    def handle_message(self, chat_message):
        if self.is_user_on_cooldown(chat_message.user):
            user_cooldown = self._cooldowns.get(chat_message.user, 0)
            remaining_cooldown = self._cooldown_manager.get_remaining_cooldown(COMMAND_ID, chat_message.user,
                                                                               user_cooldown).seconds
            self.send_message(
                "{}'s !uwu is on cooldown for {} more seconds".format(chat_message.user, remaining_cooldown))
            return

        text = chat_message.message[5:]

        self._cooldowns[chat_message.user] = len(chat_message.message) * CHARACTER_COOLDOWN_MULTIPLIER
        self._cooldown_manager.set_on_cooldown(COMMAND_ID, chat_message.user)

        uwu_text = self.__translate(text)
        self.send_message('UwU: ' + uwu_text)

        with tempfile.NamedTemporaryFile('wb', delete=False) as output_file:
            self._tts.get_speech(uwu_text, output_file, configuration.get_channel_name())
            MediaPlayer.play(output_file.name, 70)

    def __is_uwu_redeem(self, chat_message):
        command = chat_message.message.split(' ')[0]
        return command == COMMAND_ID and len(chat_message.message) > len(COMMAND_ID)

    def __translate(self, text):
        words = text.split(' ')
        translated_text = []
        for word in words:
            translated_text.append(self.__translate_word(word))

        return ' '.join(translated_text)

    def __translate_word(self, word):
        dictionary = self.__get_dictionary()
        if word.lower() in dictionary:
            return dictionary[word.lower()]

        converted = ""
        doubleT = doubleT_Presence = th_Presence = False
        for i in range(len(word)):
            if doubleT or th_Presence:
                doubleT = th_Presence = False
                continue
            elif ((word[i] == "L" or word[i] == "l") and not doubleT_Presence) or (word[i] == "R" or word[i] == "r"):
                converted += "W" if word[i].isupper() else "w"
            elif (word[i] == "T" or word[i] == "t") and (
            (word[i + (1 if i + 1 < len(word) else 0)] == "T" or word[i + (1 if i + 1 < len(word) else 0)] == "t")):
                converted += (("D" if word[i].isupper() else "d") + (
                    "D" if word[i + 1].isupper() else "d")) if i + 1 < len(word) else "t"
                doubleT = doubleT_Presence = True if i + 1 < len(word) else False
            elif (word[i] == "T" or word[i] == "t") and (
            (word[i + (1 if i + 1 < len(word) else 0)] == "H" or word[i + (1 if i + 1 < len(word) else 0)] == "h")):
                converted += ("F" if word[i].isupper() else "f") if i + 2 == len(word) else "t"
                th_Presence = True if i + 2 == len(word) else False
            else:
                converted += word[i]

        converted = converted.replace("no", "nya")
        converted = converted.replace("mo", "mya")
        converted = converted.replace("No", "Nya")
        converted = converted.replace("Mo", "Mya")
        converted = converted.replace("na", "nya")
        converted = converted.replace("ni", "nyi")
        converted = converted.replace("nu", "nyu")
        converted = converted.replace("ne", "nye")
        converted = converted.replace("anye", "ane")
        converted = converted.replace("inye", "ine")
        converted = converted.replace("onye", "one")
        converted = converted.replace("unye", "une")
        return converted

    def __get_dictionary(self):
        return DynamicDictionary.get_dictionary()
