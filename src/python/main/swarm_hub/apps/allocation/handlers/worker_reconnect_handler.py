import typing

from rest_framework.exceptions import ValidationError

from apps.allocation.events import Events
from apps.allocation.models import Worker
from apps.allocation.utils.session_repository import SessionRepository
from di.core_providers import CoreProviders
from lib.sio import SIOHandler


class WorkerReconnectHandler(SIOHandler):

	__session_repository: SessionRepository = CoreProviders.provide_session_repository()

	def _handle(self, sid: str, data: typing.Any = None):
		if data is None:
			raise ValidationError(f"Received empty data for worker-reconnect.")

		id = data["id"]
		worker = self.__session_repository.get_worker_by_id(id)
		self.__session_repository.set_worker_sid(worker, sid)
		self.__session_repository.set_worker_stage(worker, Worker.Stage.running)

		self._sio.enter_room(
			sid,
			worker.session.room
		)
		self._sio.emit(
			Events.mca_resume,
			to=sid
		)


