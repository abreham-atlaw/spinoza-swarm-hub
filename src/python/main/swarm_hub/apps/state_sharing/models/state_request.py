from django.db import models

from apps.allocation.models import Worker


class StateRequest(models.Model):

	state_id: str = models.CharField(max_length = 255)
	requester_sid: str = models.CharField(max_length = 255)
	is_responded: bool = models.BooleanField(default = False)
