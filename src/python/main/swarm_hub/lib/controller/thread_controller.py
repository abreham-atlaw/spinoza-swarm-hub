from abc import ABC, abstractmethod
from threading import Thread
from time import sleep

from di.misc_providers import logger


class ThreadController(Thread, ABC):

	def __init__(self, wait_time: float = 1.0):
		super().__init__()
		self.__wait_time = wait_time

	@abstractmethod
	def loop(self):
		pass

	def run(self):
		logger.info(f'Starting Controller {self.__class__.__name__}')
		while True:
			self.loop()
			sleep(self.__wait_time)