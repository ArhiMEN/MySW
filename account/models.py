from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from .manager import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to='avatar/', null=True, blank=True)
    friends = models.ManyToManyField('CustomUser', symmetrical=False)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    middle_name = models.CharField(max_length=15)
    sex = models.CharField(max_length=7)
    birthday = models.DateField('birthday')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def dict(self):
        return {'id': self.id,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'middle_name': self.middle_name,
                'birthday': self.birthday,
                'sex': self.sex, }

    def get_full_name(self):
        return self.last_name + " " + self.first_name + " " + self.middle_name

    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url


class Message(models.Model):
    sender = models.ForeignKey(CustomUser, related_name="user_sender", on_delete=models.CASCADE)
    recipient = models.ForeignKey(CustomUser, related_name="user_recipient", on_delete=models.CASCADE)
    message_date = models.DateTimeField(auto_now_add=True)
    text_message = models.TextField(max_length=200)

    def __str__(self):
        return self.text_message

    def get_sender_name(self):
        sender = CustomUser.objects.get(pk=self.sender.id)
        return sender.first_name

    def get_recipient_name(self):
        recipient = CustomUser.objects.get(pk=self.recipient.id)
        return recipient.first_name

    def dict(self):
        return {
            'sender_id': self.sender.id,
            'recipient_id': self.recipient.id,
            'date': self.message_date,
            'text': self.text_message,
        }


class Wall(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=30)
    text_message = models.TextField(max_length=200)

    def __str__(self):
        return self.text_message

    def dict(self):
        return {
            'name': self.sender.get_full_name(),
            'date': self.message_date,
            'title': self.title,
            'text': self.text_message
        }


class File(models.Model):
    name = models.CharField(max_length=30)
    file = models.FileField(upload_to='files/')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_image = models.BooleanField()
    content_type = models.CharField(max_length=100, blank=True)

    @property
    def file_url(self):
        if self.file and hasattr(self.file, 'url'):
            return self.file.url

    @property
    def pure_name(self):
        name = str(self.file).split("/")[-1]
        return name

    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.file_url,
            'pure_name': self.pure_name,
            'is_image': self.is_image,
        }
