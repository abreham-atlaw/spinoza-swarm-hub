import typing
from abc import ABC, abstractmethod

from apps.allocation.models import Worker
from apps.mca.models import Node


class MCARepository(ABC):

	def __init__(self):
		self.__completion_triggers: typing.List[typing.Callable[[Node], None]] = []

	def add_completion_trigger(self, callback: typing.Callable[[Node], None]):
		self.__completion_triggers.append(callback)

	@abstractmethod
	def queue_node(self, node: Node):
		pass

	@abstractmethod
	def dequeue_node(self) -> Node:
		pass

	@abstractmethod
	def _complete_node(self, node: Node):
		pass

	@abstractmethod
	def queue_worker(self, worker: Worker):
		pass

	@abstractmethod
	def dequeue_worker(self):
		pass

	def complete_node(self, node: Node):
		self._complete_node(node)
		for callback in self.__completion_triggers:
			callback(node)
