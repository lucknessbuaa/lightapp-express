from django.conf.urls import patterns, include, url

urlpatterns = patterns('portal.views',
    url(r'^$', 'index'),
    url(r'^login$', 'login')
)
