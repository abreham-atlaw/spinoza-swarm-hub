import typing
from abc import ABC, abstractmethod
from os import stat_result
from time import sleep

from django import test
from socketio import Client

from src.python.test.swarm_hub.apps.mca.mca_integration_test import QueenClientThread as OGQueenClientThread, WorkerClientThread as OGWorkerClientThread


class StateSharingClient(ABC):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def _setup(self):
		self._sio_client.on("state_request", self.__handle_state_request)
		self._sio_client.on("state_response", self.__handle_state_response)
		self._sio_client.on("bulk_state_request", self.__handle_bulk_state_request)
		self._sio_client.on("bulk_state_response", self.__handle_bulk_state_response)

	@property
	@abstractmethod
	def _available_states(self) -> typing.List[str]:
		pass

	@property
	@abstractmethod
	def _required_states(self) -> typing.List[str]:
		pass

	@property
	@abstractmethod
	def _sio_client(self) -> Client:
		pass

	@abstractmethod
	def _log(self, *args):
		pass

	def __handle_state_request(self, state_id: str):
		self._log(f"Received state request for {state_id}")
		if state_id not in self._available_states:
			return
		self._log(f"Responding to state_request {state_id}")
		self._sio_client.emit(
			"state_response",
			{
				"id": state_id,
				"state": f"State of {state_id}"
			}
		)

	def __handle_state_response(self, data):
		self._log(f"Received state response: {data}")

	def __handle_bulk_state_request(self, data):
		self._log(f"Received bulk_state_request for {data}")

		if data["states"][0] == self._available_states[0]:
			self._log(f"Responding to bulk_state_request")
			self._sio_client.emit(
				"bulk_state_response",
				{
					"id": data["id"],
					"states": [
						{
							"id": state,
							"state": f"state_{state}"
						}
						for state in self._available_states
					]
				}
			)

	def __handle_bulk_state_response(self, data):
		self._log(f"Received bulk_state_reponse for {data}")

	def _emit_state_requests(self):
		for state_id in self._required_states:
			self._log(f"Emitting state request for {state_id}")
			self._sio_client.emit(
				"state_request",
				state_id
			)

	def _emit_bulk_state_request(self):
		self._log(f"Emitting Bulk State Request")
		self._sio_client.emit(
			"bulk_state_request",
			{
				"states": self._required_states
			}
		)


class QueenClientThread(OGQueenClientThread, StateSharingClient):

	@property
	def _sio_client(self) -> Client:
		return self._client

	@property
	def _available_states(self) -> typing.List[str]:
		return [
			f"state_{i}"
			for i in range(0, 10)
			if i % 2 == 0
		]

	@property
	def _required_states(self) -> typing.List[str]:
		return [
			f"state_{i}"
			for i in range(0, 10)
			if i % 2 == 1
		]

	def _run_tasks(self):
		self._setup()
		sleep(30)
		self._log("Emitting state requests...")
		for i in range(10):
			self._emit_bulk_state_request()
			sleep(5)


class WorkerClientThread(OGWorkerClientThread, StateSharingClient):

	@property
	def _sio_client(self) -> Client:
		return self._client

	@property
	def _available_states(self) -> typing.List[str]:
		return [
			f"state_{i}"
			for i in range(0, 10)
			if i % 2 == 1
		]

	@property
	def _required_states(self) -> typing.List[str]:
		return [
			f"state_{i}"
			for i in range(0, 10)
			if i % 2 == 0
		]

	def _run_tasks(self):
		self._setup()
		sleep(20)
		self._log("Emitting state requests...")
		self._emit_state_requests()
		self._sio_client.wait()

class StateSharingIntegrationTest(test.TestCase):

	def setUp(self):
		self.queen_thread = QueenClientThread()
		self.worker_thread = WorkerClientThread()

	def test_state_sharing(self):
		self.queen_thread.start()
		self.worker_thread.start()

		self.worker_thread.join()
		print(f"Worker thread Complete")
		self.queen_thread.join()
		print(f"Worker thread Complete")
