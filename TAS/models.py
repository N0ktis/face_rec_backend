import os
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


def path_and_rename(instance, filename):
    try:
        instance.event_type
        return save_checkpoint(instance, filename)
    except:
        return save_avatar(instance, filename)


def save_avatar(instance, filename):
    upload_to = 'photos'
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(instance.pk, ext)
    return os.path.join(upload_to, filename)


def save_checkpoint(instance, filename):
    if instance.event_type in ('S_ENTR', 'F_ENTR'):
        upload_to = 'entrance'
    else:
        upload_to = 'exit'
    ext = filename.split('.')[-1]
    filename = '{}_{}_{}.{}'.format(instance.event_type, instance.event_time, instance.device_id, ext)
    return os.path.join(upload_to, filename)


class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=100)
    document_id = models.CharField(max_length=10, unique=True)
    pernr = models.CharField(max_length=10, unique=True)
    position = models.CharField(max_length=100)
    boss = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, blank=True)
    is_boss = models.BooleanField(default=False)
    birth_date = models.DateField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    email = models.EmailField(unique=True)
    user_phone_num = models.CharField(max_length=15, null=True, blank=True)
    avatar = models.ImageField(upload_to=path_and_rename, default='default_avatar.svg')
    at_workplace = models.BooleanField(default=False)
    avatar_encodings = models.JSONField(default=dict)
    about = models.TextField(max_length=256, blank=True, default='')
    work_time_30days = models.FloatField(default=0)
    work_time_7days = models.FloatField(default=0)
    work_time_1days = models.FloatField(default=0)
    is_on_holiday = models.BooleanField(default=False)
    is_sick = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['-updated', '-full_name']

    def __str__(self):
        return str(self.email)


class Department(models.Model):
    department_name = models.CharField(max_length=100, unique=True)
    department_head = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.CharField(max_length=100)
    max_users = models.PositiveIntegerField(default=0)
    staff = models.JSONField(null=True)

    def __str__(self):
        return str(self.department_name)


class Device(models.Model):
    class LocationSubType(models.TextChoices):
        entrance = 'ENTR'
        exit = 'EXIT'

    device_id = models.CharField(primary_key=True, max_length=64)
    location = models.CharField(max_length=100)
    location_sub_type = models.CharField(max_length=4, choices=LocationSubType.choices)
    is_active = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(default='127.0.0.1')
    connected_dev = models.JSONField(default=dict)

    def __str__(self):
        return self.device_id


class TimeTracking(models.Model):
    class EventType(models.TextChoices):
        success_entrance = 'S_ENTR'
        success_exit = 'S_EXIT'
        failed_entrance = 'F_ENTR'
        failed_exit = 'F_EXIT'

    user_id = models.ForeignKey(User, null=True,blank=True, on_delete=models.DO_NOTHING)
    device_id = models.ForeignKey(Device, on_delete=models.DO_NOTHING)
    event_time = models.DateTimeField(auto_now=True)
    event_date = models.DateField(auto_now=True)
    event_photo = models.ImageField(upload_to=path_and_rename)  # upload_to=static(settings.MEDIA_ROOT / 'entrance')
    event_type = models.CharField(max_length=6, choices=EventType.choices)
    event_photo_encodings = models.JSONField(default=dict)

    def __str__(self):
        return '{}_{}_{}'.format(self.event_type, self.event_time, self.device_id)
