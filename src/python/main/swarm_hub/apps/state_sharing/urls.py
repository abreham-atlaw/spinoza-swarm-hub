from apps.state_sharing.handlers import StateRequestHandler, StateResponseHandler

sio_mapping = {
	"state_request": StateRequestHandler,
	"state_response": StateResponseHandler,
}