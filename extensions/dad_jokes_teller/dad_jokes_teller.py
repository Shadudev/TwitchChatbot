import datetime
import os
import random

from core.framework.extensions.bases.command_handler import CommandHandler

COMMAND_ID = '!dad'

SCRIPT_BASE_PATH = os.path.dirname(__file__)
JOKES_FOLDER_PATH = os.path.join(SCRIPT_BASE_PATH, 'Jokes')
JOKES_LOG_PATH = os.path.join(SCRIPT_BASE_PATH, 'log.txt')

USER_COOLDOWN = datetime.timedelta(minutes=30)


class DadJokesTeller(CommandHandler):
    def __init__(self, send_message_func, cooldown_manager):
        super(DadJokesTeller, self).__init__(send_message_func, cooldown_manager)

        if not os.path.exists(JOKES_FOLDER_PATH):
            os.mkdir(JOKES_FOLDER_PATH)

    def should_handle_message(self, chat_message):
        command = chat_message.message.split(' ')[0]
        is_on_cooldown = self._cooldown_manager.is_on_cooldown(COMMAND_ID, chat_message.user, USER_COOLDOWN)
        return command == COMMAND_ID and not is_on_cooldown

    def handle_message(self, chat_message):
        self._cooldown_manager.set_on_cooldown(COMMAND_ID, chat_message.user)
        self.__tell_joke()

    def __tell_joke(self):
        chosen_file = self.__choose_random_file(JOKES_FOLDER_PATH)
        joke = self.__pop_joke(os.path.join(JOKES_FOLDER_PATH, chosen_file))
        self.send_message(joke)
        self.__log(joke)

    def __choose_random_file(self, path):
        files = list(filter(lambda fname: fname.endswith('.txt'), os.listdir(path)))
        return files[random.randrange(len(files))]

    def __pop_joke(self, file_path):
        jokes = eval(self.__read_file(file_path))
        index = random.randrange(len(jokes))
        joke = jokes.pop(index)
        self.__write_file(file_path, str(jokes))
        return joke

    def __read_file(self, path):
        with open(path) as f:
            return f.read()

    def __write_file(self, path, content):
        with open(path, 'w') as f:
            f.write(content)

    def __append_file(self, path, content):
        with open(path, 'a') as f:
            f.write(content + '\n')

    def __log(self, msg):
        self.__append_file(JOKES_LOG_PATH, str(datetime.datetime.now()) + ',' + msg)
