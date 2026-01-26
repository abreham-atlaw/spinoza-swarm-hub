import typing

from rest_framework.exceptions import ValidationError

from apps.allocation.models import Session, Worker
from apps.mca.events import Events
from apps.mca.handlers import GenericWorkerHandler


class BackpropagateHandler(GenericWorkerHandler):

	def _handle_session(self, sid: str, session: Session, worker: Worker, data: typing.Any = None):

		if data is None:
			raise ValidationError("Node data not provided.")

		self._sio.emit(
			Events.backpropagate,
			data=data,
			to=session.sid
		)
