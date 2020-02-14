import datetime
from modules.command_handler import CommandHandler
from scripts.soundbot import settings
from utils import api_requests

SOUND_ID_INDEX = 0
MOD_OPERATION_INDEX = PROPERTY_INDEX = 1
VALUE_INDEX = 2

ALL_MAGIC = '*'

DISABLE_ALL_COMMAND = 'sounds mute'
ENABLE_ALL_COMMAND = 'sounds unmute'
TOGGLE_ALL_COMMAND = 'sounds toggle'


class DynamicSettingsHandler(CommandHandler):
	def __init__(self, send_message_func, cooldown_manager, settings):
		super(DynamicSettingsHandler, self).__init__(send_message_func, cooldown_manager)
		self._settings = settings

	def is_get_command(self, command_args):
		if len(command_args) < 2:
			return False
		return self._settings.does_sound_exist(command_args[SOUND_ID_INDEX]) and self._settings.does_property_exist(command_args[PROPERTY_INDEX].lower())

	def is_set_command(self, command_args):
		if len(command_args) < 3:
			return False
		return self.is_get_command(command_args) and self._settings.is_property_settable(command_args[PROPERTY_INDEX])

	def is_mod_command(self, command_args):
		if self.is_get_command(command_args):
			return True
		if len(command_args) > MOD_OPERATION_INDEX and command_args[MOD_OPERATION_INDEX].lower() in DynamicSettingsHandler.MOD_OPERATIONS:
			return True
		if len(command_args) == 2 and ' '.join(command_args) in DynamicSettingsHandler.ALL_SOUNDS_COMMANDS_HANDLERS:
			return True
		return False

	def handle_mod_command(self, command_args):
		command_line = ' '.join(command_args)
		if command_line in DynamicSettingsHandler.ALL_SOUNDS_COMMANDS_HANDLERS:
			DynamicSettingsHandler.ALL_SOUNDS_COMMANDS_HANDLERS[command_line](self)
		elif self.is_set_command(command_args):
			self.handle_set_command(command_args)
		elif self.is_get_command(command_args):
			self.handle_get_command(command_args)
		else:
			DynamicSettingsHandler.MOD_OPERATIONS[command_args[MOD_OPERATION_INDEX]](self, command_args)

	def handle_get_command(self, command_args):
		sound_id = command_args[SOUND_ID_INDEX]
		property_key = command_args[PROPERTY_INDEX]

		if property_key == ALL_MAGIC:
			self.send_message('{}={}'.format(sound_id, self._settings.get_properties(property_key)))
		else:
			self.send_message('{}.{}={}'.format(sound_id, property_key, self._settings.get_property(sound_id, property_key)))

	def handle_set_command(self, command_args):
		sound_id = command_args[SOUND_ID_INDEX]
		property_key = command_args[PROPERTY_INDEX]
		new_value = command_args[VALUE_INDEX]

		if not self.is_valid_property_value(sound_id, property_key, new_value):
			self.send_message('Invalid value "{}" for `{}`.'.format(new_value, property_key))
		else:
			self._settings.set_property(sound_id, property_key, new_value)
			self.send_message('{}.{} was set to {}'.format(sound_id, property_key, new_value))

	def is_valid_property_value(self, sound_id, property_key, new_value):
		old_value = self._settings.get_property(sound_id, property_key)

		if type(old_value) != type(new_value):
			try:
				if type(old_value) == bool:
					new_value = new_value == str(True).lower()
				new_value = type(old_value)(new_value)
			except:
				return False
		return True		
	
	def enable_sound(self, command_args):
		sound_id = command_args[SOUND_ID_INDEX]
		self._settings.set_enabled_status(sound_id, True)
		self.send_message('{} has been enabled!'.format(sound_id))

	def disable_sound(self, command_args):
		sound_id = command_args[SOUND_ID_INDEX]
		self._settings.set_enabled_status(sound_id, False)
		self.send_message('{} has been disabled!'.format(sound_id))

	def allow_category(self, command_args):
		sound_id = command_args[SOUND_ID_INDEX]
		current_category = api_requests.get_stream_category()
		self._settings.remove_category_from_unallowed_list(sound_id, current_category)
		self.send_message('{} is now allowed on {}'.format(sound_id, current_category))
	
	def unallow_category(self, command_args):
		sound_id = command_args[SOUND_ID_INDEX]
		current_category = api_requests.get_stream_category()
		self._settings.add_category_from_unallowed_list(sound_id, current_category)
		self.send_message('No more {}s when doing "{}"'.format(sound_id, current_category))

	def disable_all_sounds(self):
		self._settings.set_general_enabled_status(False)
		self.send_message('All sounds have been disabled.')

	def enable_all_sounds(self):
		self._settings.set_general_enabled_status(True)
		self.send_message('All sounds have been enabled.')

	def toggle_all_sounds(self):
		if self._cooldown_manager.is_on_cooldown('!toggle', '', datetime.timedelta(seconds=5)):
			return

		self._cooldown_manager.set_on_cooldown('!toggle', '')
		current_status = self._settings.are_sounds_enabled()
		if current_status:
			self.disable_all_sounds()
		else:
			self.enable_all_sounds()

	MOD_OPERATIONS = {'allow': allow_category, 'unallow': unallow_category, 
				  	  'enable': enable_sound, 'disable': disable_sound}
	ALL_SOUNDS_COMMANDS_HANDLERS = {DISABLE_ALL_COMMAND: disable_all_sounds, ENABLE_ALL_COMMAND: enable_all_sounds,
	                                TOGGLE_ALL_COMMAND: toggle_all_sounds}
