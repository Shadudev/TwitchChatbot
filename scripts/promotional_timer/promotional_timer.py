from datetime import timedelta
from random import choice

from modules.timer import Timer
from utils.configuration import get_value, set_value

DEFAULT_MESSAGING_INTERVAL = timedelta(minutes=45)
# Interval configuration key
INTERVAL_CONFIG_KEY = "promotion_interval"

# Messages collection to choose randomly from
MESSAGES = [
"This Shadude has coded his own sounds commands player. Write !sounds and enjoy!",
"If you're having fun and wanna stay tuned with w.e. is going on off stream too, join the Shadudes Hangout! https://discord.gg/vv9uEan",
"Each sub can choose each month what hat I shall wear for the rest of a stream. Do !hats for the existing hats."
]


class PromotionalTimer(Timer):
	def __init__(self):
		self._last_chosen_index = -1

	def get_interval(self):
		return get_value(INTERVAL_CONFIG_KEY, DEFAULT_MESSAGING_INTERVAL)

	def set_interval(self, interval):
		set_value(INTERVAL_CONFIG_KEY, interval)

	def get_message(self):
		self._last_chosen_index = choice(list(filter(lambda index: index != self._last_chosen_index, range(len(MESSAGES)))))
		return MESSAGES[self._last_chosen_index]
