from django.contrib import admin
from django.contrib.admin import register

from .models import MeasuringInstrumentKind, MeasuringInstrumentType, MeasuringInstrument


@register(MeasuringInstrumentKind)
class MeasuringInstrumentKindAdmin(admin.ModelAdmin):
    pass


@register(MeasuringInstrumentType)
class MeasuringInstrumentTypeAdmin(admin.ModelAdmin):
    pass


@register(MeasuringInstrument)
class MeasuringInstrumentAdmin(admin.ModelAdmin):
    pass
