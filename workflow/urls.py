from django.conf.urls import url

from workflow.views import processor_rest, workflow_rest, mission_rest, processor_category_delete, processor_category_rest, sql_rest, document_rest

app_name = 'workflow'

urlpatterns = [
    url(r'^workflow/$', workflow_rest, name='workflow'),
    url(r'^processor/(.+)/$', processor_rest, name='processor'),
    url(r'^mission/(.+)/$', mission_rest, name='mission'),
    url(r'^category/(.+)/$', processor_category_rest, name='category'),
    url(r'^category_delete/$', processor_category_delete, name='category'),
    url(r'^sql/(.+)/$', sql_rest, name='sql'),
    url(r'^documents/(.+)/$', document_rest, name='document'),
]
