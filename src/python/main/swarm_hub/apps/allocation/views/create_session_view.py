from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.allocation.models import Session
from apps.allocation.serializers import CreateSessionSerializer, SessionSerializer


class CreateSessionView(APIView):

	def post(self, request: Request, *args, **kwargs) -> Response:

		serializer = CreateSessionSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		session = Session.objects.create(**serializer.validated_data)

		serializer = SessionSerializer(session)
		return Response(serializer.data)
