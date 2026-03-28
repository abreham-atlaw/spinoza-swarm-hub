import socketio

sio = socketio.Server(async_mode="gevent", max_http_buffer_size=50*1024*1024, ping_timeout=20, ping_interval=25)
