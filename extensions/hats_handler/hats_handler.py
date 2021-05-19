import datetime
import json
import os

from core.framework.extensions.bases.command_handler import CommandHandler

SCRIPT_BASE_PATH = os.path.dirname(__file__)
USERS_HISTORY_FILE_PATH = os.path.join(SCRIPT_BASE_PATH, 'users.txt')

COMMAND_ID = '!hats'
RESET_OPERATION = 'reset'

USER_NAME_INDEX = 1
OPERATION_INDEX = 2
DATE_FORMAT = "%m%Y"

HATS_LIST = ['Red Knight', 'Gray Knight', 'Pink Fluffy Bunny', 'Cookie Monster']
GIVEPLZ_EMOTE = 'GivePLZ'
TAKENRG_EMOTE = 'TakeNRG'


class HatsHandler(CommandHandler):
    def __init__(self, send_message_func, cooldown_manager):
        super(HatsHandler, self).__init__(send_message_func, cooldown_manager)

        if self.read_users_history() is None:
            self.update_users_history({})

    def should_handle_message(self, chat_message):
        return chat_message.message.split(' ')[0] == COMMAND_ID

    def handle_message(self, chat_message):
        command_args = chat_message.message.split(' ')
        if len(command_args) > 1 and (chat_message.is_mod or chat_message.is_streamer):
            self.handle_mod_command(command_args)
        elif not self._cooldown_manager.is_on_cooldown(COMMAND_ID, '', datetime.timedelta(seconds=10)):
            self._cooldown_manager.set_on_cooldown(COMMAND_ID, '')
            self.list_hats()

    def handle_mod_command(self, command_args):
        user_name = command_args[USER_NAME_INDEX]
        if len(command_args) > 2:
            operation = command_args[OPERATION_INDEX]
            self.handle_operation_command(user_name, operation)

        elif self.has_user_selected_recently(user_name):
            self.send_message(
                '{user} has chosen this month already. Write "!hats {user} {reset}" to allow them to choose once more! {emote}'
                .format(user=user_name, emote=TAKENRG_EMOTE, reset=RESET_OPERATION))

        else:
            self.add_user_to_history(user_name)
            self.send_message('/me {} has made his decision!'.format(user_name))

    def handle_operation_command(self, user_name, operation):
        if operation == RESET_OPERATION:
            self.remove_user_from_history(user_name)
            self.send_message('{} has been repermitted.'.format(user_name))
        else:
            self.send_message('Unknown operation.')

    def list_hats(self):
        hats_list_message = 'With 400 glitches, one can !redeem what hat I shall wear for an hour. Existing hats: {}'
        hats_list = self.alternative_join(HATS_LIST, [TAKENRG_EMOTE, GIVEPLZ_EMOTE])
        self.send_message(hats_list_message.format(hats_list))

    def has_user_selected_recently(self, user_name):
        users_history = self.read_users_history()
        if user_name not in users_history:
            return False

        decision_date = datetime.datetime.strptime(users_history[user_name], DATE_FORMAT).date()
        current_date = datetime.datetime.now().date()
        return current_date.month == decision_date.month and current_date.year == decision_date.year

    def add_user_to_history(self, user_name):
        users_history = self.read_users_history()
        decision_date = datetime.datetime.now().date().strftime(DATE_FORMAT)
        users_history[user_name] = decision_date
        self.update_users_history(users_history)

    def remove_user_from_history(self, user_name):
        users_history = self.read_users_history()
        users_history.pop(user_name)
        self.update_users_history(users_history)

    @staticmethod
    def alternative_join(collection, seperators):
        s = ''
        for i in range(len(collection) - 1):
            s += collection[i] + ' '
            s += seperators[i % len(seperators)] + ' '
        s += collection[-1]

        return s

    def read_users_history(self):
        return self.read_json_from_file(USERS_HISTORY_FILE_PATH)

    def update_users_history(self, users_picks):
        self.dump_json_to_file(USERS_HISTORY_FILE_PATH, users_picks)

    @staticmethod
    def dump_json_to_file(file_path, data):
        with open(file_path, 'w') as f:
            json.dump(data, f)

    @staticmethod
    def read_json_from_file(file_path):
        if not os.path.exists(file_path):
            return None

        with open(file_path) as f:
            return json.load(f)
