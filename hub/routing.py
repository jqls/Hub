from channels.routing import route, route_class


channel_routing = [
    route_class('dispatcher.consumers.LogConsumer', path='^/log/')
]
