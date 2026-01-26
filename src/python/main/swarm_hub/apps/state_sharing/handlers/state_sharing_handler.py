import typing
from abc import abstractmethod, ABC

from apps.allocation.models import Session
from apps.allocation.utils.session_repository import SessionRepository
from apps.state_sharing.utils.state_request_repository import StateRequestRepository
from di.core_providers import CoreProviders
from di.state_sharing_providers import StateSharingProvider
from lib.sio import SIOHandler


class StateSharingHandler(SIOHandler, ABC):

	__session_repository: SessionRepository = CoreProviders.provide_session_repository()

	@abstractmethod
	def _handle_session(self, sid: str, session: Session, repository: StateRequestRepository, data: typing.Any = None):
		pass

	def __get_session(self, sid: str) -> Session:

		try:
			return self.__session_repository.get_worker_by_sid(sid).session
		except Exception:
			return self.__session_repository.get_session_by_sid(sid)

	def _handle(self, sid: str, data: typing.Any = None):
		session = self.__get_session(sid)
		repository = StateSharingProvider.provide_state_request_repository(session.id.hex)

		self._handle_session(sid, session, repository, data)
