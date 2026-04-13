from apps.state_sharing.handlers import StateRequestHandler, StateResponseHandler, BulkStateRequestHandler, \
	BulkStateResponseHandler

sio_mapping = {
	"state_request": StateRequestHandler,
	"state_response": StateResponseHandler,
	"bulk_state_request": BulkStateRequestHandler,
	"bulk_state_response": BulkStateResponseHandler
}