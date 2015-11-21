from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^posts/$', views.list_posts, name='list_posts'),
    url(r'^posts/create/$', views.create_post, name='create_post'),
    url(r'^posts/(?P<pk>[0-9]+)/$', views.view_post, name='view_post'),
]
