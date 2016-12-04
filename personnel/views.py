from django.views.generic import TemplateView, DetailView, ListView

from site_app.views import OrderedFilteredListViewMixin
from .models import Contact

# Create your views here.


class ContactView(DetailView):
    model = Contact

    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)
        return context


class ContactsListView(OrderedFilteredListViewMixin, ListView):
    model = Contact
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super(ContactsListView, self).get_context_data(**kwargs)
        return context

