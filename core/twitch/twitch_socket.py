import socket
from core.framework import configuration
from core.twitch.chat_message import ChatMessage


LINE_BREAK = '\r\n'
PING_MESSAGE = 'PING :tmi.twitch.tv'
PONG_MESSAGE = 'PONG :tmi.twitch.tv'

MESSAGE_MAX_CHARACTERS = 500

class TwitchSocket(object):
	def __init__(self):
		self._init_socket()
		self._messages = []
		self._last_incomplete_msg = ''

	def _init_socket(self):
		self._socket = socket.socket()
		self.connect(**configuration.CONNECTION_PARAMETERS)

	def connect(self, host, port, oauth_pass, username, channel):
		self._socket.connect((host, port))
		self._login(username, oauth_pass)
		self._join_chat_room(channel)
		self._register_tags()

	def _login(self, username, oauth_pass):
		self._send("PASS " + oauth_pass)
		self._send("NICK " + username)

	def _join_chat_room(self, channel):
		self._send("JOIN #" + channel)
		self._channel = channel

	def _register_tags(self):
		self._send("CAP REQ :twitch.tv/tags")

	def send_message(self, message):
		message_segments = [message[i:i+MESSAGE_MAX_CHARACTERS] for i in range(0, len(message), MESSAGE_MAX_CHARACTERS)]
		for segment in message_segments:
			wrapped_segment = "PRIVMSG #{} :{}".format(self._channel, segment)
			self._send(wrapped_segment)

	def _send(self, data):
		self._socket.send(str(data + LINE_BREAK).encode('utf8'))

	def recv_message(self):
		while len(self._messages) < 1:
			self._recv_messages()
		return ChatMessage(self._messages.pop(0))

	def _recv_messages(self):
		try:
			received_messages = self._socket.recv(1024).decode('utf8')
		except (ConnectionAbortedError, ConnectionResetError):
			self._init_socket()
			received_messages = self._socket.recv(1024).decode('utf8')
			
		chat_messages = self._last_incomplete_msg + received_messages

		chat_messages = chat_messages.split(LINE_BREAK)
		self._last_incomplete_msg = chat_messages.pop(-1)

		if PING_MESSAGE in chat_messages:
			self._pong()
			chat_messages.remove(PING_MESSAGE)

		self._messages += filter(lambda message: ChatMessage.is_chat_message(message), chat_messages)

	def _pong(self):
		self._send(PONG_MESSAGE)

	def close(self):
		self._send("PART #" + self._channel + "")
		self._socket.close()
