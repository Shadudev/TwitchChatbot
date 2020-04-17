from core.framework.extensions.cooldown_manager import CooldownManager

from extensions.promotional_timer import promotional_timer
from extensions.dad_jokes_teller import dad_jokes_teller
from extensions.uwu import uwu, dynamic_dictionary
from extensions.soundbot import soundbot
from extensions.hats_handler import hats_handler
from extensions.small_screen import small_screen


def get_timers(send_message_func):
	return [promotional_timer.PromotionalTimer()]

def get_command_handlers(send_message_func):
	command_handlers = [
	dad_jokes_teller.DadJokesTeller, uwu.UwUHandler, dynamic_dictionary.DynamicDictionary,
	soundbot.Soundbot, hats_handler.HatsHandler, small_screen.SmallScreenHandler]

	return [command_handler(send_message_func, CooldownManager()) for command_handler in command_handlers]
