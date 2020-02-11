import json
import os
from time import sleep
from playsound import playsound
from modules.command_handler import CommandHandler

from scripts.uwu import tts
from scripts.uwu.dynamic_dictionary import DynamicDictionary

COMMAND_REWARD_ID = '72cc6239-9f74-4953-8d87-64d396d952da'

SCRIPT_BASE_PATH = os.path.dirname(__file__)
TTS_OUTPUT_FILE = os.path.join(SCRIPT_BASE_PATH, 'output.mp3')
SET_REPLACEMENTS_FILE = os.path.join(SCRIPT_BASE_PATH, 'set_replacements.json')


class UwUHandler(CommandHandler):
	def __init__(self, send_message_func, cooldown_manager):
		super(UwUHandler, self).__init__(send_message_func, cooldown_manager)
		self._tts = tts.UwUTTS()

	def should_handle_message(self, chat_message):
		return self._is_uwu_redeem(chat_message)

	def _is_uwu_redeem(self, chat_message):
		return getattr(chat_message, 'custom_reward_id', None) == COMMAND_REWARD_ID

	def handle_message(self, chat_message):
		text = chat_message.message
		uwu_text = self._translate(text)
		self.send_message('UwU: ' + uwu_text)

		if os.path.exists(TTS_OUTPUT_FILE):
			os.unlink(TTS_OUTPUT_FILE)
		self._tts.get_speech(uwu_text, TTS_OUTPUT_FILE)
		playsound(TTS_OUTPUT_FILE)

	def show_usage(self):
		self.send_message('Command should be used like so: !uwu this is a very long sentence')

	def _translate(self, text):
		words = text.split(' ')
		translated_text = []
		for word in words:
			translated_text.append(self._translate_word(word))

		return ' '.join(translated_text)


	def _translate_word(self, word):
		dictionary = self.get_dictionary()
		if word.lower() in dictionary:
			return dictionary[word.lower()]

		converted = ""
		doubleT = doubleT_Presence = th_Presence = False
		for i in range(len(word)):
			if doubleT or th_Presence:
				doubleT = th_Presence = False
				continue
			elif ((word[i] == "L" or word[i] == "l") and not doubleT_Presence) or (word[i] == "R" or word[i] == "r"):
				converted += "W" if word[i].isupper() else "w"
			elif (word[i] == "T" or word[i] == "t") and ((word[i + (1 if i + 1 < len(word) else 0)] == "T" or word[i + (1 if i + 1 < len(word) else 0)] == "t")):
				converted += (("D" if word[i].isupper() else "d") + ("D" if word[i + 1].isupper() else "d")) if i + 1 < len(word) else "t"
				doubleT = doubleT_Presence = True if i + 1 < len(word) else False
			elif (word[i] == "T" or word[i] == "t") and ((word[i + (1 if i + 1 < len(word) else 0)] == "H" or word[i + (1 if i + 1 < len(word) else 0)] == "h")):
				converted += ("F" if word[i].isupper() else "f") if i + 2 == len(word) else "t"
				th_Presence = True if i + 2 == len(word) else False
			else:
				converted += word[i]

		converted = converted.replace("no", "nya")
		converted = converted.replace("mo", "mya")
		converted = converted.replace("No", "Nya")
		converted = converted.replace("Mo", "Mya")
		converted = converted.replace("na", "nya")
		converted = converted.replace("ni", "nyi")
		converted = converted.replace("nu", "nyu")
		converted = converted.replace("ne", "nye")
		converted = converted.replace("anye", "ane")
		converted = converted.replace("inye", "ine")
		converted = converted.replace("onye", "one")
		converted = converted.replace("unye", "une")
		return converted

	def get_dictionary(self):
		return DynamicDictionary.get_dictionary()
