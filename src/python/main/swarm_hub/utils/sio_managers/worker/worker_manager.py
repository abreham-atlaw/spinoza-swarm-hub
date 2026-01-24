from socketio import Server

from apps.allocation.models import Worker, Session
from .allocation_manager import AllocationManager


class WorkerManager:

	def __init__(
			self,
			server: Server,
	):
		self.__server = server
		self.__allocation_manager = AllocationManager(server)

	def allocate_worker(self, worker: Worker, session: Session):
		self.__allocation_manager.allocate_worker(worker, session)
