#coding:utf-8

from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFit, Adjust,ResizeToFill
from django.utils.timezone import now


class User(AbstractUser):

    subscribe_to = models.ManyToManyField('self', symmetrical=False)
    date_of_birth = models.DateField(u'Дата рождения', null=True, blank=True, default=now)
    phone = models.CharField(max_length=15, verbose_name=u'Телефон', null=True, blank=True)
    about = models.TextField(max_length=255, verbose_name=u'О себе', null=True, blank=True)
    photo = models.ImageField(verbose_name=u'Фото',upload_to='images/',max_length=256, default='images/no_photo.png',
                              blank=True, null=True)

    photo_micro = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1),
            ResizeToFill(50, 50)], source='photo',
            format='JPEG', options={'quality': 90})

    photo_small = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1),
            ResizeToFill(100, 100)], source='photo',
            format='JPEG', options={'quality': 90})

    photo_medium = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1),
            ResizeToFit(300, 200)], source='photo',
            format='JPEG', options={'quality': 90})

    def __unicode__(self):
        return self.get_full_name() + ' (' + self.username + ')'
