import typing

from .state_sharing_handler import StateSharingHandler
from ..events import Events
from ..models import BulkStateRequest
from ..serializers import BulkStateRequestSerializer
from ..utils.state_request_repository import StateRequestRepository
from ...allocation.models import Session


class BulkStateRequestHandler(StateSharingHandler):

	def _handle_session(self, sid: str, session: Session, repository: StateRequestRepository, data: typing.Any = None):
		request = BulkStateRequest(
			states=data["states"],
			requester_sid=sid
		)

		repository.store(request)

		serializer = BulkStateRequestSerializer(instance=request)

		self._sio.emit(
			Events.bulk_state_request,
			data=serializer.data,
			room=session.room
		)
