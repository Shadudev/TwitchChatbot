import threading
import traceback
from datetime import timedelta
from time import sleep

from extensions import extensions
from core.framework import configuration, media_player
from core.twitch.twitch_socket import TwitchSocket


class Chatbot(object):

	_timers_check_interval = timedelta(seconds=10)
	_chatbot = None

	def __init__(self):
		Chatbot._chatbot = self

		self.initialize_framework()
		
		self._twitch_socket = TwitchSocket()
		self._is_running = True
		self._timers = extensions.get_timers(Chatbot.send_message)
		self._command_handlers = extensions.get_command_handlers(Chatbot.send_message)
		self._timer_thread = threading.Thread(target=self.handle_timers)

	def serve_forever(self):
		print("Chatbot starting...")
		self._timer_thread.start()
		self.__handle_chat_messages()

		self._twitch_socket.close()
		self._timer_thread.join()

	def __handle_chat_messages(self):
		while self._is_running:
			chat_message = self._twitch_socket.recv_message()
			print(chat_message.display_name + ': ' + chat_message.message)

			for command_handler in self._command_handlers:
				try:
					if command_handler.should_handle_message(chat_message):
						command_handler.handle_message(chat_message)
				except Exception as e:
					print(traceback.format_exc())

			if chat_message.message == 'Chatbot, stop.' and chat_message.is_mod:
				self._is_running = False

	def handle_timers(self):
		timers_ticks = {timer: timedelta(0) for timer in self._timers}

		sleep(self._timers_check_interval.seconds)
		while self._is_running:
			for timer in self._timers:
				try:
					if timers_ticks[timer] >= timer.get_interval():
						self.send_message(timer.get_message())
						timers_ticks[timer] = timedelta(0)
					else:
						timers_ticks[timer] += self._timers_check_interval
				except Exception as e:
					print(traceback.format_exc())
	
			sleep(self._timers_check_interval.seconds)


	def inst_send_message(self, message):
		self._twitch_socket.send_message(message)

	@staticmethod
	def send_message(message):
		Chatbot._chatbot.inst_send_message(message)

	def initialize_framework(self):
		configuration.initialize()
		media_player.MediaPlayer.initialize()
