import logging

from lib.cache.decorators import CacheDecorators


class MiscProviders:

	@staticmethod
	@CacheDecorators.singleton()
	def provide_logger():
		from swarm_hub import settings
		return logging.getLogger(settings.DEFAULT_LOGGING_ID)


logger = MiscProviders.provide_logger()
