import datetime
import os
from google.cloud import texttospeech

VOICE_LANGUAGE_CODE = 'ja-JP'
VOICE_NAME = 'ja-JP-Wavenet-A'

SPEAKING_RATE = 1.3
PITCH = 1

SCRIPT_BASE_PATH = os.path.dirname(__file__)
CHARS_COUNT_PATH = os.path.join(SCRIPT_BASE_PATH, 'count.txt')
LOG_PATH = os.path.join(SCRIPT_BASE_PATH, 'log.txt')
LAST_RESET_PATH = os.path.join(SCRIPT_BASE_PATH, 'reset.txt')
RESET_DATE_FORMAT = '%m-%Y'


class UwUTTS(object):
	def __init__(self):
		if not os.path.exists(LAST_RESET_PATH):
			with open(LAST_RESET_PATH, 'w') as f:
				f.write(datetime.date.today().strftime(RESET_DATE_FORMAT))
		else:
			with open(LAST_RESET_PATH) as f:
				last_reset_date = datetime.datetime.strptime(f.read(), RESET_DATE_FORMAT)

			today = datetime.date.today()
			if today.month > last_reset_date.month or today.year > last_reset_date.year:
				with open(CHARS_COUNT_PATH, 'w') as f:
					f.write('0')
				with open(LOG_PATH, 'a') as f:
					f.write('Count reset going into {}.{} \n'.format(today.month, today.year))


	def get_speech(self, text, output_speech_file):
		client = texttospeech.TextToSpeechClient()

		synthesis_input = texttospeech.types.SynthesisInput(text=text)
		voice = texttospeech.types.VoiceSelectionParams(
		    language_code=VOICE_LANGUAGE_CODE,
		    name=VOICE_NAME)
		audio_config = texttospeech.types.AudioConfig(
		    audio_encoding=texttospeech.enums.AudioEncoding.MP3,
		    speaking_rate=SPEAKING_RATE, pitch=PITCH)

		response = client.synthesize_speech(synthesis_input, voice, audio_config)
		self._update_characters_count(text)

		with open(output_speech_file, 'wb') as out:
		    out.write(response.audio_content)


	def _update_characters_count(self, text):
		additional_chars_count = len(text)

		chars_count = self._get_current_characters_count()

		chars_count += additional_chars_count
		with open(CHARS_COUNT_PATH, 'w') as f:
			f.write(str(chars_count))

		with open(LOG_PATH, 'a') as f:
			f.write('{}, {}\n'.format(chars_count, text))


	def _get_current_characters_count(self):
		if os.path.exists(CHARS_COUNT_PATH):
			with open(CHARS_COUNT_PATH) as f:
				return int(f.read())
		return 0
