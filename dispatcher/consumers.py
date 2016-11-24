from channels.generic.websockets import WebsocketConsumer


class LogConsumer(WebsocketConsumer):
    http_user = True

    def connect(self, message, **kwargs):
        super(LogConsumer, self).connect(message, **kwargs)

    def receive(self, text=None, bytes=None, **kwargs):
        super(LogConsumer, self).receive(text, bytes, **kwargs)

    def disconnect(self, message, **kwargs):
        super(LogConsumer, self).disconnect(message, **kwargs)
