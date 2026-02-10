import typing

from rest_framework.exceptions import ValidationError

from apps.allocation.models import Session
from apps.mca.handlers import GenericQueenHandler
from apps.mca.models import Node
from di.mca_providers import MCAProviders


class QueueHandler(GenericQueenHandler):

	def _handle_session(self, sid: str, session: Session, data: typing.Any = None):
		node_queue = MCAProviders.provide_node_queue(session.id.hex)

		if data is None:
			raise ValidationError("Node data not provided.")

		node = Node(
			session=session,
			data=data
		)

		if node not in node_queue:
			node_queue.queue(node)
		else:
			pass