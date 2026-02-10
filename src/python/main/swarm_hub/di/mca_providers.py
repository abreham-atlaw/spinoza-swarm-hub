import typing

from apps.allocation.models import Worker, Session
from apps.mca.models import Node
from apps.mca.utils.queue import Queue, InMemoryQueue
from lib.cache.decorators import CacheDecorators


class MCAProviders:

	@staticmethod
	@CacheDecorators.singleton()
	def provide_node_completion_controller() -> 'WorkerNodeAllocationController':
		from apps.mca.controllers import WorkerNodeAllocationController
		return WorkerNodeAllocationController()

	@staticmethod
	@CacheDecorators.singleton()
	def provide_node_queue_triggers() -> typing.List[typing.Callable[[Node], None]]:
		return [
			MCAProviders.provide_node_completion_controller().on_node_queued
		]

	@staticmethod
	@CacheDecorators.singleton()
	def provide_worker_queue_triggers() -> typing.List[typing.Callable[[Worker], None]]:
		return [
			MCAProviders.provide_node_completion_controller().on_worker_queued
		]

	@staticmethod
	@CacheDecorators.singleton()
	def provide_node_queue(session_id: Session) -> Queue[Node]:
		repository: Queue[Node] = InMemoryQueue(
			compare_fn=lambda node1, node2: node1.data == node2.data
		)
		for trigger in MCAProviders.provide_node_queue_triggers():
			repository.add_queue_trigger(trigger)
		return repository

	@staticmethod
	@CacheDecorators.singleton()
	def provide_worker_queue(session_id: str) -> Queue[Worker]:
		repository: Queue[Worker] = InMemoryQueue()
		for trigger in MCAProviders.provide_worker_queue_triggers():
			repository.add_queue_trigger(trigger)
		return repository
