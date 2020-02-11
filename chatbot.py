import threading
import traceback
from datetime import timedelta
from time import sleep

from scripts import scripts
from utils import configuration, log
from utils.twitch_socket import TwitchSocket


class Chatbot(object):

	_interval = timedelta(seconds=10)
	_chatbot = None

	def __init__(self):
		Chatbot._chatbot = self

		configuration.initialize()
		self._twitch_socket = TwitchSocket()
		self._is_running = True
		self._timers = scripts.get_timers(Chatbot.send_message)
		self._command_handlers = scripts.get_command_handlers(Chatbot.send_message)

	def serve_forever(self):
		self._timer_thread = threading.Thread(target=self.handle_timers)
		self._timer_thread.start()

		while self._is_running:
			chat_message = self._twitch_socket.recv_message()

			for command_handler in self._command_handlers:
				try:
					if command_handler.should_handle_message(chat_message):
						command_handler.handle_message(chat_message)
				except Exception as e:
					print(traceback.format_exc())

			if chat_message.message == 'Chatbot, stop.' and chat_message.is_mod:
				self._is_running = False

		self._twitch_socket.close()
		self._timer_thread.join()

	def handle_timers(self):
		timers_ticks = {timer: timedelta(0) for timer in self._timers}

		sleep(self._interval.seconds)
		while self._is_running:
			for timer in self._timers:
				try:
					if timers_ticks[timer] >= timer.get_interval():
						self.send_message(timer.get_message())
						timers_ticks[timer] = timedelta(0)
					else:
						timers_ticks[timer] += self._interval
				except Exception as e:
					print(traceback.format_exc())
	
			sleep(self._interval.seconds)


	def inst_send_message(self, message):
		self._twitch_socket.send(message)

	@staticmethod
	def send_message(message):
		Chatbot._chatbot.inst_send_message(message)
