import math
import random
import typing

from apps.allocation.models import Session, Worker
from di.core_providers import CoreProviders
from lib.controller import ThreadController


class SessionController(ThreadController):

	def __init__(
			self,
			wait_time: float = 1.0,
	):
		super().__init__()
		self.__wait_time = wait_time
		self.__repository = CoreProviders.provide_session_repository()

	def __get_session_workers_counts(self) -> typing.Dict[Session, int]:
		return {
			session: len(self.__repository.get_session_workers(session))
			for session in self.__repository.get_sessions()
		}

	def _allocate_worker(self, worker: Worker, session: Session):
		self.__repository.allocate_worker(worker, session)

	def _allocate_branch_workers(self, sessions: typing.List[Session], workers: typing.List[Worker]):
		workers = workers.copy()
		sessions = sessions.copy()

		allocation_map = {
			session: len(self.__repository.get_session_workers(session))
			for session in sessions
		}

		target_workers = int(math.ceil((len(workers) + sum(allocation_map.values()))/len(sessions)))
		target_allocation_map = {
			session: max(target_workers - allocation_map[session], 0)
			for session in sessions
		}

		random.shuffle(sessions)

		for session in sessions:
			target = target_allocation_map[session]
			for i in range(target):
				if len(workers) == 0:
					break
				self._allocate_worker(workers.pop(), session)

	def allocate_workers(self):
		all_sessions = self.__repository.get_sessions()

		branches = list(map(
			lambda session: session.branch,
			all_sessions
		))

		for branch in branches:
			self._allocate_branch_workers(
				sessions=list(filter(
					lambda session: session.branch == branch,
					all_sessions
				)),
				workers=self.__repository.get_free_workers(branch=branch)
			)

	def loop(self):
		self.allocate_workers()
