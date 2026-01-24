from rest_framework import serializers


class CreateSessionSerializer(serializers.Serializer):

	branch = serializers.CharField()
	model = serializers.CharField()
	model_temperature = serializers.CharField()
	model_alpha = serializers.CharField(allow_null=True)

	
