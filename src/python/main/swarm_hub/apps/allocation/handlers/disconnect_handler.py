import typing

from apps.allocation.models import Worker
from apps.allocation.utils.session_repository import SessionRepository
from di.core_providers import CoreProviders
from lib.sio import SIOHandler


class DisconnectHandler(SIOHandler):

	__session_repository: SessionRepository = CoreProviders.provide_session_repository()

	def __disconnect_session(self, sid: str):
		session = self.__session_repository.get_session_by_sid(sid)
		self.__session_repository.disconnect_session(session)

	def __disconnect_worker(self, sid: str):
		worker = self.__session_repository.get_worker_by_sid(sid)
		self.__session_repository.set_worker_stage(worker, Worker.Stage.disconnected)

	def _handle(self, sid: str, data: typing.Any = None):
		for func in [self.__disconnect_session, self.__disconnect_worker]:
			try:
				func(sid)
			except StopIteration:
				pass
