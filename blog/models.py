from django.db import models
from django.conf import settings
from django.dispatch import receiver


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey('Category')
    image = models.ImageField(
        upload_to='%Y/%m/%d/', null=True, blank=True
    )
    tags = models.ManyToManyField('Tag', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '<Post {}: "{}">'.format(self.pk, self.title[:8])

    def get_absolute_url(self):
        return '/posts/{}/'.format(self.pk)

    @receiver(post_delete, sender=Post)
    def delete_attached_image(sender, **kwargs):
        instance = kwargs.pop('instance')
        instance.image.delete(save=False)


class Category(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '<Category {}: "{}">'.format(self.pk, self.name)


class Comment(models.Model):
    post = models.ForeignKey(Post)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '<Comment {}>'.format(self.pk)


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '<Tag {}: "{}">'.format(self.pk, self.name)
