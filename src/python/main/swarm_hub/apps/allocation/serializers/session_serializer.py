from rest_framework import serializers

from apps.allocation.models import Session


class SessionSerializer(serializers.ModelSerializer):

	class Meta:
		model = Session
		fields = ["id", "sid", "branch", "configs"]

	def to_representation(self, instance: Session):
		data = super().to_representation(instance)
		data.update(data.pop("configs"))
		return data
