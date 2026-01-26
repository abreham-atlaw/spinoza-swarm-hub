from django.apps import AppConfig



class AllocationConfig(AppConfig):
	name = 'apps.allocation'
	
	def ready(self):
		from apps.allocation.models import Session
		from di.misc_providers import logger

		try:
			logger.info(f"Disconnecting all Sessions...")
			Session.objects.filter(is_active = True).update(is_active = False)
			logger.info(f"Successfully disconnected all Sessions...")
		except Exception as e:
			logger.warning(f"Failed to disconnect all Sessions: {e}")
