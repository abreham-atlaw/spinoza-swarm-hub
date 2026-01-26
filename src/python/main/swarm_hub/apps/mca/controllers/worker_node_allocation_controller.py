from apps.allocation.models import Worker
from apps.mca.events import Events
from apps.mca.models import Node
from di.core_providers import CoreProviders
from di.mca_providers import MCAProviders


class WorkerNodeAllocationController:

	def __init__(self):
		self._sio = CoreProviders.provide_server()

	def __allocate_node_to_worker(self, session_id: str):
		node_queue = MCAProviders.provide_node_queue(session_id)
		worker_queue = MCAProviders.provide_worker_queue(session_id)

		if node_queue.is_empty() or worker_queue.is_empty():
			return

		node = node_queue.dequeue()
		worker = worker_queue.dequeue()

		self._sio.emit(
			Events.select,
			data=node.data,
			to=worker.sid
		)

	def on_node_queued(self, node: Node):
		self.__allocate_node_to_worker(node.session.id.hex)

	def on_worker_queued(self, worker: Worker):
		self.__allocate_node_to_worker(worker.session.id.hex)
