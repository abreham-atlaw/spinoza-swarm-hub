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


class ServerThread(Process):

	def run(self):
		pass



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
		self.__client = Client()
		self.__client.on(
			"mca-start", self.__handle_mca_start
		)
		self.__client.on(
			"backpropagate", self.__handle_backpropagate
		)

	@staticmethod
	def __handle_backpropagate(state: dict):
		logger.info(f"[Queen]Backpropagate Received: {state}")

	def __handle_mca_start(self, data = None):
		self.__queue_states()

	def __queue_states(self):
		for state in self.QUEUE_STATES:
			self.__client.emit(
				"queue",
				data=state
			)

	def __create_session(self):
		self.__client.emit(
			"create-session",
			data={
				"branch": "branch-0",
				"model": "model-0",
				"model_temperature": 1.0,
				"model_alpha": None
			}
		)

	def run(self):
		logger.info(f"Starting Queen...")
		self.__client.connect("http://127.0.0.1:8000")
		self.__create_session()
		self.__client.wait()


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
		self.__client = Client()
		self.__client.on(
			"setup", self.__handle_setup
		)
		self.__client.on(
			"mca-start", self.__handle_mca_start,
		)
		self.__client.on(
			"select", self.__handle_select
		)
		self.__id = random.randint(0, 100)

	def __handle_mca_start(self, data = None):
		self.__client.emit(
			"select"
		)

	def __handle_setup(self, data = None):
		logger.info(f"[Worker-{self.__id}]Setup Received: {data}")
		self.__client.emit(
			"setup-complete"
		)

	def __handle_select(self, data = None):
		logger.info(f"[Worker-{self.__id}]Select Received: {data}")
		self.__client.emit(
			"backpropagate",
			next(filter(
				lambda s: s["id"] == data["id"],
				self.BACKPROPAGATE_STATES
			))
		)
		self.__client.emit(
			"select"
		)

	def __register_client(self):
		logger.info(f"[Worker-{self.__id}]Registering Worker...")
		self.__client.emit(
			"register-worker",
			data={
				"branch": "branch-0",
			}
		)

	def run(self):
		logger.info(f"[Worker-{self.__id}]Starting Worker...")
		self.__client.connect("http://127.0.0.1:8000")
		self.__register_client()
		self.__client.wait()


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