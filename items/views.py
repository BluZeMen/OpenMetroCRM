from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import SuspiciousOperation
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView, CreateView
from django.views.generic.edit import UpdateView

from site_app.utils import get_fields_names
from site_app.views import OrderedFilteredListViewMixin, ListViewEditorMixin
from .forms import MeasurementInstrumentForm, MeasurementInstrumentsEditForm
from .models import MeasuringInstrument


# Create your views here.


class MeasuringInstrumentView(DetailView):
    model = MeasuringInstrument


class MeasuringInstrumentCreateView(LoginRequiredMixin, CreateView):
    model = MeasuringInstrument
    fields = [n for n in get_fields_names(model)
              if n not in ['repair_description', 'last_repair_date']]


class MeasuringInstrumentUpdateView(LoginRequiredMixin, UpdateView):
    model = MeasuringInstrument
    fields = get_fields_names(model)


class MeasuringInstrumentListView(OrderedFilteredListViewMixin, ListView):
    model = MeasuringInstrument
    paginate_by = 100
    ordering = 'next_check_date'

    def get_queryset(self, *args, **kwargs):
        q = super(MeasuringInstrumentListView, self).get_queryset(*args, **kwargs)
        return self.model.objects.annotate_next_check_date(q)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        multiedit_form = MeasurementInstrumentForm()

        # optimization
        if 'holder' in multiedit_form.fields:
            multiedit_form.fields['holder'].queryset = multiedit_form.fields['holder'].queryset.select_related('type')
        context['multiedit_form'] = multiedit_form

        # optimization
        context['object_list'] = context['object_list'].select_related('type', 'type__kind', 'holder', 'holder__holder')

        context['today'] = datetime.now()
        return context


class MeasuringInstrumentListEditorView(LoginRequiredMixin, MeasuringInstrumentListView, ListViewEditorMixin):
    items_editor_form = MeasurementInstrumentsEditForm
    allowed_actions = 'delete', 'update'

    # template_name = 'items/measuringinstrument_list_editor.html'

    def delete(self, editor_form, context, *args, **kwargs):
        editor_form.cleaned_data['items'].all().delete()
        return redirect(reverse('items:mi-list'))

    def update(self, editor_form, context, *args, **kwargs):
        # print('args:', editor_form.cleaned_data['arguments'])
        allowed_fields = [field.name for field in self.model._meta.get_fields() if field.editable]
        bad_fields = [name for name in editor_form.cleaned_data['arguments'] if name not in allowed_fields]
        if bad_fields:
            raise SuspiciousOperation('Bad fields in request: %s' % ', '.join(bad_fields))
        editor_form.cleaned_data['items'].update(**editor_form.cleaned_data['arguments'])
        return redirect(reverse('items:mi-list'))
