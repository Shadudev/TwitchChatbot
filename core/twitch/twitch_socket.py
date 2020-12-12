import socket
from core.framework import configuration
from core.twitch.chat_message import ChatMessage


LINE_BREAK = '\r\n'
PING_MESSAGE = 'PING :tmi.twitch.tv'
PONG_MESSAGE = 'PONG :tmi.twitch.tv'

MESSAGE_MAX_CHARACTERS = 500


class TwitchSocket(object):
	CAPABILITIES = ' '.join(["twitch.tv/tags", "twitch.tv/commands"])

	def __init__(self):
		self.__init_socket()
		self._messages = []
		self._last_incomplete_msg = ''

	def __init_socket(self):
		self._socket = socket.socket()
		self.connect(**configuration.CONNECTION_PARAMETERS)

	def connect(self, host, port, oauth_pass, username, channel):
		self._socket.connect((host, port))
		self.__login(username, oauth_pass)
		self.__join_chat_room(channel)
		self.__register_tags()

	def __login(self, username, oauth_pass):
		self.__send("PASS " + oauth_pass)
		self.__send("NICK " + username)

	def __join_chat_room(self, channel):
		self.__send("JOIN #" + channel)
		self._channel = channel

	def __register_tags(self):
		self.__send("CAP REQ :%s" % self.CAPABILITIES)

	def send_message(self, message):
		message_segments = [message[i:i+MESSAGE_MAX_CHARACTERS] for i in range(0, len(message), MESSAGE_MAX_CHARACTERS)]
		for segment in message_segments:
			wrapped_segment = "PRIVMSG #{} :{}".format(self._channel, segment)
			self.__send(wrapped_segment)

	def __send(self, data):
		self._socket.send(str(data + LINE_BREAK).encode('utf8'))

	def recv_message(self):
		while len(self._messages) < 1:
			self.__recv_messages()
		return ChatMessage(self._messages.pop(0))

	def __recv_messages(self):
		try:
			received_messages = self._socket.recv(1024).decode('utf8')
		except (ConnectionAbortedError, ConnectionResetError):
			self.__init_socket()
			received_messages = self._socket.recv(1024).decode('utf8')

		chat_messages = self._last_incomplete_msg + received_messages

		chat_messages = chat_messages.split(LINE_BREAK)
		self._last_incomplete_msg = chat_messages.pop(-1)

		if PING_MESSAGE in chat_messages:
			self.__pong()
			chat_messages.remove(PING_MESSAGE)

		self._messages += filter(lambda message: ChatMessage.is_chat_message(message), chat_messages)

	def __pong(self):
		self.__send(PONG_MESSAGE)

	def close(self):
		self.__send("PART #" + self._channel + "")
		self._socket.close()
