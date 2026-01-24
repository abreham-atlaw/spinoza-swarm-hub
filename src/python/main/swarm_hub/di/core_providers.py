import logging
import typing

from socketio import Server

from lib.cache.decorators import CacheDecorators
from lib.controller import ThreadController
from swarm_hub import settings
from utils.session_repository import SessionRepository, DBSessionRepository


class CoreProviders:

	@staticmethod
	def provide_server() -> Server:
		from swarm_hub.sio import sio
		return sio

	@staticmethod
	@CacheDecorators.singleton()
	def provide_session_repository() -> SessionRepository:
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

