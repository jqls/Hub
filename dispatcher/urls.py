from django.conf.urls import url

from dispatcher.views import submit_mission_view, get_inputs_view

app_name = 'dispatcher'

urlpatterns = [
    url(r'^submit_mission/$', submit_mission_view, name='submit_mission'),
    url(r'^get_inputs/(?P<parameter>\d+)/$', get_inputs_view, name='get_inputs')
]
