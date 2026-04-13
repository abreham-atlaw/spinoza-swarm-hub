import typing

from apps.state_sharing.models import StateRequest, BulkStateRequest, AbstractStateRequest
from apps.state_sharing.utils.state_request_repository import StateRequestRepository


class DBStateRequestRepository(StateRequestRepository):

	def get_requests(self) -> typing.List[StateRequest]:
		return list(StateRequest.objects.filter(
			is_responded=False
		))

	def get_bulk_requests(self) -> typing.List[BulkStateRequest]:
		return list(BulkStateRequest.objects.filter(
			is_responded=False
		))

	def store(self, request: AbstractStateRequest):
		request.save()

	def mark_responded(self, request: AbstractStateRequest):
		super().mark_responded(request)
		request.save()

	def get_bulk_by_id(self, id: str) -> BulkStateRequest:
		return BulkStateRequest.objects.get(
			id=id,
			is_responded=False
		)