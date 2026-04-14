from apps.mca.handlers import QueueHandler, SelectHandler, BackpropagateHandler, ClearQueueHandler, \
	ConfirmBackpropagationHandler, ResetSessionHandler

sio_mapping = {
	"queue": QueueHandler,
	"clear-queue": ClearQueueHandler,
	"select": SelectHandler,
	"backpropagate": BackpropagateHandler,
	"backpropagate-confirm": ConfirmBackpropagationHandler,
	"session-reset": ResetSessionHandler
}
