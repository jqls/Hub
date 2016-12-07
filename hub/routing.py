from channels.routing import route
from dispatcher.consumers import processor_runner, submit_mission, log_output

channel_routing = [
    route('submit_mission', submit_mission),
    route('processor_runner', processor_runner),
    route('log_output', log_output),
]
