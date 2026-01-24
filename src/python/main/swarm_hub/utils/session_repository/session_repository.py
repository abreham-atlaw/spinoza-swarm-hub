import typing
from abc import ABC, abstractmethod

from apps.allocation.models import Session, Worker


class SessionRepository(ABC):

	@abstractmethod
	def add_session(self, session: Session):
		pass

	@abstractmethod
	def register_worker(self, worker: Worker):
		pass

	@abstractmethod
	def get_sessions(self) -> typing.List[Session]:
		pass

	@abstractmethod
	def get_workers(self) -> typing.List[Worker]:
		pass

	def get_worker_by_sid(self, sid: str) -> Worker:
		return next(filter(
			lambda worker: worker.sid == sid,
			self.get_workers()
		))

	def allocate_worker(self, worker: Worker, session: Session):
		worker.session = session
		worker.stage = Worker.Stage.allocated

	def set_worker_stage(self, worker: Worker, stage: int):
		worker.stage = stage

	def get_free_workers(self, branch: str = None) -> typing.List[Worker]:
		return list(filter(
			lambda worker: (worker.stage == Worker.Stage.unallocated) and (branch is None or worker.branch == branch),
			self.get_workers()
		))

	def get_session_workers(self, session: Session) -> typing.List[Worker]:
		return list(filter(
			lambda worker: worker.session == session,
			self.get_workers()
		))
