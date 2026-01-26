import traceback
import typing
from abc import ABC, abstractmethod

from rest_framework.exceptions import ValidationError

from di.core_providers import CoreProviders
from di.misc_providers import logger
from lib.sio.events import Events


class SIOHandler(ABC):

	_sio = CoreProviders.provide_server()

	@abstractmethod
	def _handle(self, sid: str, data: typing.Any = None):
		pass

	@classmethod
	def handle(cls: typing.Type['SIOHandler'], sid: str, data=None, event=None):
		logger.info(f"Incoming [{event}], sid: {sid}")
		instance = cls()
		try:
			instance._handle(sid, data)
		except Exception as ex:

			message = str(ex)
			if isinstance(ex, ValidationError):
				message = ex.detail

			cls._sio.emit(
				Events.errors,
				data={
					"type": ex.__class__.__name__,
					"message": message
				},
				to=sid
			)
			logger.error(message)
			traceback.print_exc()
