from abc import ABCMeta, abstractmethod


class CommandHandler(object):
	def __init__(self, send_message_func):
		self._send_message_func = send_message_func

	def send_message(self, message):
		self._send_message_func(message)

	@abstractmethod
	def should_handle_message(self, chat_message):
		pass

	@abstractmethod
	def handle_message(self, chat_message):
		pass
