import os
import random
import threading
import unittest
from multiprocessing import Process
from threading import Thread
from time import sleep

import django
from django import test
from socketio import Client

from di.misc_providers import logger


class QueenClientThread(Thread):

	QUEUE_STATES = [
		{
			"id": f"node-{i}",
			"children": []
		}
		for i in range(3)
	]

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._client = Client(logger=True)
		self._client.on(
			"mca-start", self.__handle_mca_start
		)
		self._client.on(
			"backpropagate", self.__handle_backpropagate
		)

	def __handle_backpropagate(self, state: dict):
		self._log(f"Backpropagate Received: {state}")

	def __handle_mca_start(self, data = None):
		self.__queue_states()

	def _log(self, message):
		logger.info(f"[Queen]{message}")

	def __queue_states(self):
		for state in self.QUEUE_STATES:
			self._client.emit(
				"queue",
				data=state
			)

	def __create_session(self):
		self._client.emit(
			"create-session",
			data={
				"branch": "branch-0",
				"model": "model-0",
				"model_temperature": 1.0,
				"model_alpha": None
			}
		)

	def _run_tasks(self):
		pass

	def run(self):
		logger.info(f"Starting Queen...")
		self._client.connect("http://127.0.0.1:8888")
		self.__create_session()
		sleep(20)

		self._run_tasks()
		self._client.wait()


class WorkerClientThread(Thread):

	BACKPROPAGATE_STATES = [
		{
			"id": f"node-{i}",
			"children": [
				"child-1"
			]
		}
		for i in range(3)
	]

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._client = Client()
		self._client.on(
			"setup", self.__handle_setup
		)
		self._client.on(
			"mca-start", self.__handle_mca_start,
		)
		self._client.on(
			"select", self.__handle_select
		)

		self.__id = random.randint(0, 100)

	def __handle_mca_start(self, data = None):
		self._client.emit(
			"select"
		)

	def __handle_setup(self, data = None):
		self._log(f"Setup Received: {data}")
		self._client.emit(
			"setup-complete"
		)

	def __handle_select(self, data = None):
		self._log(f"Select Received: {data}")
		self._client.emit(
			"backpropagate",
			next(filter(
				lambda s: s["id"] == data["id"],
				self.BACKPROPAGATE_STATES
			))
		)
		self._client.emit(
			"select"
		)

	def _log(self, message):
		logger.info(f"[Worker-{self.__id}]{message}")

	def __register_client(self):
		self._log(f"Registering Worker...")
		self._client.emit(
			"register-worker",
			data={
				"branch": "branch-0",
			}
		)

	def _run_tasks(self):
		pass

	def run(self):
		self._log(f"Starting Worker...")
		self._client.connect("http://127.0.0.1:8888")
		self.__register_client()
		sleep(20)
		self._run_tasks()
		self._client.wait()


class MCAIntegrationTest(test.TestCase):

	def setUp(self):
		self.queen_thread = QueenClientThread()
		self.client_thread = WorkerClientThread()
		self.client_threads = [
			WorkerClientThread()
			for _ in range(5)
		]

	def test_single_client(self):
		self.queen_thread.start()
		self.client_thread.start()

		logger.info(f"Waiting for Client...")
		self.client_thread.join()
		self.queen_thread.join()

	def test_multiple_clients(self):
		self.queen_thread.start()
		for thread in self.client_threads:
			thread.start()

		self.queen_thread.join()