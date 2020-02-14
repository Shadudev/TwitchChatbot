from modules.command_handler import CommandHandler
from scripts.soundbot.dynamic_settings_handler import DynamicSettingsHandler
from scripts.soundbot.settings import SoundbotSettings
from scripts.soundbot.sound_player import SoundPlayer
from utils import api_requests


class Soundbot(CommandHandler):
	def __init__(self, send_message_func, cooldown_manager):
		super(Soundbot, self).__init__(send_message_func, cooldown_manager)
		self._settings = SoundbotSettings()
		self._settings_handler = DynamicSettingsHandler(send_message_func, cooldown_manager, self._settings)
		self._player = SoundPlayer()

	def should_handle_message(self, chat_message):
		command = chat_message.message.split(' ')[0]
		return self._settings.does_sound_exist(command.lstrip('!')) or command in Soundbot.LIST_COMMAND_HANDLERS
			
	def handle_message(self, chat_message):
		if chat_message.is_mod or chat_message.is_streamer:
			command_args = chat_message.message.lstrip('!').split(' ')
			if self._settings_handler.is_mod_command(command_args):
				self._settings_handler.handle_mod_command(command_args)
			else:
				self._handle_simple_command(chat_message)
		else:
			self._handle_simple_command(chat_message)

	def _handle_simple_command(self, chat_message):
		command = chat_message.message.split(' ')[0]
		if command in Soundbot.LIST_COMMAND_HANDLERS:
			Soundbot.LIST_COMMAND_HANDLERS[command](self, chat_message)
		else:
			self.handle_play_command(chat_message)

	def _get_sound_name(self, chat_message):
		return chat_message.message.lstrip('!').split(' ')[0]

	def list_allowed_sounds(self, chat_message):
		current_category = api_requests.get_stream_category()
		self.send_message("Allowed sounds: {}".format(self._get_allowed_sounds(current_category)))

	def list_all_sounds(self, chat_message):
		self.send_message("All existing sounds: {}".format(self._get_all_sounds()))

	def _get_allowed_sounds(self, category):
		return self.make_pretty(self._settings.get_allowed_sounds(category))

	def _get_all_sounds(self):
		return self.make_pretty(self._settings.get_existing_sounds())

	def make_pretty(self, collection, separator=', '):
		return separator.join(collection)

	def handle_play_command(self, chat_message):
		current_category = api_requests.get_stream_category()
		sound_id = self._get_sound_name(chat_message)
		sound_cooldown = self._settings.get_cooldown(sound_id)

		if not self._settings.are_sounds_enabled():
			self.send_message('All sounds are currently disabled')

		elif not self._settings.is_sound_enabled(sound_id):
			self.send_message('{} is disabled.'.format(sound_id))

		elif not self._settings.is_sound_allowed(sound_id, current_category):
			self.send_message('{} is not allowed while playing {}'.format(sound_id, current_category))

		elif self._cooldown_manager.is_on_cooldown(sound_id, '', sound_cooldown):
			remaining_cooldown = self._cooldown_manager.get_remaining_cooldown(sound_id, '', sound_cooldown).seconds
			self.send_message('{} is on cooldown for {} more seconds'.format(sound_id, remaining_cooldown))			

		else:
			self._cooldown_manager.set_on_cooldown(sound_id, '')
			self.play_sound(sound_id)

	def play_sound(self, sound_id):
		sound_path = self._settings.get_sound_path(sound_id)
		volume = self._settings.get_volume(sound_id)
		self._player.play(sound_path, volume=volume)


	LIST_COMMAND_HANDLERS = {'!sounds': list_allowed_sounds, '!allsounds': list_all_sounds}
