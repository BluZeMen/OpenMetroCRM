from django import forms
import json

from site_app.utils import get_choices_from_model_editable
from .models import MeasuringInstrument
from django.utils.translation import ugettext_lazy as _

from django.core.exceptions import ValidationError

def validate_all_choices(value):
    # here have your custom logic
    pass

class ItemsEditForm(forms.Form):
    ACTION_CHOICES = (
        ('delete', 'Удалить'),
        ('update', 'Обновить значения полей'),
    )

    # class Media:
    #     js = ('items/js/items_list.js',)

    action = forms.ChoiceField(choices=ACTION_CHOICES, required=True)
    items = forms.MultipleChoiceField(validators=[validate_all_choices])
    arguments = forms.CharField(required=False)

    def clean_arguments(self):
        args = self.cleaned_data['arguments'].strip()
        if len(args) < 1:
            return {}
        try:
            args = json.loads(args)  # loads string as json
            # validate json_data
        except json.JSONDecodeError as e:
            raise forms.ValidationError('Invalid data in "arguments" field. Cause %s' % str(e))
            # if json data not valid:
            # raise forms.ValidationError("Invalid data in jsonfield")
        return args


class MeasurementInstrumentsEditForm(ItemsEditForm):
    items = forms.ModelMultipleChoiceField(queryset=MeasuringInstrument.objects.all().values('id'))

import types
class MeasurementInstrumentForm(forms.ModelForm):
    class Meta:
        model = MeasuringInstrument
        fields = [field.name for field in model._meta.get_fields() if field.editable]

    # def __init__(self, *args, **kwargs):
    #     super(MeasurementInstrumentForm, self).__init__(*args, **kwargs)
    #     for field in self.fields:
    #         if not hasattr(self.fields[field], 'queryset'):
    #             continue
    #
    #         # self.fields[field].queryset.all = list(self.fields[field].queryset)  # optimizing requests count
    #         self.fields[field].queryset.__all = self.fields[field].queryset.all
    #         def qs_all(self):
    #             return self.__all()
    #         qs_type = type(self.fields[field].queryset)
    #         self.fields[field].queryset.all = types.MethodType(qs_all, qs_type)


        # widgets = {
        #     'last_check_date': forms.DateField(attrs={'placeholder': 'ГГГГ-ММ-ДД'}),
        #     'last_repair_date': forms.DateField(attrs={'placeholder': 'ГГГГ-ММ-ДД'})
        # }

    # def clean(self):
    #     try:
    #         super(MeasurementInstrumentForm, self).clean()  # if necessary
    #     except BaseException as e:
    #         print('MeasurementInstrumentForm clean exception:', e)
    #
    #     # if self.cleaned_data.get('film') and 'director' in self._errors:
    #     #     del self._errors['director']
    #     return self.cleaned_data
