import typing
from abc import ABC, abstractmethod

from apps.state_sharing.models import StateRequest


class StateRequestRepository(ABC):

	@abstractmethod
	def get_requests(self) -> typing.List[StateRequest]:
		pass

	@abstractmethod
	def store(self, request: StateRequest):
		pass

	def mark_responded(self, request: StateRequest):
		request.is_responded = True

	def get_by_state_id(self, state_id: str) -> StateRequest:
		return next(filter(
			lambda request: request.state_id == state_id,
			self.get_requests()
		))
