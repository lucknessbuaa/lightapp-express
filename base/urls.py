from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.shortcuts import redirect


def index(request):
    return redirect('/app')
    

urlpatterns = patterns('',
    url(r'^$', index),
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^oauth/', include('social_auth.urls')),
    url(r'^app/', include('portal.urls'))
)

handler404 = 'portal.views.error'
handler403 = 'portal.views.error'
handler400 = 'portal.views.error'
handler500 = 'portal.views.error'
