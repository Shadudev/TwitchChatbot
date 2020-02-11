import datetime
import json
import os
import random
import sys

from shutil import copyfile
from modules.command_handler import CommandHandler


ScriptName = COMMAND_ID = '!dad'
COMMAND_REWARD_ID = '799b6367-fc89-4159-8932-d34157150e21'

Website = ''
Description = 'Capable of printing strings from a file in a given folder'
Creator = 'TheShadu'
Version = '1.0.0.0'

SCRIPT_BASE_PATH = os.path.dirname(__file__)
sys.path.append(SCRIPT_BASE_PATH)

JOKES_FOLDER_PATH = os.path.join(SCRIPT_BASE_PATH, 'Jokes')
JOKES_LOG_PATH = os.path.join(SCRIPT_BASE_PATH, 'log.txt')
SETTINGS_FILE_PATH = os.path.join(SCRIPT_BASE_PATH, 'settings.ini')
SETTINGS_BACKUP_FILE_PATH = SETTINGS_FILE_PATH + '.bkp'


COMMAND_COOLDOWN_KEY = 'cooldown'
USER_COOLDOWN_KEY = 'user_cooldown'
MANUAL_COOLDOWN_RESET_KEY = 'cooldown_reset'
PROPERTIES = [COMMAND_COOLDOWN_KEY, USER_COOLDOWN_KEY]
DEFAULT_SETTINGS = {COMMAND_COOLDOWN_KEY: 5, USER_COOLDOWN_KEY: 30 * 60, MANUAL_COOLDOWN_RESET_KEY: False}

ALL_PROPERTIES_MAGIC = '*'
RESET_COOLDOWN_COMMAND = 'reset'
MOD_PERMISSIONS = 'Moderator'


