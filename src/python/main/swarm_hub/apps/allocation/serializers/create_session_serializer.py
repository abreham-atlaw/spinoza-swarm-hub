from rest_framework import serializers


class CreateSessionSerializer(serializers.Serializer):

	branch = serializers.CharField()

	def to_internal_value(self, data):
		out = super().to_internal_value(data)
		out["configs"] = data
		return out
