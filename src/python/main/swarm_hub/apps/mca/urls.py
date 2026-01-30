from apps.mca.handlers import QueueHandler, SelectHandler, BackpropagateHandler, ClearQueueHandler

sio_mapping = {
	"queue": QueueHandler,
	"clear-queue": ClearQueueHandler,
	"select": SelectHandler,
	"backpropagate": BackpropagateHandler,
}
