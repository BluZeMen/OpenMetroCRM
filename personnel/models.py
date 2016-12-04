""" Models module
"""
import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

from site_app.models import ModelTimestampMixin


class Location(ModelTimestampMixin, models.Model):
    """Location"""

    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')

    name = models.CharField(_('name'), max_length=256)
    description = models.TextField(_('description'), blank=True, null=True)

    def __str__(self):
        return self.name


class Contact(AbstractUser, ModelTimestampMixin, models.Model):
    """Contact"""

    class Meta:
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')

    patronymic = models.CharField(_('patronymic'), max_length=32, blank=True, null=True)
    GENDER_CHOICES = (
        (True, _('Male')),
        (False, _('Female')),
        (None, _('Undefined')),
    )
    gender = models.NullBooleanField(_('gender'), blank=True, null=True)
    mobile_phone = models.CharField(_('mobile phone'), max_length=14, blank=True, null=True)
    home_phone = models.CharField(_('home phone'), max_length=14, blank=True, null=True)
    home_location = models.ForeignKey(Location, verbose_name=_('home location'), blank=True, null=True)
    birthday = models.DateField(_('birthday'), blank=True, null=True)

    @property
    def age(self):
        """User age"""
        if not self.birthday:
            return False
        else:
            today = datetime.date.today()
            # Raised when birth date is February 29 and the current year is not a
            # leap year.
            try:
                birthday = self.birthday.replace(year=today.year)
            except ValueError:
                day = today.day - 1 if today.day != 1 else today.day + 2
                birthday = self.birthday.replace(year=today.year, day=day)
            if birthday > today:
                return today.year - self.birthday.year - 1
            else:
                return today.year - self.birthday.year

    @property
    def appeal(self):
        """Short appeal to contact"""
        if self.first_name and self.patronymic:
            return self.first_name + ' ' + self.patronymic
        return self.username

    @property
    def appeal_full(self):
        """Long appeal to contact"""
        return self.first_name + ' ' + self.patronymic + ((' ' + self.last_name) if self.last_name else '')

    @property
    def short_presentation(self):
        """Short presentation: last name with initials"""
        if self.first_name and self.last_name and self.patronymic:
            return self.last_name + ' ' + self.first_name[:1].upper() + '.' + self.patronymic[:1].upper() + '.'
        return self.username

    def __str__(self):
        return self.appeal


class ContractorType(ModelTimestampMixin, models.Model):
    """Contractor type"""

    class Meta:
        verbose_name = _('Contractor type')
        verbose_name_plural = _('Contractor types')

    name = models.CharField(_('name'), max_length=256)
    description = models.TextField(_('description'), blank=True, null=True)

    def __str__(self):
        return self.name


class Contractor(ModelTimestampMixin, models.Model):
    """Contractor"""

    class Meta:
        verbose_name = _('Contractor')
        verbose_name_plural = _('Contractors')

    name = models.CharField(_('name'), max_length=64)
    full_name = models.CharField(_('full name'), max_length=256, blank=True, null=True)
    type = models.ForeignKey(ContractorType, verbose_name=_('type'), blank=True, null=True)
    description = models.TextField(_('description'), blank=True, null=True)
    location = models.ForeignKey(Location, verbose_name=_('location'), blank=True, null=True)

    def __str__(self):
        return self.name + ' [' + str(self.type) + ']'


class JobType(ModelTimestampMixin, models.Model):
    """Job position type"""

    class Meta:
        verbose_name = _('Job type')
        verbose_name_plural = _('Job types')

    name = models.CharField(_('name'), max_length=256)
    description = models.TextField(_('description'), blank=True, null=True)

    def __str__(self):
        return self.name


class Job(ModelTimestampMixin, models.Model):
    """Job position"""

    class Meta:
        verbose_name = _('Job')
        verbose_name_plural = _('Jobs')

    name = models.CharField(_('name'), max_length=256)
    type = models.ForeignKey(JobType, verbose_name=_('type'), blank=True, null=True)
    holder = models.ForeignKey('Contact', verbose_name=_('holder'), blank=True, null=True)
    contractor = models.ForeignKey(Contractor, verbose_name=_('contractor'), blank=True, null=True)
    location = models.ForeignKey(Location, verbose_name=_('location'), blank=True, null=True)
    description = models.TextField(_('description'), blank=True, null=True)

    def __str__(self):
        return self.name + ' [' + str(self.type) + ']'


class InventoryNumber(ModelTimestampMixin, models.Model):
    """Inventory number"""

    class Meta:
        verbose_name = _('Inventory number')
        verbose_name_plural = _('Inventory numbers')

    number = models.IntegerField(_('number'))
    holder = models.ForeignKey('Contact', verbose_name=_('holder'), blank=True, null=True)

    def __str__(self):
        return self.number + ' [' + str(self.holder) + ']'
