from core.framework.extensions.bases.command_handler import CommandHandler
from core.framework.media_player import MediaPlayer


COMMAND_ID = '!skip'


class SoundsSkipper(CommandHandler):
    def __init__(self, send_message_func, cooldown_manager):
        super(SoundsSkipper, self).__init__(send_message_func, cooldown_manager)

    def should_handle_message(self, chat_message):
        return chat_message.message == COMMAND_ID and (chat_message.is_mod or chat_message.is_streamer)

    def handle_message(self, chat_message):
        MediaPlayer.skip()
        self.send_message('Skipped!')
