from django.conf.urls import url
from .views import Task

task_get = Task.as_view({'get': 'get'})
task_getPending = Task.as_view({'get': 'get_pending'})
task_getComplete = Task.as_view({'get': 'get_complete'})
task_getTaskWeek = Task.as_view({'get': 'get_last_wek'})
task_update = Task.as_view({'put': 'put'})
task_create = Task.as_view({'post': 'post'})
task_delete = Task.as_view({'delete': 'delete'})
task_finalize = Task.as_view({'put': 'finalize'})
task_stop = Task.as_view({'put': 'stop'})

urlpatterns = [
    url(r'^getTask$', task_get),
    url(r'^getTask/(?P<pk>[0-9]+)$', task_get),
    url(r'^getPending', task_getPending),
    url(r'^getComplete', task_getComplete),
    url(r'^getHistoryWeek', task_getTaskWeek),
    url(r'^createTask$', task_create),
    url(r'^removeTask$', task_delete),
    url(r'^updateTask$', task_update),
    url(r'^finalizeTask$', task_finalize),
    url(r'^stopTask$', task_stop),
]