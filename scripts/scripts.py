from hydration_timer import hydration_timer
from dad_jokes_teller import dad_jokes_teller


def get_timers(send_message_func):
	return [hydration_timer.HydrationTimer()]

def get_command_handlers(send_message_func):
	return [dad_jokes_teller.DadJokesTeller(send_message_func)]
