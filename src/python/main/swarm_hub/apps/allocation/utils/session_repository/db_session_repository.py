import typing

from django.db.models import Q

from apps.allocation.models import Worker, Session
from di.core_providers import CoreProviders
from .session_repository import SessionRepository

class DBSessionRepository(SessionRepository):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__sio = CoreProviders.provide_server()

	def add_session(self, session: Session):
		session.save()

	def register_worker(self, worker: Worker):
		worker.save()

	def _get_sessions(self) -> typing.List[Session]:
		return Session.objects.all()

	def activate_session(self, session: Session):
		super().activate_session(session)
		session.save()

	def disconnect_session(self, session: Session):
		super().disconnect_session(session)
		session.save()

	def set_session_sid(self, session: Session, sid: str):
		super().set_session_sid(session, sid)
		session.save()

	def get_workers(self) -> typing.List[Worker]:
		return list(Worker.objects.filter(
			~Q(stage=Worker.Stage.disconnected)
		))

	def get_worker_by_sid(self, sid: str) -> Worker:
		return Worker.objects.get(sid=sid)

	def get_worker_by_id(self, id: str):
		return Worker.objects.get(
			id=id
		)

	def allocate_worker(self, worker: Worker, session: Session):
		super().allocate_worker(worker, session)
		worker.save()

	def set_worker_stage(self, worker: Worker, stage: int):
		super().set_worker_stage(worker, stage)
		worker.save()

	def set_worker_sid(self, worker: Worker, sid: str):
		super().set_worker_sid(worker, sid)
		worker.save()