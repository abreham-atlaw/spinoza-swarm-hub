import typing

from apps.allocation.models import Session
from apps.mca.handlers import GenericQueenHandler
from di.mca_providers import MCAProviders
from di.misc_providers import logger


class ClearQueueHandler(GenericQueenHandler):

	def _handle_session(self, sid: str, session: Session, data: typing.Any = None):
		queue = MCAProviders.provide_node_queue(session.id.hex)

		logger.info(f"Clearing queue of size: {len(queue)}")
		queue.clear()
