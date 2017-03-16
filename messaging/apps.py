from django.apps import AppConfig

from django.utils.translation import ugettext_lazy as _


class MessagingConfig(AppConfig):
    name = 'messaging'
    verbose_name = 'Обмен сообщениями'
