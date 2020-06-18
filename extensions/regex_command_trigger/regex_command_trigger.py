import datetime
import os
import re
from core.framework.extensions.bases.command_handler import CommandHandler
from core.framework.media_player import MediaPlayer


SCRIPT_BASE_PATH = os.path.dirname(__file__)
SOUNDS_FOLDER_PATH = os.path.join(SCRIPT_BASE_PATH, 'Sounds')
BLOWER_SOUND_PATH = os.path.join(SOUNDS_FOLDER_PATH, 'blower.mp3')


class RegexCommandTrigger(CommandHandler):
	def __init__(self, send_message_func, cooldown_manager):
		super(RegexCommandTrigger, self).__init__(send_message_func, cooldown_manager)

	def should_handle_message(self, chat_message):
		return self.get_matching_regex_trigger(chat_message)
		
	def get_matching_regex_trigger(self, chat_message):
		for regex in self.REGEX_TRIGGERS:
			if re.match(regex, chat_message.message):
				return regex
		return None

	def handle_message(self, chat_message):
		regex = self.get_matching_regex_trigger(chat_message)

		if not self._cooldown_manager.is_on_cooldown(regex, chat_message.user, datetime.timedelta(seconds=10)):
			self._cooldown_manager.set_on_cooldown(regex, chat_message.user)
			self.trigger_command(chat_message, regex)

	def trigger_command(self, chat_message, regex):
		self.REGEX_TRIGGERS[regex](self, chat_message, regex)
		
	def blower(self, chat_message, regex):
		match = re.match(regex, chat_message.message).group(1)
		self.send_message('{channel} said {match}!'.format(channel=chat_message.display_name, match=match))
		MediaPlayer.play(BLOWER_SOUND_PATH, 80)

	REGEX_TRIGGERS = {'.*(happy|grats|versary).*': blower}
