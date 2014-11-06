from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('backend.views',
    url(r'^$', 'index'),
    url(r'^login$', 'login'),
    url(r'^logout$', 'logout'),
    url(r'^send$', 'send_package')
)

urlpatterns = urlpatterns + patterns('backend.fetch_views',
    url(r'^fetch$', 'fetch')
)

urlpatterns = urlpatterns + patterns('backend.user_views',
    url(r'^user$', 'user'),
    url(r'^user/(?P<id>\d+)$', 'edit_user'),
    url(r'^user/delete$', 'delete_user'),
    url(r'^user/requireName$', 'requireName')
)

'''
urlpatterns = urlpatterns + patterns('backend.dishes_views',
    url(r'^dishes$', 'dishes'),
    url(r'^dishes/(?P<id>\d+)$', 'edit_dishes'),
    url(r'^dishes/add$', 'add_dishes'),
    url(r'^dishes/delete$', 'delete_dishes')
)

urlpatterns = urlpatterns + patterns('backend.preorder_views',
    url(r'^preorder$', 'preorder'),
    url(r'^preorder/delete$', 'delete_preorder'),
    url(r'^preorder/complete$', 'complete_preorder')
)

urlpatterns = urlpatterns + patterns('backend.user_views',
    url(r'^user$', 'user')
)
'''
