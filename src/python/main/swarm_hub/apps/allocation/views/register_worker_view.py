from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class RegisterWorkerView(APIView):

	def post(self, request: Request) -> Response:
