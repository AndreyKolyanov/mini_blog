# coding:utf-8
from django.db import models
from account.models import User


class Record(models.Model):
    text = models.CharField(max_length=255, verbose_name=u'Текст записи')
    author = models.ForeignKey(User)
    date = models.DateTimeField()

    def __unicode__(self):
        return self.author.get_username() + ' ' + str(self.date)

    class Meta:
        ordering = ['-date']
