# Common utils
from django.db import models
from django.db.models import Func


def get_fields_names(model, editable_only=True):
    if editable_only:
        return [field.name for field in model._meta.get_fields() if field.editable]
    return [field.name for field in model._meta.get_fields()]


def get_choices_from_model_editable(model):
    return [(field.name, field.verbose_name) for field in model._meta.get_fields() if field.editable]


class Month(Func):
    function = 'EXTRACT'
    template = '%(function)s(MONTH from %(expressions)s)'
    output_field = models.IntegerField()
