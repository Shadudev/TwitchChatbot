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
		self._tell_joke()


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
		self._write_file(file_path, str(jokes))
		return joke


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
