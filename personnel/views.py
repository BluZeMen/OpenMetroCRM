from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

from site_app.views import OrderedFilteredListViewMixin
from .models import Contact, Contractor


# Create your views here.


class ContactView(LoginRequiredMixin, DetailView):
    model = Contact

    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)
        return context


class ContactsListView(LoginRequiredMixin, OrderedFilteredListViewMixin, ListView):
    model = Contact
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super(ContactsListView, self).get_context_data(**kwargs)
        context['object_list'] = context['object_list'].select_related('home_location')
        return context


class ContractorView(LoginRequiredMixin, DetailView):
    model = Contractor

    def get_context_data(self, **kwargs):
        context = super(ContractorView, self).get_context_data(**kwargs)
        return context


class ContractorListView(LoginRequiredMixin, OrderedFilteredListViewMixin, ListView):
    model = Contractor
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super(ContractorListView, self).get_context_data(**kwargs)
        return context
