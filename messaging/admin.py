"""Admin module

This module used for registerating models in the Django admin.

"""

from django.contrib import admin
from django.contrib.admin import register

from .models import Dialog, Message


@register(Dialog)
class DialogAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_datetime')


@register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('created_datetime', 'sender', 'dialog', 'is_read')
