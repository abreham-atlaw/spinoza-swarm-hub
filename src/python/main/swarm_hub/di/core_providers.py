import typing

from lib.cache.decorators import CacheDecorators
from lib.controller import ThreadController


class CoreProviders:

	@staticmethod
	def provide_server() -> 'SwarmServer':
		from swarm_hub.sio import sio
		from lib.sio.swarm_server import SwarmServer
		return SwarmServer(sio)

	@staticmethod
	@CacheDecorators.singleton()
	def provide_session_repository() -> 'SessionRepository':
		from apps.allocation.utils.session_repository import DBSessionRepository
		return DBSessionRepository()

	@staticmethod
	@CacheDecorators.singleton()
	def provide_thread_controllers() -> typing.List[ThreadController]:
		from apps.allocation.controllers import SessionController
		from apps.allocation.controllers import WorkerAllocationController

		return [
			SessionController(),
			WorkerAllocationController()
		]

