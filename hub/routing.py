from channels.routing import route
from dispatcher.consumers import processor_runner, submit_mission, ws_receive, ws_connect, ws_disconnect

channel_routing = [
    route('submit_mission', submit_mission),
    route('processor_runner', processor_runner),
    route('websocket.receive', ws_receive),
    route('websocket.connect', ws_connect),
    route('websocket.disconnect', ws_disconnect),
]
