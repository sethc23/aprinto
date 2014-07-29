from django.conf.urls import patterns, url
import load
# import maintenance

urlpatterns = patterns('',
    url(r'^load_new_user/$', load.new_user, name='load_new_user'),
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
