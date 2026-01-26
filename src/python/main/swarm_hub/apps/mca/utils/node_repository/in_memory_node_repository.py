from apps.mca.exceptions import QueueEmptyException
from apps.mca.models import Node
from apps.mca.utils.node_repository import MCARepository


class InMemoryMCARepository(MCARepository):

	def __init__(self):
		super(InMemoryMCARepository, self).__init__()
		self.__queue = []

	def queue_node(self, node: Node):
		self.__queue.append(node)

	def dequeue_node(self) -> Node:
		if len(self.__queue) == 0:
			raise QueueEmptyException()
		return self.__queue.pop(0)

	def _complete_node(self, node: Node):
		pass
