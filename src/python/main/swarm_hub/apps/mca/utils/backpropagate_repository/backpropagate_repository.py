import typing
from abc import ABC, abstractmethod

from apps.mca.models import Node


class BackpropagateRepository(ABC):

	@abstractmethod
	def backpropagate_node(self, node: Node):
		pass

	@abstractmethod
	def confirm_backpropagation(self, node_id: str):
		pass

	@abstractmethod
	def get_backpropagate_nodes(self) -> typing.List[Node]:
		pass

	@abstractmethod
	def get_node_id(self, node: Node) -> str:
		pass
