from django.conf.urls import url

from dispatcher.views import submit_mission_view

app_name = 'dispatcher'

urlpatterns = [
    url(r'^submit_mission/$', submit_mission_view, name='submit_mission'),
]
