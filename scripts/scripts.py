from utils.cooldown_manager import CooldownManager

from scripts.promotional_timer import promotional_timer
from scripts.dad_jokes_teller import dad_jokes_teller
from scripts.uwu import uwu, dynamic_dictionary
from scripts.soundbot import soundbot
from scripts.hats_handler import hats_handler


def get_timers(send_message_func):
	return [promotional_timer.PromotionalTimer()]

def get_command_handlers(send_message_func):
	command_handlers = [
	dad_jokes_teller.DadJokesTeller, uwu.UwUHandler, dynamic_dictionary.DynamicDictionary,
	soundbot.Soundbot, hats_handler.HatsHandler]

	return [command_handler(send_message_func, CooldownManager()) for command_handler in command_handlers]
