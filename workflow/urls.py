from django.conf.urls import url

from workflow.views import processor_rest, workflow_rest

app_name = 'workflow'

urlpatterns = [
    url('^workflow/$', workflow_rest, name='workflow'),
    url('^processor/$', processor_rest, name='processor'),
]
