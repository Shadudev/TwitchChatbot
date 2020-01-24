from utils.configuration import get_value, set_value
from modules.timer import Timer

# Interval in seconds
DEFAULT_MESSAGING_INTERVAL = 10 * 60
# Interval configuration key
INTERVAL_CONFIG_KEY = "hydration_reminder_interval"

# Messages collection to choose randomly from
MESSAGES = [
"Gotta balance the PUBG thirst with some actual water *cough*",
"The human body is composed of 72% water, make yours 73%!",
"Good sleep can improve concentration but since you're live, drinking may help!",
"Water boosts skin health. You want that baby buttcheek skin don't you?",
"Drinking water improves performance. That's gotta be the cause for your games today SeemsGood"
]


class HydrationTimer(Timer):
	def __init__(self):
		self._last_chosen_index = -1

	def get_interval(self):
		return get_value(INTERVAL_CONFIG_KEY, DEFAULT_MESSAGING_INTERVAL)

	def set_interval(self, interval):
		set_value(INTERVAL_CONFIG_KEY, interval)

	def get_message(self):
		self._last_chosen_index = choice(filter(lambda index: index != self._last_chosen_index, range(len(MESSAGES))))
		return MESSAGES[self._last_chosen_index]
