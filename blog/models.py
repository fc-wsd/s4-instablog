from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey('Category')
    tags = models.ManyToManyField('Tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '<Post {}: "{}">'.format(self.pk, self.title[:8])


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
