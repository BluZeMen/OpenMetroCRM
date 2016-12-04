from django.db import models
from django.utils.translation import ugettext_lazy as _


class ModelTimestampMixin(models.Model):
    last_change_date = models.DateTimeField(_('last change date'), auto_now=True, blank=True, null=True)
    created_date = models.DateTimeField(_('entry date'), auto_created=True, blank=True, null=True)

    class Meta:
        abstract = True
