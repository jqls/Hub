from channels.routing import route

channel_routing = [
    route('submit_mission', 'dispatcher.consumers.submit_mission'),
    route('counter', 'dispatcher.consumers.counter'),
]
