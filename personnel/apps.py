from django.apps import AppConfig

from django.utils.translation import ugettext_lazy as _


class PersonnelConfig(AppConfig):
    """App "Personnel" config"""
    name = 'personnel'
    verbose_name = 'Персонал'
