import typing

from django.shortcuts import get_object_or_404

from .state_sharing_handler import StateSharingHandler
from apps.state_sharing.events import Events
from apps.state_sharing.models import BulkStateRequest
from apps.state_sharing.serializers import BulkStateResponseSerializer
from apps.state_sharing.utils.state_request_repository import StateRequestRepository
from apps.allocation.models import Session


class BulkStateResponseHandler(StateSharingHandler):

	@staticmethod
	def __find_state_request(state_ids: typing.List[str], repository: StateRequestRepository) -> BulkStateRequest:
		open_requests = repository.get_bulk_requests()
		for request in open_requests:
			if state_ids in request.states:
				return request
		return None

	def _handle_session(self, sid: str, session: Session, repository: StateRequestRepository, data: typing.Any = None):

		serializer = BulkStateResponseSerializer(data=data)
		serializer.is_valid(raise_exception=True)


		request = repository.get_bulk_by_id(id=serializer.validated_data["id"])

		repository.mark_responded(request)

		self._sio.emit(
			Events.bulk_state_response,
			data=serializer.data,
			to=request.requester_sid
		)
