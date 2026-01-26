from socketio import Server

from di.misc_providers import logger


class SwarmServer:

	def __init__(self, sio: Server):
		self.sio = sio

	def emit(self, event, *args, data=None, to=None, room=None, **kwargs):
		logger.info(f"Outgoing [{event}], to: {to}, room: {room}")
		self.sio.emit(event, *args, data=data, to=to, room=room, **kwargs)

	def is_client_connected(self, sid: str):
		return sid in self.sio.eio.sockets

	def __getattr__(self, name):
		return getattr(self.sio, name)
