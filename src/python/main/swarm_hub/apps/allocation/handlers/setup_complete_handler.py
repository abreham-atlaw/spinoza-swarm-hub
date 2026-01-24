import typing

from apps.allocation.models import Worker
from di.core_providers import CoreProviders
from lib.sio import SIOHandler


class SetupCompleteHandler(SIOHandler):

	__repository = CoreProviders.provide_session_repository()
	__server = CoreProviders.provide_server()

	def _handle(self, sid: str, data: typing.Any = None):
		worker = self.__repository.get_worker_by_sid(sid)
		self.__repository.set_worker_stage(worker, Worker.Stage.prepared)
