from django.conf.urls import url

from .views import list_posts
from .views import view_post
from .views import create_post
from .views import edit_post

urlpatterns = [
    url(r'^posts/$', list_posts, name='list_post'),
    url(r'^posts/(?P<pk>[0-9]+)/$', view_post, name='view_post'),
    url(r'^posts/create/$', create_post, name='create_post'),
    url(r'^posts/(?P<pk>[0-9]+)/edit/$', edit_post, name='edit_post'),
]
