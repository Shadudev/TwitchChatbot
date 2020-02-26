import os
try:
	os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')
except AttributeError as e:
	pass # Python 3.8-
import vlc


class SoundPlayer(object):
	def __init__(self):
		self._instance = vlc.Instance()
		self._player = self._instance.media_player_new()

	def play(self, sound_path, volume):
		self._player.set_media(self._instance.media_new(sound_path))
		self._player.audio_set_volume(volume)
		self._player.play()
