import re


MESSAGE_DATA_REGEX = '.*.tmi.twitch.tv PRIVMSG #(.*) :.*'
BADGE_INFO = '(.*)/(.*)'

SUBSCRIBER_BADGE_ID = 'subscriber'
STREAMER_BADGE_ID = 'broadcaster'
VIP_BADGE_ID = 'vip'
CHEER_BADGE_ID = 'bits'


class ChatMessage(object):
	def __init__(self, message_data):
		self.is_sub = self.is_vip = self.is_streamer = self.is_mod = False
		self.bits = self.sub_length = self.cheer_badge = 0
		self._parse_message_data(message_data)

	def _parse_message_data(self, message_data):
		privmsg_index = message_data.index('PRIVMSG #')
		actual_message = message_data[message_data.index(':', privmsg_index) + 1:]
		self.message = actual_message

		extra_message_data = message_data[:privmsg_index - 1].split(';')
		for tag in extra_message_data:
			key, value = tag.split('=')
			if key in ChatMessage.TAGS_PARSERS:
				ChatMessage.TAGS_PARSERS[key](self, value)

	def _parse_badge_info(self, tag_value):
		for value in tag_value.split(','):
			match = re.match(BADGE_INFO, value)
			if match:
				badge_id = match.group(1)
				if badge_id == SUBSCRIBER_BADGE_ID and not self.is_sub:
					self.is_sub = True
					self.sub_length = int(match.group(2))
				elif badge_id == STREAMER_BADGE_ID:
					self.is_streamer = True
				elif badge_id == VIP_BADGE_ID:
					self.is_vip = True
				elif badge_id == CHEER_BADGE_ID:
					self.cheer_badge = int(value[value.index('/')+1:])

	def _parse_bits(self, bits_amount):
		self.bits = int(bits_amount)

	def _parse_display_name(self, display_name):
		self.display_name = display_name

	def _parse_mod(self, mod_value):
		self.is_mod = mod_value == '1' 

	def _parse_subscriber(self, subscriber_value):
		self.is_sub = subscriber_value == '1'

	def _parse_user_id(self, user_id):
		self.user_id = user_id

	def _parse_user(self, user_type):
		self.user = re.match('.*@(.*).tmi.twitch.tv.*', user_type).group(1)

	def _parse_custom_reward_id(self, custom_reward_id):
		self.custom_reward_id = custom_reward_id

	@staticmethod
	def is_chat_message(message_data):
		return re.match(MESSAGE_DATA_REGEX, message_data) is not None


	TAGS_PARSERS = {'@badge-info': _parse_badge_info, 'badges': _parse_badge_info,
					'bits': _parse_bits, 'display-name': _parse_display_name, 'mod': _parse_mod,
					'subscriber': _parse_subscriber, 'user-id': _parse_user_id, 'user-type': _parse_user,
					'custom-reward-id': _parse_custom_reward_id}
