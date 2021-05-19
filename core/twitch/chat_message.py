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
		self.__parse_message_data(message_data)

	@staticmethod
	def is_chat_message(message_data):
		return re.match(MESSAGE_DATA_REGEX, message_data) is not None

	def __parse_message_data(self, message_data):
		self.raw = message_data
		privmsg_index = message_data.index('PRIVMSG #')
		actual_message = message_data[message_data.index(':', privmsg_index) + 1:]
		self.message = actual_message

		extra_message_data = message_data[:privmsg_index - 1].split(';')
		for tag in extra_message_data:
			key, value = tag.split('=')
			if key in ChatMessage.TAGS_PARSERS:
				ChatMessage.TAGS_PARSERS[key](self, value)

	def __parse_badge_info(self, tag_value):
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

	def __parse_bits(self, bits_amount):
		self.bits = int(bits_amount)

	def __parse_display_name(self, display_name):
		self.display_name = display_name

	def __parse_mod(self, mod_value):
		self.is_mod = mod_value == '1' 

	def __parse_subscriber(self, subscriber_value):
		self.is_sub = subscriber_value == '1'

	def __parse_user_id(self, user_id):
		self.user_id = user_id

	def __parse_user(self, user_type):
		self.user = re.match('.*@(.*).tmi.twitch.tv.*', user_type).group(1)

	def __parse_custom_reward_id(self, custom_reward_id):
		self.custom_reward_id = custom_reward_id

	def __parse_message_id(self, message_id):
		self.msg_id = message_id

	TAGS_PARSERS = {'@badge-info': __parse_badge_info, 'badges': __parse_badge_info,
					'bits': __parse_bits, 'display-name': __parse_display_name, 'mod': __parse_mod,
					'subscriber': __parse_subscriber, 'user-id': __parse_user_id, 'user-type': __parse_user,
					'custom-reward-id': __parse_custom_reward_id, 'id': __parse_message_id}
