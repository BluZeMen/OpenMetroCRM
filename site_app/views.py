from django.views.generic import TemplateView, DetailView, ListView


# Create your views here.


class DashboardView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        return context


class OrderedFilteredListViewMixin():
    """
    ListViewMixin, which adds ordering and ordering by "get" url.
    Filters in urls begins with "fltr_" string, and after goes like well known QuerySet filter() named
    arguments. For example: www.example.com/items/1?fltr_type__name_
    """

    def get_queryset(self):
        prefix = 'fltr_'
        filters = [k[len(prefix):] for k in dict(self.request.GET).keys() if k[:len(prefix)] == prefix]
        filters = {f: self.request.GET[prefix + f] for f in filters}

        print('filters=', filters)
        qs = self.model.objects
        if filters:
            qs = qs.filter(**filters)
        else:
            qs = qs.all()

        ordering = self.request.GET.get('order_by', self.ordering)
        if ordering:
            qs = qs.order_by(ordering)
        return qs
