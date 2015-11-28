from django.db import models
from django.conf import settings


class Profile(models.Model):
    GENDER_CHOICES = (
        ('m', 'Male', ),
        ('f', 'Female', ),
        ('u', 'Unknown', ),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
