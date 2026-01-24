from django.apps import AppConfig
from django.db.models.signals import post_migrate

from di.misc_providers import logger


class CoreConfig(AppConfig):
	name = 'apps.core'

	@staticmethod
	def __start_controllers(*args, **kwargs):
		import os
		if os.environ.get("RUN_MAIN") != "true":
			return

		from di.core_providers import CoreProviders
		controllers = CoreProviders.provide_thread_controllers()

		for controller in controllers:
			logger.info(f"Starting {controller.__class__.__name__}")
			controller.start()

	def ready(self):
		self.__start_controllers()
