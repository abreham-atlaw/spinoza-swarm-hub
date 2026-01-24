from rest_framework import serializers

from apps.allocation.models import Session


class SessionSerializer(serializers.ModelSerializer):

	class Meta:
		model = Session
		fields = ["id", "sid", "branch", "model", "model_temperature", "model_alpha"]
