import json
import os
from core.framework.extensions.bases.command_handler import CommandHandler

COMMAND_ID = '!dict'
SCRIPT_BASE_PATH = os.path.dirname(__file__)
DICTIONARY_FILE = os.path.join(SCRIPT_BASE_PATH, 'dictionary.json')

class DynamicDictionary(CommandHandler):
	def __init__(self, send_message_func, cooldown_manager):
		super(DynamicDictionary, self).__init__(send_message_func, cooldown_manager)

	def should_handle_message(self, chat_message):
		return chat_message.message.split(' ')[0] == COMMAND_ID

	def handle_message(self, chat_message):
		try:
			if chat_message.is_mod or chat_message.is_streamer:
				split_message = chat_message.message.split(' ')
				_, word, translation = split_message[0], split_message[1], split_message[2:]
				self.add_to_dictionary(word, translation)
				self.send_message('Oh, so {} is actually {}.'.format(word, translation))
			else:
				self.show_usage()
		except:
			self.show_usage()

	def show_usage(self):
		self.send_message("No, it's {} <word> <twanswation-nya>. Oh, and mods only!".format(COMMAND_ID))

	def add_to_dictionary(self, word, translation):
		dictionary = DynamicDictionary.get_dictionary()
		dictionary[word] = translation
		self.set_dictionary(dictionary)

	@staticmethod
	def get_dictionary():
		with open(DICTIONARY_FILE) as f:
			return json.loads(f.read())

	def set_dictionary(self, dictionary):
		with open(DICTIONARY_FILE, 'w', encoding='utf-8') as f:
			return json.dump(dictionary, f, ensure_ascii=False)
