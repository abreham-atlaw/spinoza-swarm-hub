import typing

from rest_framework.exceptions import ValidationError

from apps.allocation.models import Session
from apps.mca.handlers import GenericQueenHandler
from di.core_providers import CoreProviders
from di.mca_providers import MCAProviders


class ConfirmBackpropagationHandler(GenericQueenHandler):

	def __init__(self, *args, **kwargs):
		super().__init__()
		self.__bkp_repository = MCAProviders.provide_backpropagate_repository()

	def _handle_session(self, sid: str, session: Session, data: typing.Any = None):
		if data is None:
			raise ValidationError("Session data not provided.")

		node_id = data["id"]
		self.__bkp_repository.confirm_backpropagation(node_id)
