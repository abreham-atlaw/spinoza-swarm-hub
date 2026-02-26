import typing

from rest_framework.exceptions import ValidationError

from apps.allocation.models import Session, Worker
from apps.mca.events import Events
from apps.mca.handlers import GenericWorkerHandler
from apps.mca.models import Node
from di.mca_providers import MCAProviders


class BackpropagateHandler(GenericWorkerHandler):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__confirmed = False
		self.__repository = MCAProviders.provide_backpropagate_repository()

	def _handle_session(self, sid: str, session: Session, worker: Worker, data: typing.Any = None):

		if data is None:
			raise ValidationError("Node data not provided.")

		self.__repository.backpropagate_node(
			node=Node(
				data=data,
				session=session,
			)
		)
