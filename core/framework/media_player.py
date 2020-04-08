import os
try:
	os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')
except AttributeError as e:
	pass # Python 3.8-
import vlc


class MediaPlayer(object):
	_instance = None
	_player = None

	@staticmethod
	def initialize():
		if MediaPlayer._instance is None or MediaPlayer._player is None:
			MediaPlayer._instance = vlc.Instance()
			MediaPlayer._player = MediaPlayer._instance.media_player_new()

	@staticmethod
	def play(sound_path, volume):
		if MediaPlayer._instance is None or MediaPlayer._player is None:
			MediaPlayer.initialize()

		MediaPlayer._player.set_media(MediaPlayer._instance.media_new(sound_path))
		MediaPlayer._player.audio_set_volume(volume)
		MediaPlayer._player.play()
