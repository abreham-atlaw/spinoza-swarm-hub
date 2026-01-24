import typing

from socketio import Server

from lib.sio import SIOHandler


class SIOUtils:

	@staticmethod
	def __make_handler(handler, event):
		def _inner(*args, **kwargs):
			return handler.handle(*args, **kwargs, event=event)
		return _inner

	@staticmethod
	def map_events(sio: Server, events_map: typing.Dict[str, SIOHandler]):
		for event, handler in events_map.items():
			sio.on(event, SIOUtils.__make_handler(handler, event))
