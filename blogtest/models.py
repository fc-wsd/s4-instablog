from django.db import models
from django.conf import settings


class Post(models.Model):
    """게시물 정보를 담는 모델. 필요한 모델 필드를 추가하세요.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='testpost_user'
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class Comment(models.Model):
    """댓글 모델. 필요한 모델 필드를 추가하세요.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='testcomment_user'
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class Category(models.Model):
    """글 갈래 모델. 필요한 모델 필드를 추가하세요.
    """
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
