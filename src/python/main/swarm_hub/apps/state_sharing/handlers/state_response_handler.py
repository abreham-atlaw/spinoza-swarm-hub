import typing

from .state_sharing_handler import StateSharingHandler
from ..events import Events
from ..utils.state_request_repository import StateRequestRepository
from ...allocation.models import Session


class StateResponseHandler(StateSharingHandler):

	def _handle_session(self, sid: str, session: Session, repository: StateRequestRepository, data: typing.Any = None):
		state_id = data["id"]

		request = repository.get_by_state_id(state_id)
		repository.mark_responded(request)

		self._sio.emit(
			Events.state_response,
			data=data,
			to=request.requester_sid
		)
		