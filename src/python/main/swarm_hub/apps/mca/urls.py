from apps.mca.handlers import QueueHandler, SelectHandler, BackpropagateHandler, ClearQueueHandler, \
	ConfirmBackpropagationHandler

sio_mapping = {
	"queue": QueueHandler,
	"clear-queue": ClearQueueHandler,
	"select": SelectHandler,
	"backpropagate": BackpropagateHandler,
	"backpropagate-confirm": ConfirmBackpropagationHandler,
}
