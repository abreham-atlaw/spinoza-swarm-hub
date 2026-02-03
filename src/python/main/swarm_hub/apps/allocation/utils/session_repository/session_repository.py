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
	def _get_sessions(self) -> typing.List[Session]:
		pass

	@abstractmethod
	def get_workers(self) -> typing.List[Worker]:
		pass

	def get_sessions(self):
		return list(filter(
			lambda session: session.is_active,
			self._get_sessions()
		))

	def activate_session(self, session: Session):
		session.is_active = True

	def disconnect_session(self, session: Session):
		session.is_active = False

	def get_session_by_sid(self, sid: str) -> Session:
		return next(filter(
			lambda session: session.sid == sid,
			self.get_sessions()
		))

	def get_session_by_id(self, id: str) -> Session:
		return next(filter(
			lambda session: session.id.hex == id,
			self._get_sessions()
		))

	def set_session_sid(self, session: Session, sid: str):
		session.sid = sid

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
