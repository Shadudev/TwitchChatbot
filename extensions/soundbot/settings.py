import contextlib
import json
import os
from datetime import timedelta
from shutil import copyfile


SCRIPT_BASE_PATH = os.path.dirname(__file__)
SOUNDS_FOLDER_PATH = os.path.join(SCRIPT_BASE_PATH, 'Sounds')
SETTINGS_FILE_PATH = os.path.join(SCRIPT_BASE_PATH, 'settings.ini')
SETTINGS_BACKUP_FILE_PATH = SETTINGS_FILE_PATH + '.bkp'

COOLDOWN_KEY = 'cooldown'
ENABLED_KEY = 'enabled'
UNALLOWED_GAMES_KEY = 'unallowed_categories'
VOLUME_KEY = 'volume'
SETTABLE_PROPERTIES = [VOLUME_KEY, COOLDOWN_KEY]
ALL_PROPERTIES = [ENABLED_KEY, UNALLOWED_GAMES_KEY] + SETTABLE_PROPERTIES

DEFAULT_SETTINGS = {COOLDOWN_KEY: 300, VOLUME_KEY: 80, UNALLOWED_GAMES_KEY: [], ENABLED_KEY: True}


class SoundbotSettings(object):
	def __init__(self):
		self.initialize_resources()
		self._general_enabled_status = True

	def initialize_resources(self):
		if not os.path.exists(SOUNDS_FOLDER_PATH):
			os.mkdir(SOUNDS_FOLDER_PATH)

		if not os.path.exists(SETTINGS_FILE_PATH):
			self.update_settings({})

		copyfile(SETTINGS_FILE_PATH, SETTINGS_BACKUP_FILE_PATH)

	def get_sound_path(self, sound_name):
		return os.path.join(SOUNDS_FOLDER_PATH, sound_name + '.mp3')

	def does_sound_exist(self, sound_id):
		return sound_id in self.get_existing_sounds()

	def get_existing_sounds(self):
		return [os.path.splitext(file_name)[0] for file_name in os.listdir(SOUNDS_FOLDER_PATH)]

	def does_property_exist(self, property_key):
		return property_key in ALL_PROPERTIES

	def is_property_settable(self, property_key):
		return property_key in SETTABLE_PROPERTIES

	def get_allowed_sounds(self, category):
		existing_sounds = self.get_existing_sounds()
		allowed_sounds = []
		for sound_id in existing_sounds:
			if self.is_sound_allowed(sound_id, category) and self.is_sound_enabled(sound_id):
				allowed_sounds.append(sound_id)
		return allowed_sounds

	def is_sound_allowed(self, sound_id, category):
		unallowed_categories = self.get_unallowed_categories(sound_id)
		for unallowed_category in unallowed_categories:
			if category.lower() == unallowed_category.lower():
				return False 
		return True

	def get_unallowed_categories(self, sound_id):
		return self.get_property(sound_id, UNALLOWED_GAMES_KEY)

	def is_sound_enabled(self, sound_id):
		return bool(self.get_property(sound_id, ENABLED_KEY))
	
	def get_volume(self, sound_id):
		return int(self.get_property(sound_id, VOLUME_KEY))

	def get_cooldown(self, sound_id):
		return timedelta(seconds=self.get_property(sound_id, COOLDOWN_KEY))

	def set_enabled_status(self, sound_id, status):
		self.set_property(sound_id, ENABLED_KEY, status)

	def are_sounds_enabled(self):
		return self._general_enabled_status

	def set_general_enabled_status(self, status):
		self._general_enabled_status = status

	def add_category_from_unallowed_list(self, sound_id, category):
		unallowed_categories = self.get_property(sound_id, UNALLOWED_GAMES_KEY)
		unallowed_categories.append(category)
		self.set_property(sound_id, UNALLOWED_GAMES_KEY, unallowed_categories)

	def remove_category_from_unallowed_list(self, sound_id, category):
		unallowed_categories = self.get_property(sound_id, UNALLOWED_GAMES_KEY)
		if category in unallowed_categories:
			unallowed_categories.remove(category)
			self.set_property(sound_id, UNALLOWED_GAMES_KEY, unallowed_categories)

	def get_properties(self, sound_id):
		sound_properties = {}
		for property_key in PROPERTIES:
			sound_properties[property_key] = self.get_property(sound_id, property_key)
		return sound_properties
			
	def get_property(self, sound_id, property_key):
		with self.current_settings() as settings:
			if sound_id in settings and property_key in settings[sound_id]:
				return settings[sound_id][property_key]
		return DEFAULT_SETTINGS[property_key]

	def set_property(self, sound, property_key, new_value):
		with self.current_settings() as settings:
			if sound not in settings:
				settings[sound] = {}
			settings[sound][property_key] = new_value

	@contextlib.contextmanager
	def current_settings(self):
		settings = self.read_settings()
		yield settings
		self.update_settings(settings)

	def read_settings(self):
		return self.read_json_from_file(SETTINGS_FILE_PATH)

	def read_json_from_file(self, file_path):
		with open(file_path) as f:
			return json.load(f)

	def update_settings(self, settings):
		self.dump_json_to_file(SETTINGS_FILE_PATH, settings)

	def dump_json_to_file(self, file_path, data):
		with open(file_path, 'w', encoding='utf8') as f:
			json.dump(data, f, ensure_ascii=False)
