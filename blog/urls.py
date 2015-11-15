from django.conf.urls import url

from .views import list_posts

urlpatterns = [
    url(r'^posts/$', list_posts),
]

# blog 앱 디렉터리의 urls.py
