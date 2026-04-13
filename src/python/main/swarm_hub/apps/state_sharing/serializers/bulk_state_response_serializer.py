import typing

from rest_framework import serializers

from apps.state_sharing.models import BulkStateRequest


class BulkStateResponseSerializer(serializers.Serializer):

	id = serializers.CharField()
	states = serializers.ListSerializer(child=serializers.JSONField(), required=True)
