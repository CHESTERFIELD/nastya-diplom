from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager
from diplom import settings


class CustomUser(AbstractUser):
    first_name = None
    last_name = None
    email = None
    username = models.CharField(_('username'), unique=True, max_length=100)
    password = models.CharField(max_length=100)
    fio = models.CharField(max_length=255)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class UserPhoto(models.Model):
    user_photo = models.ImageField(upload_to='uploads', width_field="img_width", height_field="img_height")
    img_width = models.PositiveIntegerField(null=True, default=640)
    img_height = models.PositiveIntegerField(null=True, default=480)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.user.fio


class RecognizedObject(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_datetime = models.DateTimeField(default=timezone.now)
    img_width = models.PositiveIntegerField(null=True, default=640)
    img_height = models.PositiveIntegerField(null=True, default=480)
    user_photo = models.ImageField(upload_to='uploads/recognitation_faces', null=True, blank=True,
                                   width_field="img_width", height_field="img_height")

    def __str__(self):
        return "%s" % self.created_datetime
