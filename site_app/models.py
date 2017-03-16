from django.db import models
from django.utils.translation import ugettext_lazy as _


class ModelTimestampMixin(models.Model):
    modified_datetime = models.DateTimeField('Изменено', auto_now=True, editable=False,
                                             help_text='Дата и время последнего изменения записи'
                                             )
    created_datetime = models.DateTimeField('Создано', auto_now_add=True, editable=False,
                                            help_text='Дата и время создания записи'
                                            )

    class Meta:
        abstract = True
