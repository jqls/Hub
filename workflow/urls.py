from django.conf.urls import url

from workflow.views import processor_rest, workflow_rest

app_name = 'workflow'

urlpatterns = [
    url(r'^workflow/$', workflow_rest, name='workflow'),
    url(r'^processor/$', processor_rest, name='processor'),
]
