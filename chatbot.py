from scripts import scripts
from utils import configuration
from utils.twitch_socket import TwitchSocket


class Chatbot(object):

	_chatbot = None

	def __init__(self):
		Chatbot._chatbot = self
		self._twitch_socket = TwitchSocket()
		self._timers = scripts.get_timers(Chatbot.send_message)
		self._command_handlers = scripts.get_command_handlers(Chatbot.send_message)

	def serve_forever(self):
		self._twitch_socket.connect(**configuration.CONNECTION_PARAMETERS)
		while True:
			chat_message = self._twitch_socket.recv_message()
			#print 'mod?{},sub?{}-{},vip?{},bits?{}-{},{} ({}): {}'.format(
			#	chat_message.is_mod, chat_message.is_sub, chat_message.sub_length, chat_message.is_vip,
			#	chat_message.bits, chat_message.cheer_badge, chat_message.display_name, chat_message.user, 
			#	chat_message.message)

			for command_handler in self._command_handlers:
				if command_handler.should_handle_message(chat_message):
					command_handler.handle_message(chat_message)

			if chat_message.message == 'Chatbot, stop.':
				break

		self._twitch_socket.close()

	def inst_send_message(self, message):
		self._twitch_socket.send(message)

	@staticmethod
	def send_message(message):
		Chatbot._chatbot.inst_send_message(message)
