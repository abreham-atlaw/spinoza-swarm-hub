from apps.allocation.utils.session_repository import SessionRepository
from apps.mca.events import Events
from apps.mca.models import Node
from di.core_providers import CoreProviders
from di.mca_providers import MCAProviders
from lib.controller import ThreadController
from lib.sio.swarm_server import SwarmServer


class BackpropagationController(ThreadController):

	__sio: SwarmServer = CoreProviders.provide_server()

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__repository = MCAProviders.provide_backpropagate_repository()
		self.__session_repo: SessionRepository = CoreProviders.provide_session_repository()

	def __emit_backpropagation(self, node: Node):
		session = self.__session_repo.get_session_by_id(node.session.id.hex)
		self.__sio.emit(
			Events.backpropagate,
			data={
				"id": self.__repository.get_node_id(node),
				"data": node.data,
			},
			to=session.sid
		)

	def loop(self):
		for node in self.__repository.get_backpropagate_nodes():
			self.__emit_backpropagation(node)
