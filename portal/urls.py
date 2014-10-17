from django.conf.urls import patterns, include, url

urlpatterns = patterns('portal.views',
    url(r'^$', 'index'),
    url(r'^login$', 'login'),
    url(r'^logout$', 'logout'),
    url(r'^sign$', 'sign'),
    url(r'^recent$', 'recent'),
    url(r'^send$', 'send'),
    url(r'^send/add$', 'addSendOrder'),
    url(r'^store$', 'store'),
    url(r'^store/item$', 'storeItem'),
    url(r'^store/order$','doOrder'),
    url(r'^profile$', 'profile'),
    url(r'^rule$', 'rule')
)
