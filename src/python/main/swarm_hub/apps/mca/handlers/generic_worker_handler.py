import typing
from abc import abstractmethod, ABC

from apps.allocation.models import Session, Worker
from apps.allocation.utils.session_repository import SessionRepository
from di.core_providers import CoreProviders
from lib.sio import SIOHandler


class GenericWorkerHandler(SIOHandler, ABC):

	_session_repository: SessionRepository = CoreProviders.provide_session_repository()

	@abstractmethod
	def _handle_session(self, sid: str, session: Session, worker: Worker, data: typing.Any = None):
		pass

	def _handle(self, sid: str, data: typing.Any = None):
		worker = self._session_repository.get_worker_by_sid(sid)
		session = worker.session
		return self._handle_session(sid, session, worker, data)
