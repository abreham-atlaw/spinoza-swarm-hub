import typing

from di.misc_providers import logger
from lib.sio import SIOHandler


class ConnectHandler(SIOHandler):

	def _handle(self, sid: str, data: typing.Any = None):
		logger.info(f"{sid} Connected")