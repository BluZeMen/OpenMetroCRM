from django.apps import AppConfig

from django.utils.translation import ugettext_lazy as _


class ItemsConfig(AppConfig):
    """App "Items" config"""
    name = 'items'
    verbose_name = 'Инвентарь'
