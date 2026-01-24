import uuid

from django.db import models


class Session(models.Model):

	id: str = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	sid: str = models.CharField(max_length=255)
	branch: str = models.CharField(max_length=100)
	model: str = models.CharField(max_length=100)
	model_temperature: float = models.FloatField()
	model_alpha: float = models.FloatField(null=True)
	is_active: bool = models.BooleanField(default=True)

