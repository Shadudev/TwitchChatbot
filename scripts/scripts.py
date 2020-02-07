from scripts.hydration_timer import hydration_timer
from scripts.dad_jokes_teller import dad_jokes_teller
from scripts.uwu import uwu


def get_timers(send_message_func):
	return [hydration_timer.HydrationTimer()]

def get_command_handlers(send_message_func):
	command_handlers = [dad_jokes_teller.DadJokesTeller, uwu.UwUHandler]
	return [command_handler(send_message_func) for command_handler in command_handlers]
