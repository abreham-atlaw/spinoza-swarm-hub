from apps.mca.handlers import QueueHandler, SelectHandler, BackpropagateHandler

sio_mapping = {
	"queue": QueueHandler,
	"select": SelectHandler,
	"backpropagate": BackpropagateHandler,
}
