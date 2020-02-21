import socket
from utils import configuration
from utils.chat_message import ChatMessage


PING_MESSAGE = 'PING :tmi.twitch.tv'
PONG_MESSAGE = 'PONG :tmi.twitch.tv'


class TwitchSocket(object):
	def __init__(self):
		self.init_socket()
		self._messages = []
		self._last_incomplete_msg = ''

	def init_socket(self):
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

	def send(self, message):
		packed_message = "PRIVMSG #{} :{}".format(self._channel, message)
		self._send(packed_message)

	def _send(self, data):
		self._socket.send(str(data + '\r\n').encode('utf8'))

	def recv_message(self):
		while len(self._messages) < 1:
			self._recv_messages()
		return ChatMessage(self._messages.pop(0))

	def _recv_messages(self):
		try:
			received_messages = self._socket.recv(1024).decode('utf8')
		except (ConnectionAbortedError, ConnectionResetError):
			self.init_socket()
			received_messages = self._socket.recv(1024).decode('utf8')
			
		chat_messages = self._last_incomplete_msg + received_messages

		chat_messages = chat_messages.split('')
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
