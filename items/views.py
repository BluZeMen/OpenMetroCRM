import datetime
from django.views.generic import TemplateView, DetailView, ListView

from .models import MeasuringInstrument, MeasuringInstrumentKind, MeasuringInstrumentType
from site_app.views import OrderedFilteredListViewMixin

# Create your views here.


class MeasuringInstrumentView(DetailView):
    model = MeasuringInstrument

    def get_context_data(self, **kwargs):
        context = super(MeasuringInstrumentView, self).get_context_data(**kwargs)
        return context


class MeasuringInstrumentListView(OrderedFilteredListViewMixin, ListView):
    model = MeasuringInstrument
    paginate_by = 100
    ordering = 'next_check_date'

    def get_context_data(self, **kwargs):
        context = super(MeasuringInstrumentListView, self).get_context_data(**kwargs)
        return context

