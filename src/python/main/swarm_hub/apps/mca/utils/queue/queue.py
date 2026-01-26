import typing
from abc import ABC, abstractmethod
from typing import TypeVar

T = TypeVar('T')

class Queue(ABC, typing.Generic[T]):

	def __init__(self):
		self.__queue_triggers: typing.List[typing.Callable[[T], None]] = []

	def add_queue_trigger(self, trigger: typing.Callable[[T], None]):
		self.__queue_triggers.append(trigger)

	@abstractmethod
	def _queue(self, item: T):
		pass

	def queue(self, item: T):
		self._queue(item)
		for trigger in self.__queue_triggers:
			trigger(item)

	@abstractmethod
	def dequeue(self) -> T:
		pass

	@abstractmethod
	def is_empty(self) -> bool:
		pass
