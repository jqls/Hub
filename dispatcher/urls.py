from django.conf.urls import url

from dispatcher.views import submit_mission_view, get_inputs_view, emit_outputs_view, get_parameters_view, visualization_view

app_name = 'dispatcher'

urlpatterns = [
    url(r'^submit_mission/(?P<parameter>\d+)/$', submit_mission_view, name='submit_mission'),
    url(r'^get_inputs/(.+)/$', get_inputs_view, name='get_inputs'),
    url(r'^emit_outputs/(.+)/$', emit_outputs_view, name='emit_outputs'),
    url(r'^get_parameters/(.+)/$', get_parameters_view, name='get_parameters'),
    url(r'^visualization/(.+)/$', visualization_view, name='visualization'),
]
