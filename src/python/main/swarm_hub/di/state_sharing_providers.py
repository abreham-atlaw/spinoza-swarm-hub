from apps.state_sharing.utils.state_request_repository import StateRequestRepository, DBStateRequestRepository
from lib.cache.decorators import CacheDecorators


class StateSharingProvider:

	@staticmethod
	@CacheDecorators.singleton()
	def provide_state_request_repository(session_id: str) -> StateRequestRepository:
		return DBStateRequestRepository()
