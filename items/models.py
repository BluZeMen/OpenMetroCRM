from datetime import timedelta
from django.db import models
from django.utils.translation import ugettext as _

from site_app.models import ModelTimestampMixin
from personnel.models import Job, Contractor


class MeasuringInstrumentKind(ModelTimestampMixin, models.Model):
    """
    Instrument kind
    """

    class Meta:
        verbose_name = _('Measuring instrument kind')
        verbose_name_plural = _('Measuring instruments kinds')

    name = models.CharField(_('name'), max_length=64)
    description = models.TextField(_('description'), blank=True, null=True)

    def __str__(self):
        return self.name


class MeasuringInstrumentType(ModelTimestampMixin, models.Model):
    """
    Instrument type
    """

    class Meta:
        verbose_name = _('Measuring instrument type')
        verbose_name_plural = _('Measuring instruments types')

    kind = models.ForeignKey(MeasuringInstrumentKind, related_name='kinds', verbose_name=_('kind'))
    name = models.CharField(_('type name'), max_length=16)
    accuracy_class = models.CharField(_('accuracy class'), max_length=16, blank=True, null=True)
    measurement_limits = models.CharField(_('measurement limits'), max_length=64, blank=True, null=True)
    suppliers = models.ManyToManyField(Contractor, blank=True, verbose_name=_('supplier'), related_name='suppliers')
    check_periodicity = models.IntegerField(_('check periodicity'), default=12)
    checking_organization = models.ForeignKey(Contractor, verbose_name=_('checking organization'), blank=True,
                                              null=True)
    description = models.TextField(_('description'), blank=True, null=True)

    def __str__(self):
        return str(self.kind) + ' ' + self.name


class MeasuringInstrument(ModelTimestampMixin, models.Model):
    """
    Instrument item
    """

    class Meta:
        verbose_name = _('Measuring instrument')
        verbose_name_plural = _('Measuring instruments')

    CHOOSE_INSTRUMENT_STATE = (
        ('un', _('Undefined')),
        ('ok', _('Okay')),
        ('rp', _('In repair')),
        ('rv', _('Reserved')),
        ('cs', _('Conserved')),
        ('wt', _('Expected delivery')),
        ('rm', _('Prepares to write-off')),
    )

    #  Translators: This message appears on the home page only
    type = models.ForeignKey(MeasuringInstrumentType, verbose_name=_('type name'), blank=True, null=True)
    serial = models.CharField(_('serial'), max_length=64, blank=True, null=True)
    inventory_number = models.IntegerField(_('inventory number'), blank=True, null=True)
    state = models.CharField(_('state'), max_length=2, choices=CHOOSE_INSTRUMENT_STATE, default='un')
    last_check_date = models.DateField(_('last check date'), blank=True, null=True)
    next_check_date = models.DateField(_('next check date'), blank=True, null=True)
    last_repair_date = models.DateField(_('last repair date'), blank=True, null=True)
    repair_description = models.TextField(_('repair description'), blank=True, null=True)

    # add some props more...

    holder = models.ForeignKey(Job, verbose_name=_('holder'), blank=True, null=True)
    description = models.TextField(_('description'), blank=True, null=True)

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
            return _('Undefined instrument')