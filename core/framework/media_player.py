import os

try:
    os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')
except AttributeError as e:
    pass  # Python 3.8-
import vlc


class MediaPlayer(object):
    __instance = None
    __player = None
    __media_list = None
    __media_volumes = []
    __currently_playing_index = 0

    @classmethod
    def initialize(cls):
        if cls.__instance is None or cls.__player is None or cls.__media_list is None:
            cls.__instance = vlc.Instance()
            cls.__player = cls.__create_media_list_player()
            cls.__media_list = cls.__create_media_list()
            cls.__player.set_media_list(cls.__media_list)
            cls.__player.event_manager().event_attach(vlc.EventType.MediaListPlayerNextItemSet,
                                                      lambda self: cls.__update_next_volume())
            cls.__player.event_manager().event_attach(vlc.EventType.MediaListPlayerPlayed,
                                                      lambda self: cls.__player_ended())

    @classmethod
    def play(cls, sound_path, volume, sync=True):
        if cls.__instance is None or cls.__player is None:
            cls.initialize()

        if sync:
            cls.__play_sync(sound_path, volume)
        else:
            cls.__play_async(sound_path, volume)

    @classmethod
    def skip(cls):
        if -1 == cls.__player.next():
            cls.__set_volume(0)

    @classmethod
    def __update_next_volume(cls):
        cls.__set_volume(cls.__get_next_volume())

    @classmethod
    def __set_volume(cls, volume):
        cls.__player.get_media_player().audio_set_volume(volume)

    @classmethod
    def __get_next_volume(cls):
        if cls.__media_volumes:
            volume = cls.__media_volumes[cls.__currently_playing_index]
            cls.__currently_playing_index += 1
            return volume

    @classmethod
    def __play_sync(cls, sound_path, volume):
        cls.__media_list.lock()
        cls.__media_list.add_media(cls.__get_media(sound_path))
        cls.__media_volumes.append(volume)
        cls.__media_list.unlock()

        if not cls.__player.is_playing():
            cls.__player.play()

    @classmethod
    def __play_async(cls, sound_path, volume):
        player = cls.__create_media_player()
        player.set_media(cls.__get_media(sound_path))
        player.audio_set_volume(volume)
        player.play()

    @classmethod
    def __player_ended(cls):
        cls.__media_list.lock()
        for _ in range(cls.__currently_playing_index):
            cls.__media_list.remove_index(0)

        cls.__media_volumes = cls.__media_volumes[cls.__currently_playing_index:]
        cls.__currently_playing_index = 0
        cls.__media_list.unlock()

    @classmethod
    def __get_media(cls, sound_path):
        return cls.__instance.media_new(sound_path)

    @classmethod
    def __create_media_list_player(cls):
        return cls.__instance.media_list_player_new()

    @classmethod
    def __create_media_player(cls):
        return cls.__instance.media_player_new()

    @classmethod
    def __create_media_list(cls):
        return cls.__instance.media_list_new()
