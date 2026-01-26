from django import test

from src.python.test.swarm_hub.apps.mca.mca_integration_test import QueenClientThread as OGQueenClientThread, WorkerClientThread as OGWorkerClientThread


class QueenClientThread(OGQueenClientThread):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._client.on("state_request", self.__handle_state_request)
		self._client.on("state_response", self.__handle_state_response)

	def __handle_state_request(self, state_id):
		if state_id != "state-0":
			return
		self._log(f"Received state request for {state_id}")
		self._client.emit(
			"state_response",
			{
				"id": state_id,
				"state": "state-0"
			}
		)

	def __handle_state_response(self, data):
		self._log(f"Received state response: {data}")

	def _run_tasks(self):
		self._log("Emitting state request")
		self._client.emit(
			"state_request",
			"state-1"
		)


class WorkerClientThread(OGWorkerClientThread):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._client.on("state_request", self.__handle_state_request)
		self._client.on("state_response", self.__handle_state_response)

	def __handle_state_request(self, state_id):
		if state_id != "state-1":
			return
		self._log(f"Received state request for {state_id}")
		self._client.emit(
			"state_response",
			{
				"id": state_id,
				"state": "state-1"
			}
		)

	def __handle_state_response(self, data):
		self._log(f"Received state response: {data}")

	def _run_tasks(self):
		self._log("Emitting state request")
		self._client.emit(
			"state_request",
			"state-0"
		)

class StateSharingIntegrationTest(test.TestCase):

	def setUp(self):
		self.queen_thread = QueenClientThread()
		self.worker_thread = WorkerClientThread()

	def test_state_sharing(self):
		self.queen_thread.start()
		self.worker_thread.start()

		self.queen_thread.join()
