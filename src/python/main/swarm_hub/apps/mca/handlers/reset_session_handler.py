import typing

from .generic_queen_handler import GenericQueenHandler
from ..events import Events
from ...allocation.models import Session


class ResetSessionHandler(GenericQueenHandler):

	def _handle_session(self, sid: str, session: Session, data: typing.Any = None):
		self._sio.emit(
			Events.reset,
			room=session.room
		)
