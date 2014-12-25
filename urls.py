import views
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<forum_id>\d+)/$', views.forum, name='forum'),
    url(r'^(?P<topic_id>\d+)/(?P<subject>.*)/$', views.topic, name='topic'),
)