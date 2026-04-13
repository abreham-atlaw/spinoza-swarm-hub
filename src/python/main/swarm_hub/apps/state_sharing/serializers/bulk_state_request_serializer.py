from rest_framework import serializers

from apps.state_sharing.models import BulkStateRequest


class BulkStateRequestSerializer(serializers.ModelSerializer):

	class Meta:
		model=BulkStateRequest
		fields=("id", "states")
