import typing

from apps.allocation.models import Session
from apps.allocation.serializers import CreateSessionSerializer
from di.core_providers import CoreProviders
from lib.sio import SIOHandler
from utils.session_repository import SessionRepository


class CreateSessionHandler(SIOHandler):

	__session_repository: SessionRepository = CoreProviders.provide_session_repository()
	__sio = CoreProviders.provide_server()

	def _handle(self, sid: str, data: typing.Any = None):
		serializer = CreateSessionSerializer(data=data)
		serializer.is_valid(raise_exception=True)

		session = Session(**serializer.validated_data, sid=sid)

		self.__session_repository.add_session(session)

		self.__sio.enter_room(sid, session.id)
		self.__sio.emit(
			"mca-start"
		)
