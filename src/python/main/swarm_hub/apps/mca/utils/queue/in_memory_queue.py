import typing

from apps.mca.utils.queue import Queue
from apps.mca.utils.queue.queue import T


class InMemoryQueue(Queue, typing.Generic[T]):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__queue = []

	def _queue(self, item: T):
		self.__queue.append(item)

	def dequeue(self) -> T:
		return self.__queue.pop(0)

	def is_empty(self) -> bool:
		return len(self.__queue) == 0

	def clear(self):
		self.__queue = []
