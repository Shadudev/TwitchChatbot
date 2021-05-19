import datetime

import win32gui

from core.framework.extensions.bases.command_handler import CommandHandler

COMMAND_ID = '!smallscreen'
RESPONSE_MESSAGE = '!so {channel}'


class SmallScreenHandler(CommandHandler):
    def __init__(self, send_message_func, cooldown_manager):
        super(SmallScreenHandler, self).__init__(send_message_func, cooldown_manager)

    def should_handle_message(self, chat_message):
        return chat_message.message.split(' ')[0] == COMMAND_ID

    def handle_message(self, chat_message):
        if not self._cooldown_manager.is_on_cooldown(COMMAND_ID, '', datetime.timedelta(seconds=10)):
            self._cooldown_manager.set_on_cooldown(COMMAND_ID, '')
            self.shoutout()

    def shoutout(self):
        twitch_windows = self.find_twitch_window_names()
        if len(twitch_windows) == 0:
            return
        elif len(twitch_windows) > 1:
            print("Over a single twitch window?")

        window_name = twitch_windows[0]
        channel = self.extract_channel_from_window_name(window_name)
        self.send_message(RESPONSE_MESSAGE.format(channel=channel))

    def find_twitch_window_names(self):
        matching_windows = []
        win32gui.EnumWindows(self.filter_window_names, matching_windows)
        return matching_windows

    @staticmethod
    def filter_window_names(hwnd, lParam):
        name = win32gui.GetWindowText(hwnd)
        if ' - Twitch ' in name:
            lParam.append(name)

    def extract_channel_from_window_name(self, window_name):
        return window_name[:window_name.index(' - ')]
