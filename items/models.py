import calendar
from datetime import timedelta, datetime, date

from django.db import models
from django.db.models import Count
from django.urls import reverse_lazy
from django.utils.timezone import get_current_timezone

from site_app.models import ModelTimestampMixin
from site_app.utils import Month
from personnel.models import Job, Contractor



class MeasuringInstrumentKind(ModelTimestampMixin, models.Model):
    """
    Instrument kind
    """

    class Meta:
        verbose_name = 'Вид измерительного прибора'
        verbose_name_plural = 'Виды измерительных приборов'

    name = models.CharField('Название', max_length=64)
    description = models.TextField('Описание', blank=True, null=True)

    def __str__(self):
        return self.name


class MeasuringInstrumentType(ModelTimestampMixin, models.Model):
    """
    Instrument type
    """

    class Meta:
        verbose_name = 'Тип измерительного прибора'
        verbose_name_plural = 'Типы измерительных приборов'

    kind = models.ForeignKey(MeasuringInstrumentKind, related_name='kinds', verbose_name='Вид')
    name = models.CharField('Название', max_length=16)
    accuracy_class = models.CharField('Класс точности', max_length=16, blank=True, null=True)
    measurement_limits = models.CharField('Пределы измерений', max_length=64, blank=True, null=True)
    suppliers = models.ManyToManyField(Contractor, blank=True, verbose_name='Поставщики', related_name='suppliers')
    check_periodicity = models.DurationField('Периодичность проверки', default=timedelta(days=365))
    checking_organization = models.ForeignKey(Contractor, verbose_name='Проверяющая организация', blank=True,
                                              null=True)
    description = models.TextField('Описание', blank=True, null=True)

    def __str__(self):
        return str(self.kind) + ' ' + self.name


class MeasuringInstrumentManager(models.Manager):
    DEFAULT_LOOKUP_PERIOD_DAYS = 45

    def annotate_next_check_date(self, queryset=None):
        if queryset == None:
            queryset = self  # dirty strange naming
        next_check_date = models.F('last_check_date') + models.F('type__check_periodicity')
        next_check_date.output_field = models.DateField()
        q = queryset.annotate(next_check_date=next_check_date)
        return q

    def overdue(self, start_date=None):
        if not start_date: start_date = date.today()
        return self.with_next_check_date().values('next_check_date').filter(next_check_date__lte=start_date)

    def for_checking(self, period_days=DEFAULT_LOOKUP_PERIOD_DAYS, period_start=None):
        period_start = date.today() if period_start is None else period_start
        q = self.annotate_next_check_date()
        q = q.filter(next_check_date__lte=period_start + timedelta(days=period_days))
        return q

    def for_checking_stat_per_organization(self, period_days=DEFAULT_LOOKUP_PERIOD_DAYS, period_start=None):
        q = self.for_checking(period_days, period_start)
        q = q.values('type', 'type__name', 'type__kind__name', 'type__checking_organization',
                     'type__checking_organization__name').annotate(Count('type__checking_organization'))
        return q

    def checking_stat_per_organization_and_type(self, period_days=DEFAULT_LOOKUP_PERIOD_DAYS, period_start=None):
        q = self.for_checking(period_days, period_start)
        q = q.values('type', 'type__name', 'type__kind__name', 'type__checking_organization',
                     'type__checking_organization__name').annotate(Count('type__checking_organization'), Count('type'))
        return q

    def year_checking_stat_per_organization_and_month(self, period_year=None):
        """
        Returns year's statistics of checking measurement instruments by checking organizations and month's

        :param period_year: integer, year of statistics(..., 2015, 2016, etc.)

        :return: Returns
        """
        period_start = date.today().replace(month=1, day=1)
        if period_year:
            period_start = period_start.replace(year=period_year)

        days_in_year = 366 if calendar.isleap(period_start.year) else 365
        lookup_days = days_in_year

        q = self.for_checking(lookup_days, period_start)

        checking_month = Month((models.F('last_check_date') + models.F('type__check_periodicity')))
        checking_month.output_field = models.IntegerField()
        q = q.annotate(checking_month=checking_month)

        q = q.values('type', 'type__name', 'type__kind__name', 'type__checking_organization',
                     'type__checking_organization__name', 'checking_month').annotate(
            Count('checking_month'), Count('type__checking_organization')).order_by('checking_month')
        return q


class MeasuringInstrument(ModelTimestampMixin, models.Model):
    """
    Instrument item
    """

    class Meta:
        verbose_name = 'Измерительный прибор'
        verbose_name_plural = 'Измерительние приборы'

    CHOOSE_INSTRUMENT_STATE = (
        ('un', 'Неопределено'),
        ('ok', 'Исправен'),
        ('rp', 'В ремонте'),
        ('rv', 'В резерве'),
        ('cs', 'В консервации'),
        ('wt', 'Ожидается поступление'),
        ('rm', 'Ожидается списание'),
    )

    objects = MeasuringInstrumentManager()

    type = models.ForeignKey(MeasuringInstrumentType, verbose_name='Тип', blank=True, null=True)
    serial = models.CharField('Заводской номер', max_length=64, blank=True, null=True)
    inventory_number = models.IntegerField('Инвентарный номер', blank=True, null=True)
    state = models.CharField('Состояние', max_length=2, choices=CHOOSE_INSTRUMENT_STATE, default='un')
    last_check_date = models.DateField('Дата последней проверки', blank=False, null=True)
    # next_check_date = models.DateField('Дата следующей проверки', blank=False, null=True)
    last_repair_date = models.DateField('Дата последней починки', blank=True, null=True)
    repair_description = models.TextField('Описание починки', blank=True, null=True)

    # add some props more...

    holder = models.ForeignKey(Job, verbose_name='Держатель', blank=True, null=True)
    description = models.TextField('Описание', blank=True, null=True)

    def get_next_check_date(self):
        return self.last_check_date + self.type.check_periodicity

    def get_absolute_url(self):
        return reverse_lazy('items:mi', kwargs={'pk': self.id})

    def __str__(self):
        if self.type and self.serial:
            return str(self.type) + ' ' + self.serial
        elif self.serial:
            return '-*- ' + self.serial
        elif self.type:
            return str(type)
        elif self.inventory_number:
            return '#' + str(self.inventory_number)
        else:
            return 'Неопределённый прибор'
