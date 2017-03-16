from django import forms
from django.utils.translation import ugettext_lazy as _

from personnel.models import Contact
from .models import Dialog


class MessageChatForm(forms.Form):
    text = forms.CharField(label='Текст сообщения', widget=forms.Textarea, required=True)

    class Media:
        js = ('messaging/js/forms.js',)

    def clean_text(self):
        text = self.cleaned_data['text'].strip()
        if len(text) < 1:
            raise forms.ValidationError('Message can\'t be empty')
        return text


class MessageForm(MessageChatForm):
    TODO_CHOICES = (
        (True, 'Создать новый диалог'),
        (False, 'Написать в существующий диалог'),
    )
    create_new_dialog = forms.ChoiceField(choices=TODO_CHOICES,
                                          widget=forms.RadioSelect(
                                              attrs={
                                                  'behavior': 'switch-ui-enabler',
                                                  'switch-items': """
                                                  {"dialog": "True", "dialog_name": "False", "receivers": "False"}
                                                  """
                                              }
                                          ), required=True, initial=True)
    dialog = forms.ModelChoiceField(
        label='Диалог',
        queryset=Dialog.objects.all(),
        required=False
    )
    dialog_name = forms.CharField(label='Название диалога', required=False)
    receivers = forms.ModelMultipleChoiceField(
        label='Получатели',
        queryset=Contact.objects.all(),
        required=False)