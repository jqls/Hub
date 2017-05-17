from django.conf.urls import url
from views import Mission_list, Mission_detail, Mission_detail_v2

app_name = 'restapi'

urlpatterns = [
    url(r'^missions/$', Mission_list),
    url(r'^missions/(?P<id>[0-9]+)/$', Mission_detail),
    url(r'^missions/(?P<id1>[0-9]+)/(?P<id2>[0-9]+)/$', Mission_detail_v2),
]