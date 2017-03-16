""" Models module
"""

from django.conf import settings
from django.db import models

from site_app.models import ModelTimestampMixin


class DialogManager(models.Manager):
    def personal(self, participant):
        return self.filter(participants__in=[participant])

class Dialog(ModelTimestampMixin, models.Model):
    """Dialog"""

    class Meta:
        verbose_name = 'Диалог'
        verbose_name_plural = 'Диалоги'

    objects = DialogManager()

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='creator')
    name = models.CharField('Название', max_length=150, blank=True, null=True)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='Участники', blank=True)

    def get_last_messages(self, count=100):
        return Message.objects.filter(dialog_id=self.id).order_by('-created_datetime')[:count]

    def get_unread_messages_count(self):
        return Message.objects.filter(dialog_id=self.id, is_read=False).count()

    def get_last_message(self):
        messages = self.get_last_messages(1)
        if len(messages) > 0:
            return messages[0]
        return None

    def __str__(self):
        return self.name


class Message(ModelTimestampMixin, models.Model):
    """Message"""

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Отправитель')
    dialog = models.ForeignKey(Dialog, verbose_name='Дилог')
    text = models.TextField('Текст', blank=True, null=True)
    is_read = models.BooleanField('Прочитано', default=False)

    def __str__(self):
        return self.text
