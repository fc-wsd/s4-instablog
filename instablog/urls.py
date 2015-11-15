from django.conf.urls import include, url
from django.contrib import admin

from blog.urls import urlpatterns as blog_urls

urlpatterns = [
    url(r'^blog/', include(blog_urls, namespace='blog')),
    url(r'^admin/', include(admin.site.urls)),
]
