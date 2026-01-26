import typing

from apps.allocation.models import Session, Worker
from apps.mca.events import Events
from apps.mca.handlers import GenericWorkerHandler, QueueHandler
from di.mca_providers import MCAProviders


class SelectHandler(GenericWorkerHandler):

	def _handle_session(self, sid: str, session: Session, worker: Worker, data: typing.Any = None):
		worker_queue = MCAProviders.provide_worker_queue(session.id.hex)
		worker_queue.queue(worker)
