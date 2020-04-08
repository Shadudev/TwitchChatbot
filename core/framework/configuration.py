import contextlib
import json
import os

SCRIPT_BASE_PATH = os.getcwd()
DATA_FOLDER_PATH = os.path.join(SCRIPT_BASE_PATH, 'data')
OAUTH_FILE_NAME = 'oauth.txt'
CONFIG_FILE_NAME = 'config.json'
BACKUP_FILE_EXTENSION = '.bkp'
PRIVATE_DEFAULTS = {}

OAUTH_FILE_PATH = os.path.join(DATA_FOLDER_PATH, OAUTH_FILE_NAME)
CONFIG_FILE_PATH = os.path.join(DATA_FOLDER_PATH, CONFIG_FILE_NAME)


def initialize(script_defaults={}):
	default_config = script_defaults.copy()
	default_config.update(PRIVATE_DEFAULTS)
	if not os.path.exists(CONFIG_FILE_PATH):
		update_config(default_config)


def read_file(file_path):
	with open(file_path) as f:
		return f.read()


CHANNEL_PROPERTY_KEY = 'channel'
CONNECTION_PARAMETERS = {
	'host': "irc.twitch.tv",
	'port': 6667,
	'oauth_pass': read_file(OAUTH_FILE_PATH),
	'username': "ShaduDevBot",
	CHANNEL_PROPERTY_KEY: "shadudev"
}


def get_channel_name():
	return CONNECTION_PARAMETERS[CHANNEL_PROPERTY_KEY]


def get_value(config_key, default_value):
	with current_config() as config:
		return config.get(config_key, default_value)


def set_value(config_key, new_value):
	with current_config() as config:
		current_value = config[config_key]
		new_value = type(current_value)(new_value)
		config[config_key] = new_value


@contextlib.contextmanager
def current_config():
	config = read_config()
	yield config
	update_config(config)


def read_config():
	return read_json_from_file(CONFIG_FILE_PATH)


def read_json_from_file(file_path):
	return json.loads(read_file(file_path))


def update_config(config):
	dump_json_to_file(CONFIG_FILE_PATH, config)


def dump_json_to_file(file_path, data):
	with open(file_path, 'w') as f:
		json.dump(data, f)
