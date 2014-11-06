from django.conf.urls import patterns, include, url

urlpatterns = patterns('mgr.views',
    url(r'^sign/fetch$', 'signOrdersToFetch'),
    url(r'^sign/delivery$', 'signOrdersToDelivery'),
    url(r'^send/fetch$', 'sendOrdersToFetch'),
    url(r'^send/delivery$', 'sendOrdersToDelivery'),

    url(r'api/send/receive', 'receiveSendOrder'),
    url(r'api/send/complete', 'completeSendOrder'),
    url(r'api/sign/receive', 'receiveSignOrder'),
    url(r'api/sign/refuse', 'refuseSignOrder'),
    url(r'api/sign/complete', 'completeSignOrder'),
    url(r'logout', 'logout')
)
