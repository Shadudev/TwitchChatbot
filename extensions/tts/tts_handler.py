import datetime
import os
import tempfile

from core.framework import configuration
from core.framework.extensions.bases.command_handler import CommandHandler
from core.framework.media_player import MediaPlayer
from extensions.tts import tts


COMMAND_ID = '!tts'

CHARACTER_COOLDOWN_MULTIPLIER = datetime.timedelta(seconds=5)


class TTSHandler(CommandHandler):
    def __init__(self, send_message_func, cooldown_manager):
        super(TTSHandler, self).__init__(send_message_func, cooldown_manager)
        self._tts = tts.TTS()
        self._cooldowns = {}

    def should_handle_message(self, chat_message):
        return self.__is_tts_redeem(chat_message)

    def is_user_on_cooldown(self, user):
        user_cooldown = self._cooldowns.get(user, 0)
        return self._cooldown_manager.is_on_cooldown(COMMAND_ID, user, user_cooldown) and user != 'shadudev'

    def handle_message(self, chat_message):
        if self.is_user_on_cooldown(chat_message.user):
            user_cooldown = self._cooldowns.get(chat_message.user, 0)
            remaining_cooldown = self._cooldown_manager.get_remaining_cooldown(COMMAND_ID, chat_message.user,
                                                                               user_cooldown).seconds
            self.send_message(
                "{}'s !tts is on cooldown for {} more seconds".format(chat_message.user, remaining_cooldown))
            return

        text = chat_message.message[5:]

        self._cooldowns[chat_message.user] = len(chat_message.message) * CHARACTER_COOLDOWN_MULTIPLIER
        self._cooldown_manager.set_on_cooldown(COMMAND_ID, chat_message.user)

        with tempfile.NamedTemporaryFile('wb', delete=False) as output_file:
            self._tts.get_speech(text, output_file, configuration.get_channel_name())
            MediaPlayer.play(output_file.name, 70)

    def __is_tts_redeem(self, chat_message):
        command = chat_message.message.split(' ')[0]
        return command == COMMAND_ID and len(chat_message.message) > len(COMMAND_ID)
