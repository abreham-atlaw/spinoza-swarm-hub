import typing
import uuid
from datetime import datetime

from django.db import models

from .abstract_state_request import AbstractStateRequest


class BulkStateRequest(AbstractStateRequest):


	id: uuid.UUID = models.UUIDField(default=uuid.uuid4, primary_key=True)
	states: typing.List[str] = models.JSONField()
