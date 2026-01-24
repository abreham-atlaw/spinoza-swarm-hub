import typing

from django.db.models import Q

from apps.allocation.models import Worker, Session
from .session_repository import SessionRepository

class DBSessionRepository(SessionRepository):

	def add_session(self, session: Session):
		session.save()

	def register_worker(self, worker: Worker):
		worker.save()

	def get_sessions(self) -> typing.List[Session]:
		return list(Session.objects.all())

	def get_workers(self) -> typing.List[Worker]:
		return list(Worker.objects.filter(
			~Q(stage=Worker.Stage.disconnected)
		))

	def get_worker_by_sid(self, sid: str) -> Worker:
		return Worker.objects.get(sid=sid)

	def allocate_worker(self, worker: Worker, session: Session):
		super().allocate_worker(worker, session)
		worker.save()

	def set_worker_stage(self, worker: Worker, stage: int):
		super().set_worker_stage(worker, stage)
		worker.save()
