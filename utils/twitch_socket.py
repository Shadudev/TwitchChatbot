import socket
from chat_message import ChatMessage


PING_MESSAGE = 'PING :tmi.twitch.tv'
PONG_MESSAGE = 'PONG :tmi.twitch.tv'


class TwitchSocket(object):
	def __init__(self):
		self._socket = socket.socket()
		self._messages = []
		self._last_incomplete_msg = ''

	def connect(self, host, port, oauth_pass, username, channel):
		self._socket.connect((host, port))
		self._socket.send("PASS " + oauth_pass + "\r\n")
		self._socket.send("NICK " + username + "\r\n")
		self._socket.send("JOIN #" + channel + "\r\n")
		self._socket.send("CAP REQ :twitch.tv/tags\r\n")
		self._channel = channel
	
	def send(self, message):
		packed_message = "PRIVMSG #{} :{}\r\n".format(self._channel, message)
		self._socket.send(packed_message)

	def recv_message(self):
		while len(self._messages) < 1:
			self._recv_messages()
		return ChatMessage(self._messages.pop(0))

	def _recv_messages(self):
		chat_messages = self._last_incomplete_msg + self._socket.recv(1024)
		chat_messages = chat_messages.split('\r\n')
		self._last_incomplete_msg = chat_messages.pop(-1)

		if PING_MESSAGE in chat_messages:
			self._pong()
			chat_messages.remove(PING_MESSAGE)

		self._messages += filter(lambda message: ChatMessage.is_chat_message(message), chat_messages)


	def _pong(self):
		self._socket.send(PONG_MESSAGE)

	def close(self):
		self._socket.send("PART #" + self._channel + "\r\n")
		self._socket.close()
