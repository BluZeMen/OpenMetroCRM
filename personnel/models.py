""" Models module
"""
import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from site_app.models import ModelTimestampMixin


class Location(ModelTimestampMixin, models.Model):
    """Location"""

    class Meta:
        verbose_name = 'Местоположение'
        verbose_name_plural = 'Местоположения'

    name = models.CharField('Название', max_length=256)
    description = models.TextField('Описание', blank=True, null=True)

    def __str__(self):
        return self.name


class Contact(AbstractUser, ModelTimestampMixin, models.Model):
    """Contact"""

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    patronymic = models.CharField('Отчество', max_length=32, blank=True, null=True)
    GENDER_CHOICES = (
        (True, 'М'),
        (False, 'Ж'),
        (None, 'Не указано'),
    )
    gender = models.NullBooleanField('Пол', blank=True, null=True)
    mobile_phone = models.CharField('Моб. теефон', max_length=14, blank=True, null=True)
    home_phone = models.CharField('Домашний телефон', max_length=14, blank=True, null=True)
    home_location = models.ForeignKey(Location, verbose_name='Место жительства', blank=True, null=True)
    birthday = models.DateField('Дата рождения', blank=True, null=True)
    avatar = models.ImageField('Аватар', upload_to='avatars', blank=True, null=True)

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
        verbose_name = 'Тип контрагента'
        verbose_name_plural = 'Типы контрагентов'

    name = models.CharField('Название', max_length=256)
    description = models.TextField('Описание', blank=True, null=True)

    def __str__(self):
        return self.name


class Contractor(ModelTimestampMixin, models.Model):
    """Contractor"""

    class Meta:
        verbose_name = 'Контрагент'
        verbose_name_plural = 'Контрагенты'

    name = models.CharField('Имя', max_length=64)
    full_name = models.CharField('Полное имя', max_length=256, blank=True, null=True)
    type = models.ForeignKey(ContractorType, verbose_name='Тип', blank=True, null=True)
    description = models.TextField('description', blank=True, null=True)
    location = models.ForeignKey(Location, verbose_name='Местоположение', blank=True, null=True)

    def __str__(self):
        s = self.name
        if self.type:
            s += ' [' + str(self.type) + ']'
        elif self.location:
            s += ' [' + str(self.location) + ']'
        return s


class JobType(ModelTimestampMixin, models.Model):
    """Job position type"""

    class Meta:
        verbose_name = 'Тип должности'
        verbose_name_plural = 'Типы должностей'

    name = models.CharField('Название', max_length=256)
    description = models.TextField('Описание', blank=True, null=True)

    def __str__(self):
        return self.name


class Job(ModelTimestampMixin, models.Model):
    """Job position"""

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    name = models.CharField('Название', max_length=256)
    type = models.ForeignKey(JobType, verbose_name='Тип', blank=True, null=True)
    holder = models.ForeignKey('Contact', verbose_name='Держатель', blank=True, null=True)
    contractor = models.ForeignKey(Contractor, verbose_name='Контрагент', blank=True, null=True)
    location = models.ForeignKey(Location, verbose_name='Местоположение', blank=True, null=True)
    description = models.TextField('Описание', blank=True, null=True)

    def __str__(self):
        return self.name + ' [' + str(self.type) + ']'


class InventoryNumber(ModelTimestampMixin, models.Model):
    """Inventory number"""

    class Meta:
        verbose_name = 'Инвентарный номер'
        verbose_name_plural = 'Инвентарные номера'

    number = models.IntegerField('Номер')
    holder = models.ForeignKey('Contact', verbose_name='Держатель', blank=True, null=True)

    def __str__(self):
        return self.number + ' [' + str(self.holder) + ']'
