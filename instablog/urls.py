from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login as django_login
from django.contrib.auth.views import logout as django_logout

from blog.urls import urlpatterns as blog_urls

urlpatterns = [
    url(r'^blog/', include(blog_urls, namespace='blog')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blogtest/', include('blogtest.urls', namespace='blogtest')),
    url(
        r'^login/$', django_login,
        {'template_name': 'login.html'}, name='login_url'
    ),
    url(
        r'^logout/$', django_logout,
        {'next_page': '/login/'}, name='logout_url'
    ),
]
