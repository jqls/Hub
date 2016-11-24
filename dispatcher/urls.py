from django.conf.urls import url

from . import views


app_name = 'dispatcher'


urlpatterns = [
    url(r'^post_mission/$', views.post_mission, name='post_mission'),
    url(r'^get_processor/(?P<pk>\d+)/$', views.get_processor, name='get_processor'),
]