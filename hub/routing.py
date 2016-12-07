from channels.routing import route
from dispatcher.consumers import processor_runner, submit_mission

channel_routing = [
    route('websocket.submit_mission', submit_mission),
    route('websocket.processor_runner', processor_runner),
]
