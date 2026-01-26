import uuid

from django.db import models

from apps.allocation.models import Session


class Node(models.Model):

	data: str = models.TextField()
	session: Session = models.ForeignKey(Session, on_delete=models.CASCADE)
