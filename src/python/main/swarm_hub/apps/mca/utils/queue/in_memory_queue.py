import typing

from apps.mca.utils.queue import Queue
from apps.mca.utils.queue.queue import T


class InMemoryQueue(Queue, typing.Generic[T]):

	def __init__(
			self,
			*args,
			compare_fn: typing.Callable[[T, T], bool] = None,
			**kwargs,
	):
		super().__init__(*args, **kwargs)
		self.__queue = []
		self.__compare_fn = compare_fn

	def _queue(self, item: T):
		self.__queue.append(item)

	def dequeue(self) -> T:
		return self.__queue.pop(0)

	def is_empty(self) -> bool:
		return len(self.__queue) == 0

	def clear(self):
		self.__queue = []

	def __len__(self):
		return len(self.__queue)

	def _compare(self, item1: T, item2: T) -> bool:
		if self.__compare_fn is not None:
			return self.__compare_fn(item1, item2)
		return item1 == item2

	def __contains__(self, item) -> bool:
		for queued_item in self.__queue:
			if self._compare(queued_item, item):
				return True
		return False
