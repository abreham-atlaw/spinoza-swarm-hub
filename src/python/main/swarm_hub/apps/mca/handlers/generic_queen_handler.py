import typing
from abc import abstractmethod, ABC

from apps.allocation.models import Session
from di.core_providers import CoreProviders
from lib.sio import SIOHandler


class GenericQueenHandler(SIOHandler, ABC):

	_session_repository = CoreProviders.provide_session_repository()

	@abstractmethod
	def _handle_session(self, sid: str, session: Session, data: typing.Any = None):
		pass

	def _handle(self, sid: str, data: typing.Any = None):
		session = self._session_repository.get_session_by_sid(sid)
		return self._handle_session(sid, session, data)
