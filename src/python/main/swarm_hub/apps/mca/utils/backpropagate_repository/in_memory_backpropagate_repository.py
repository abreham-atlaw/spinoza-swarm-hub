import hashlib
import typing

from .backpropagate_repository import BackpropagateRepository
from ...models import Node


class InMemoryBackpropagateRepository(BackpropagateRepository):

	def __init__(self):
		super().__init__()
		self.__nodes = []

	def backpropagate_node(self, node: Node):
		self.__nodes.append(node)

	def confirm_backpropagation(self, node_id: str):
		try:
			node = next(filter(
				lambda n: self.get_node_id(n) == node_id,
				self.__nodes
			))
			self.__nodes.remove(node)
		except StopIteration:
			pass

	def get_backpropagate_nodes(self) -> typing.List[Node]:
		return self.__nodes

	def get_node_id(self, node: Node) -> str:
		return hashlib.sha256(str(node.data).encode("utf-8")).hexdigest()
