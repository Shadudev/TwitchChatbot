from abc import ABCMeta, abstractmethod, abstractproperty

# Interval in seconds
DEFAULT_INTERVAL = 15 * 60


class Timer(object):
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def get_interval(self):
		pass

	@abstractmethod
	def set_interval(self, interval):
		pass

	@abstractmethod
	def get_message(self):
		pass

