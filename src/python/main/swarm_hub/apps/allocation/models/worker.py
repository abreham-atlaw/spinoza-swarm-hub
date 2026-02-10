import uuid

from django.db import models

from .session import Session


class Worker(models.Model):

	class Stage:
		unallocated = 0
		allocated = 1
		setup = 2
		prepared = 3
		running = 4
		disconnected = 5


	id: uuid.UUID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	branch: str = models.CharField(max_length=255)
	sid: str = models.CharField(max_length=255)
	session: Session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True)
	stage: int = models.IntegerField(default=Stage.unallocated)
