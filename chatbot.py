import concurrent.futures
import threading
import traceback
from datetime import timedelta
from time import sleep

from core.exceptions.chatbot_already_initialized import ChatbotAlreadyInitialized
from core.framework import configuration, media_player
from core.twitch.twitch_socket import TwitchSocket
from extensions import extensions


class Chatbot(object):
    __timers_check_interval = timedelta(seconds=10)
    __chatbot = None

    def __init__(self):
        if Chatbot.__chatbot is not None:
            raise ChatbotAlreadyInitialized()

        Chatbot.__chatbot = self

        self.initialize_framework()

        self.__twitch_socket = TwitchSocket()
        self.__is_running = True
        self.__timers = extensions.get_timers()
        self.__command_handlers = extensions.get_command_handlers(Chatbot.send_message)
        self.__timer_thread = threading.Thread(target=self.handle_timers)
        self.__worker_threads = concurrent.futures.ThreadPoolExecutor()

    def serve_forever(self):
        print("Chatbot starting...")
        self.__timer_thread.start()
        self.__handle_chat_messages()

        self.__twitch_socket.close()
        self.__timer_thread.join()

    def handle_timers(self):
        timers_ticks = {timer: timedelta(0) for timer in self.__timers}

        sleep(self.__timers_check_interval.seconds)
        while self.__is_running:
            for timer in self.__timers:
                try:
                    if timers_ticks[timer] >= timer.get_interval():
                        timer_message = timer.get_message()
                        if timer_message:
                            self.send_message(timer_message)
                        timers_ticks[timer] = timedelta(0)
                    else:
                        timers_ticks[timer] += self.__timers_check_interval
                except Exception as e:
                    print(traceback.format_exc())

            sleep(self.__timers_check_interval.seconds)

    def inst_send_message(self, message):
        self.__twitch_socket.send_message(message)

    @staticmethod
    def send_message(message):
        Chatbot.__chatbot.inst_send_message(message)

    @staticmethod
    def initialize_framework():
        configuration.initialize()
        media_player.MediaPlayer.initialize()

    def __handle_chat_messages(self):
        while self.__is_running:
            chat_message = self.__twitch_socket.recv_message()
            print(chat_message.display_name + ': ' + chat_message.message)
            self.__broadcast_chat_message(chat_message)

            if chat_message.message == 'Chatbot, stop.' and chat_message.is_mod:
                self.__is_running = False

    def __broadcast_chat_message(self, chat_message):
        self.__worker_threads.map(
            lambda command_handler: self.__forward_chat_message_to_command_handler(chat_message, command_handler),
            self.__command_handlers)

    @staticmethod
    def __forward_chat_message_to_command_handler(chat_message, command_handler):
        try:
            if command_handler.should_handle_message(chat_message):
                command_handler.handle_message(chat_message)
        except Exception as e:
            print(traceback.format_exc())
