from core.framework.extensions.cooldown_manager import CooldownManager
from extensions.dad_jokes_teller import dad_jokes_teller
from extensions.hats_handler import hats_handler
from extensions.promotional_timer import promotional_timer
from extensions.regex_command_trigger import regex_command_trigger
from extensions.small_screen import small_screen
from extensions.soundbot import soundbot
from extensions.uwu import uwu, dynamic_dictionary


def get_timers():
    return [promotional_timer.PromotionalTimer()]


def get_command_handlers(send_message_func):
    command_handlers = [
        dad_jokes_teller.DadJokesTeller, uwu.UwUHandler, dynamic_dictionary.DynamicDictionary,
        soundbot.Soundbot, hats_handler.HatsHandler, small_screen.SmallScreenHandler,
        regex_command_trigger.RegexCommandTrigger]

    return [command_handler(send_message_func, CooldownManager()) for command_handler in command_handlers]
