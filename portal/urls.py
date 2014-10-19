from django.conf.urls import patterns, include, url

urlpatterns = patterns('portal.views',
    url(r'^$', 'index'),
    url(r'^login$', 'login'),
    url(r'^logout$', 'logout'),
    url(r'^sign$', 'sign'),
    url(r'^points$', 'points'),
    url(r'^recent$', 'recent'),
    url(r'^recent/delete$', 'deleteRecent'),
    url(r'^send$', 'send'),
    url(r'^send/add$', 'addSendOrder'),
    url(r'^store$', 'store'),
    url(r'^store/item$', 'storeItem'),
    url(r'^store/order$','doOrder'),
    url(r'^store/myOrder$','getOrder'),
    url(r'^profile$', 'profile'),
    url(r'^error$', 'error'),
    url(r'^price$', 'price'),
    #url(r'^test$', 'test'),
    url(r'^rule$', 'rule')
)
