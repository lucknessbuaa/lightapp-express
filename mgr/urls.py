from django.conf.urls import patterns, include, url

urlpatterns = patterns('mgr.views',
    url(r'^sign/fetch$', 'signOrdersToFetch'),
    url(r'^sign/delivery$', 'signOrdersToDelivery'),
    url(r'^send/fetch$', 'sendOrdersToFetch'),
    url(r'^send/delivery$', 'sendordersToDelivery')
)
