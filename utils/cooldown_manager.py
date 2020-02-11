import datetime


class CooldownManager(object):
	def __init__(self):
		self._cooldowns = {}

	def set_on_cooldown(self, key, secondary_key=''):
		self._cooldowns[key][secondary_key] = datetime.datetime.now()

	def is_on_cooldown(self, key, cooldown):
		if key in self._cooldowns:
			return datetime.datetime.now() >= self._cooldowns[key] + cooldown
		return False
