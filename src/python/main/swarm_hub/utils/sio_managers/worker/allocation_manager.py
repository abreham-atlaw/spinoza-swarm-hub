from socketio import Server

from apps.allocation.models import Session, Worker


class AllocationManager:

	def __init__(self, server: Server):
		self.__server = server

	def allocate_worker(self, worker: Worker, session: Session):