class DadJokesTeller(CommandHandler):
	def __init__(self, send_message_func, cooldown_manager):
		super(DadJokesTeller, self).__init__(send_message_func, cooldown_manager)

		if not os.path.exists(JOKES_FOLDER_PATH):
			os.mkdir(JOKES_FOLDER_PATH)

		if not os.path.exists(SETTINGS_FILE_PATH):
			self.update_settings(DEFAULT_SETTINGS)

		copyfile(SETTINGS_FILE_PATH, SETTINGS_BACKUP_FILE_PATH)

	def should_handle_message(self, chat_message):
		return getattr(chat_message, 'custom_reward_id', None) == COMMAND_REWARD_ID

	def handle_message(self, chat_message):
		if not chat_message.is_mod:
			self._handle_basic_command(chat_message)
		else:
			operation = chat_message.split(' ')[1].lower()
			if operation not in PROPERTIES and operation not in [RESET_COOLDOWN_COMMAND, ALL_PROPERTIES_MAGIC]:
				self._handle_basic_command(chat_message)
			elif operation == RESET_COOLDOWN_COMMAND:
				self._handle_cooldown_reset_command()
			elif 2 == params_count:
				self._handle_get_command(operation)
			else:
				self._handle_set_command(chat_message)

	def _handle_basic_command(self, chat_message):
		if self._is_command_in_cooldown():
			raise 'is_command_in_cooldown'
			#send_message('Command is in cooldown for {} more seconds.'.format(get_remaining_cooldown()))
		elif self._is_user_in_cooldown(chat_message.user):
			raise 'is_user_in_cooldown'
			#send_message('NO {} ! No more for at least {} more seconds!'.format(chat_message.display_name, get_user_remaining_cooldown(chat_message.user)))
		else:
			self._tell_joke()
			#add_command_cooldown()
			#add_user_cooldown(chat_message.user)
			self._set_manual_cooldown_reset(False)


	def _tell_joke(self):
		chosen_file = self._choose_random_file(JOKES_FOLDER_PATH)
		joke = self._pop_joke(os.path.join(JOKES_FOLDER_PATH, chosen_file))
		self.send_message(joke)
		self._log(joke)


	def _choose_random_file(self, path):
		files = list(filter(lambda fname: fname.endswith('.txt'), os.listdir(path)))
		return files[random.randrange(len(files))]
		

	def _pop_joke(self, file_path):
		jokes = eval(self._read_file(file_path))
		index = random.randrange(len(jokes))
		joke = jokes.pop(index)
		#self.write_file(file_path, str(jokes))
		return joke


	def _handle_cooldown_reset_command(self):
		self._set_manual_cooldown_reset(True)
		self._send_message("Cooldown was reset!")


	def _set_manual_cooldown_reset(self, state):
		self._set_property(MANUAL_COOLDOWN_RESET_KEY, state)


	def _get_manual_cooldown_reset(self):
		return bool(self._get_property(MANUAL_COOLDOWN_RESET_KEY))


	def _is_command_in_cooldown(self):
		return False
		#return Parent.IsOnCooldown(COMMAND_ID, '') and not get_manual_cooldown_reset()

	"""
	def get_remaining_cooldown():
		return Parent.GetCooldownDuration(COMMAND_ID, '')

	"""
	def _is_user_in_cooldown(self, user):
		return False
		#return Parent.IsOnUserCooldown(COMMAND_ID, '', user) and not get_manual_cooldown_reset()

	"""
	def get_user_remaining_cooldown(user):
		return Parent.GetUserCooldownDuration(COMMAND_ID, '', user)


	def add_command_cooldown():
		cooldown = get_command_cooldown()
		Parent.AddCooldown(COMMAND_ID, '', cooldown)


	def add_user_cooldown(user):
		user_cooldown = get_user_cooldown()
		Parent.AddUserCooldown(COMMAND_ID, '', user, user_cooldown)
	"""

	def _handle_get_command(self, config_property):
		if config_property == ALL_PROPERTIES_MAGIC:
			config = self._get_properties()
			for property in config.keys():
				if property not in PROPERTIES:
					config.pop(property)
			self.send_message(str(config))
		elif config_property in PROPERTIES:
			self.send_message('{}={}'.format(config_property, self._get_property(config_property)))


	def _handle_set_command(self, chat_message):
		config_property = chat_message.split(' ')[1].lower()
		new_value = chat_message.split(' ')[2].lower()
		
		if config_property not in PROPERTIES:
			self._show_properties()
		else:
			current_value = self._get_property(config_property)
			try:
				new_value = type(current_value)(new_value)
			except:
				self.send_message('Invalid value {}, expected value of type {}'.format(new_value, type(current_value)))
			if current_value != new_value:
				self._set_property(config_property, new_value)
				self.send_message('{} set to {}'.format(config_property, new_value))
			else:
				self.send_message('{} is already {} !'.format(config_property, new_value))


	def _get_command_cooldown(self):
		return self._get_property(COMMAND_COOLDOWN_KEY)


	def _get_user_cooldown(self):
		return self._get_property(USER_COOLDOWN_KEY)


	def _get_property(self, config_property):
		return self._get_properties()[config_property]


	def _get_properties(self):
		return self._read_settings()


	def _set_property(self, config_property, new_value):
		settings = self._read_settings()
		settings[config_property] = new_value
		self._update_settings(settings)


	def _show_properties(self):
		self.send_message("Invalid property. Available properties: {}. Use {} for all properties.".format(make_pretty(PROPERTIES), ALL_PROPERTIES_MAGIC))


	def _make_pretty(self, collection, separator=', '):
		return separator.join(collection)


	def _read_settings(self):
		return self._read_json_from_file(SETTINGS_FILE_PATH)


	def _update_settings(self, settings):
		self._dump_json_to_file(SETTINGS_FILE_PATH, settings)


	def _dump_json_to_file(self, file_path, file_data):
		with open(file_path, 'w', encoding='utf8') as f:
			json.dump(file_data, f, ensure_ascii=False)


	def _read_json_from_file(self, file_path):
		with open(file_path) as f:
			return json.load(f)


	def _read_file(self, path):
		with open(path) as f:
			return f.read()


	def _write_file(self, path, content):
		with open(path, 'w') as f:
			f.write(content)


	def _append_file(self, path, content):
		with open(path, 'a') as f:
			f.write(content+'\n')


	def _log(self, msg):
		self._append_file(JOKES_LOG_PATH, str(datetime.datetime.now()) + ',' + msg)
