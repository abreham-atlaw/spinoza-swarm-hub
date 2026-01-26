import typing

from apps.state_sharing.models import StateRequest
from apps.state_sharing.utils.state_request_repository import StateRequestRepository


class DBStateRequestRepository(StateRequestRepository):

	def get_requests(self) -> typing.List[StateRequest]:
		return list(StateRequest.objects.filter(
			is_responded=False
		))

	def store(self, request: StateRequest):
		request.save()

	def mark_responded(self, request: StateRequest):
		super().mark_responded(request)
		request.save()
