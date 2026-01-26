from django.urls import path

from apps.allocation.handlers import RegisterWorkerHandler, SetupCompleteHandler, CreateSessionHandler, \
	DisconnectHandler
from apps.allocation.views import CreateSessionView

urlpatterns = [
	path("core/create-session/", CreateSessionView.as_view(), name="create_session"),
]


sio_mapping = {
	"create-session": CreateSessionHandler,
	"register-worker": RegisterWorkerHandler,
	"setup-complete": SetupCompleteHandler,
	"disconnect": DisconnectHandler,
}