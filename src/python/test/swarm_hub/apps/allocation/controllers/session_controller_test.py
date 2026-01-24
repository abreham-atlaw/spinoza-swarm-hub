import random
import uuid
from time import sleep

from django import test

from apps.allocation.controllers import SessionController
from apps.allocation.models import Session, Worker
from di.core_providers import CoreProviders


class SessionControllerTest(test.TestCase):

	def init_sessions(self):
		self.sessions = [
			Session(
				sid=f"{uuid.uuid4().hex}",
				branch=f"branch-{b}",
				model=f"model-{m}",
				model_temperature=1.0,
				model_alpha=None
			)

			for b in range(2)
			for m in range(2)
		]
		return self.sessions

	def init_workers(self):
		self.workers = [
			Worker(
				sid=f"{uuid.uuid4().hex}",
				branch=f"branch-{b}"
			)
			for b in range(2)
			for _ in range(5)
		]
		return self.workers

	def setUp(self):
		self.controller = SessionController()
		self.repository = CoreProviders.provide_session_repository()

	def test_manual_allocate(self):
		sessions, workers = self.init_sessions(), self.init_workers()

		for session in sessions:
			self.repository.add_session(session)

		for worker in workers:
			self.repository.register_worker(worker)

		self.assertEqual(len(self.repository.get_free_workers()), len(self.workers))
		self.controller.allocate_workers()
		self.assertEqual(len(self.repository.get_free_workers()), 0)
		for session in self.sessions:
			self.assertIn(
				len(self.repository.get_session_workers(session)),
				[
					2, 3
				]
			)

	def test_auto_allocate(self):
		self.init_sessions()
		self.init_workers()

		self.controller.start()


		for worker in self.workers:
			self.repository.register_worker(worker)

		self.assertEqual(len(self.repository.get_free_workers()), len(self.workers))
		for session in self.sessions:
			self.repository.add_session(session)

		sleep(10)

		self.assertEqual(len(self.repository.get_free_workers()), 0)
		for session in self.sessions:
			self.assertEqual(len(self.repository.get_session_workers(session)), 5)
