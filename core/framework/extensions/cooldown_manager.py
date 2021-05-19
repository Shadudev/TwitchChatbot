import datetime


class CooldownManager(object):
    def __init__(self):
        self._cooldowns = {}

    def set_on_cooldown(self, key, secondary_key):
        if not key in self._cooldowns:
            self._cooldowns[key] = {}
        self._cooldowns[key][secondary_key] = datetime.datetime.now()

    def set_off_cooldown(self, key, secondary_key):
        if key in self._cooldowns and secondary_key in self._cooldowns[key]:
            self._cooldowns[key].pop(secondary_key)

    def is_on_cooldown(self, key, secondary_key, cooldown):
        if key in self._cooldowns and secondary_key in self._cooldowns[key]:
            return self.get_remaining_cooldown(key, secondary_key, cooldown) > datetime.timedelta(0)
        return False

    def get_remaining_cooldown(self, key, secondary_key, cooldown):
        return self._cooldowns[key][secondary_key] + cooldown - datetime.datetime.now()
