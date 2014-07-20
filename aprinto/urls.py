from django.conf.urls import patterns, include, url

# from django.contrib import admin
# admin.autodiscover()

from pdf.views import doc_upload, doc_list,doc_detail

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'aprinto.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # Default login url
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),

    # url(r'^admin/', include(admin.site.urls)),

    # url(r'^docs/', include('pdf.urls')),
    url(r'^$', doc_upload, name='pdf_upload'),
    url(r'^docs/$', doc_list, name='pdf_list'),
    url(r'^(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', doc_detail, name='pdf_detail'),
    # url(r'^list/', doc_list, name='pdf_list'),
)
