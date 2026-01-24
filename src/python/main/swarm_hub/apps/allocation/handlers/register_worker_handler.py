import typing

from apps.allocation.models import Worker
from di.core_providers import CoreProviders
from lib.sio import SIOHandler
from utils.session_repository import SessionRepository


class RegisterWorkerHandler(SIOHandler):

	__session_repository: SessionRepository = CoreProviders.provide_session_repository()

	def _handle(self, sid: str, data: typing.Any = None):
		worker = Worker(
			sid=sid,
			branch=data["branch"]
		)

		self.__session_repository.register_worker(worker)
