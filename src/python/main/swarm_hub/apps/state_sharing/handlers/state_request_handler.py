import typing

from apps.allocation.models import Session, Worker
from apps.allocation.utils.session_repository import SessionRepository
from apps.state_sharing.events import Events
from apps.state_sharing.models import StateRequest
from .state_sharing_handler import StateSharingHandler
from ..utils.state_request_repository import StateRequestRepository


class StateRequestHandler(StateSharingHandler):

	def _handle_session(self, sid: str, session: Session, repository: StateRequestRepository, data: typing.Any = None):

		request = StateRequest(
			state_id=data,
			requester_sid=sid
		)

		repository.store(request)

		self._sio.emit(
			Events.state_request,
			data=data,
			room=session.room,
		)
