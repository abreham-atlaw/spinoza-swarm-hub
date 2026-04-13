from django.db import models


class AbstractStateRequest(models.Model):

	requester_sid: str = models.CharField(max_length=255)
	is_responded: bool = models.BooleanField(default=False)

	class Meta:
		abstract = True