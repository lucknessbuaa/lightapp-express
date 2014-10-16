from django.conf.urls import patterns, include, url

urlpatterns = patterns('portal.views',
    url(r'^$', 'index'),
    url(r'^login$', 'login'),
    url(r'^logout$', 'logout'),
    url(r'^sign$', 'sign'),
    url(r'^send$', 'send'),
    url(r'^store$', 'store'),
    url(r'^profile$', 'profile')
)
