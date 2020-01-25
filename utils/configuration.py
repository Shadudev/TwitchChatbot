import contextlib
import json
import os


DATA_FOLDER_PATH = 'data'
OAUTH_FILE_NAME = 'oauth.txt'
CONFIG_FILE_NAME = 'config.json'
BACKUP_FILE_EXTENSION = '.bkp'

OAUTH_FILE_PATH = os.path.join(DATA_FOLDER_PATH, OAUTH_FILE_NAME)
CONFIG_FILE_PATH = os.path.join(DATA_FOLDER_PATH, CONFIG_FILE_NAME)


def read_file(file_path):
	with open(file_path) as f:
		return f.read()


CONNECTION_PARAMETERS = {
	'host': "irc.twitch.tv",
	'port': 6667,
	'oauth_pass': read_file(OAUTH_FILE_PATH),
	'username': "TheShadude",
	'channel': "shadudev"
}


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
	return json.load(read_file(file_path))


def update_config(config):
	dump_json_to_file(CONFIG_FILE_PATH, config)


def dump_json_to_file(file_path, data):
	with open(file_path, 'w') as f:
		json.dump(data, f)
