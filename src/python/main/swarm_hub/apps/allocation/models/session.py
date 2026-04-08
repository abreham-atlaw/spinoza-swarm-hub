import typing
import uuid

from django.db import models


class Session(models.Model):

	id: uuid.UUID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	sid: str = models.CharField(max_length=255)
	branch: str = models.CharField(max_length=100)
	configs: typing.Dict[str, typing.Any] = models.JSONField()
	is_active: bool = models.BooleanField(default=True)

	@property
	def room(self) -> str:
		return self.id.hex
