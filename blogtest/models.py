from django.db import models


class Post(models.Model):
    """게시물 정보를 담는 모델. 필요한 모델 필드를 추가하세요.
    """


class Comment(models.Model):
    """댓글 모델. 필요한 모델 필드를 추가하세요.
    """
    post = models.ForeignKey(Post)


class Category(models.Model):
    """글 갈래 모델. 필요한 모델 필드를 추가하세요.
    """
