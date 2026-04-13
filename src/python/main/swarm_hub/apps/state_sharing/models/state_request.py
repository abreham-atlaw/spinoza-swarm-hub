from django.db import models

from apps.allocation.models import Worker
from .abstract_state_request import AbstractStateRequest

class StateRequest(AbstractStateRequest):

	state_id: str = models.CharField(max_length = 255)
