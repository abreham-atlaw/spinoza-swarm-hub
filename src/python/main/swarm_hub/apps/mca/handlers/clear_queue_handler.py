import typing

from apps.allocation.models import Session
from apps.mca.handlers import GenericQueenHandler
from di.mca_providers import MCAProviders


class ClearQueueHandler(GenericQueenHandler):

	def _handle_session(self, sid: str, session: Session, data: typing.Any = None):
		queue = MCAProviders.provide_node_queue(session.id.hex)
		queue.clear()
