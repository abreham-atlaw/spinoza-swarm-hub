import typing

from apps.allocation.events import Events
from apps.allocation.models import Worker
from apps.allocation.serializers import SessionSerializer
from di.core_providers import CoreProviders
from lib.controller import ThreadController
from utils.session_repository import SessionRepository


class WorkerAllocationController(ThreadController):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__server = CoreProviders.provide_server()
		self.__session_repository: SessionRepository = CoreProviders.provide_session_repository()

	def __get_unprepared_workers(self) -> typing.List[Worker]:
		return list(filter(
			lambda worker: worker.stage == Worker.Stage.allocated,
			self.__session_repository.get_workers()
		))

	def __get_prepared_workers(self) -> typing.List[Worker]:
		return list(filter(
			lambda worker: worker.stage == Worker.Stage.prepared,
			self.__session_repository.get_workers()
		))

	def __prepare_worker(self, worker: Worker):
		self.__server.emit(
			Events.setup,
			data=SessionSerializer(instance=worker.session).data,
			to=worker.sid
		)
		self.__session_repository.set_worker_stage(worker, Worker.Stage.setup)

	def __run_worker(self, worker: Worker):
		self.__server.enter_room(worker.sid, worker.session.id)
		self.__server.emit(
			Events.mca_start,
			to=worker.sid
		)
		self.__session_repository.set_worker_stage(worker, Worker.Stage.running)

	def __prepare_workers(self):
		workers = self.__get_unprepared_workers()
		for worker in workers:
			self.__prepare_worker(worker)

	def __run_workers(self):
		workers = self.__get_prepared_workers()
		for worker in workers:
			self.__run_worker(worker)

	def loop(self):
		self.__prepare_workers()
		self.__run_workers()
