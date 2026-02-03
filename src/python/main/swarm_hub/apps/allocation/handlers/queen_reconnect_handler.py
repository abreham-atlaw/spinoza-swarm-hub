import typing

from rest_framework.exceptions import ValidationError

from apps.allocation.utils.session_repository import SessionRepository
from di.core_providers import CoreProviders
from lib.sio import SIOHandler


class QueenReconnectHandler(SIOHandler):

	__session_repository: SessionRepository = CoreProviders.provide_session_repository()

	def _handle(self, sid: str, data: typing.Any = None):
		if data is None:
			raise ValidationError(f"Received empty data for queen-reconnect.")

		id = data["id"]
		session = self.__session_repository.get_session_by_id(id)
		self.__session_repository.set_session_sid(session, sid)
		self.__session_repository.activate_session(session)

		self._sio.emit(
			"mca-resume",
			to=sid
		)
