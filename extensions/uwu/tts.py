import requests


TTS_SERVER_URI = "https://tts-server.glitch.me"
CHANNEL_HEADER_NAME = "channel"


JAPANESE_CODE = 'ja-JP'
JAPANESE_VOICE_NAME = 'ja-JP-Wavenet-A'
SPEAKING_RATE = 1.3
PITCH = 1


class UwUTTS(object):
	def get_speech(self, text, output_speech_file, channel, language_code=JAPANESE_CODE, voice_name=JAPANESE_VOICE_NAME, speaking_rate=SPEAKING_RATE, pitch=PITCH):
		headers = {CHANNEL_HEADER_NAME: channel}
		request_parameters = {"text": text, "languageCode": language_code,
		 "languageName": voice_name, "pitch": pitch, "speakingRate": speaking_rate}
		
		response = requests.post(TTS_SERVER_URI, json=request_parameters, headers=headers)

		with open(output_speech_file, 'wb') as out:
		    out.write(response.content)
