import typing
from abc import ABC, abstractmethod

from apps.state_sharing.models import StateRequest, BulkStateRequest, AbstractStateRequest


class StateRequestRepository(ABC):

	@abstractmethod
	def get_requests(self) -> typing.List[StateRequest]:
		pass

	@abstractmethod
	def get_bulk_requests(self) -> typing.List[BulkStateRequest]:
		pass

	@abstractmethod
	def store(self, request: AbstractStateRequest):
		pass

	def mark_responded(self, request: AbstractStateRequest):
		request.is_responded = True

	def get_by_state_id(self, state_id: str) -> StateRequest:
		return next(filter(
			lambda request: request.state_id == state_id,
			self.get_requests()
		))

	def get_bulk_by_id(self, id: str) -> BulkStateRequest:
		return next(filter(
			lambda request: request.id.hex == id,
			self.get_bulk_requests()
		))
