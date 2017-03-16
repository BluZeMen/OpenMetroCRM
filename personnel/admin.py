"""Admin module

This module used for registerating models in the Django admin.

"""

from django.contrib import admin
from django.contrib.admin import register

from .models import Contact, Contractor, ContractorType, Job, JobType, Location, InventoryNumber


@register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    Contact admin entity
    """
    list_display = ('appeal', 'mobile_phone', 'home_location')
    search_fields = ('first_name', 'last_name', 'patronymic')


@register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
    pass


@register(ContractorType)
class ContractorTypeAdmin(admin.ModelAdmin):
    pass


@register(Job)
class JobAdmin(admin.ModelAdmin):
    pass


@register(JobType)
class JobTypeAdmin(admin.ModelAdmin):
    pass


@register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass


@register(InventoryNumber)
class InventoryNumberAdmin(admin.ModelAdmin):
    pass
