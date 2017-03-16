from enum import Enum

from django.core.exceptions import SuspiciousOperation
from django.views.generic import TemplateView


# Create your views here.
from django.views.generic.list import ListView

from items.forms import ItemsEditForm


class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        return context


class OrderedFilteredListViewMixin:
    """
    OrderedFilteredListViewMixin, which adds ordering and ordering by "get" url.
    Filters in urls begins with "fltr_" string, and after goes like well known QuerySet filter() named
    arguments. For example: www.example.com/items/1?fltr_type__name_
    """

    def get_queryset(self):
        prefix = 'fltr_'
        filters = [k[len(prefix):] for k in dict(self.request.GET).keys() if k[:len(prefix)] == prefix]
        filters = {f: self.request.GET[prefix + f] for f in filters}

        # print('filters=', filters)
        qs = self.model.objects
        if filters:
            qs = qs.filter(**filters)
        else:
            qs = qs.all()

        ordering = self.request.GET.get('order_by', self.ordering)
        if ordering:
            qs = qs.order_by(ordering)
        return qs


class ViewPostDispatcherMixin:
    action_form_argument_name = 'action'
    allowed_actions = []

    class ReturnCode(Enum):
        OK = 0
        WARNING = 1
        FAIL = 2
        PERMISSION_DENIED = 3

    def __init__(self, *args, **kwargs):
        super(self).__init__(*args, **kwargs)

    def get_allowed_actions(self):
        return self.allowed_actions

    def _not_found_action(self, request, context, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        allowed_actions = self.allowed_actions()
        self.object_list = self.object_list()
        context = self.get_context_data(object=self.object_list)
        if self.action_form_argument_name not in request.POST:
            return self.render_to_response(context)
        action = request.POST[self.action_form_argument_name]
        if action in allowed_actions:
            getattr(self, action, self._not_found_action)(request, context, *args, **kwargs)
        return self.render_to_response(context)


class ListViewEditorMixin(ViewPostDispatcherMixin):
    items_editor_form = ItemsEditForm
    def _not_found_action(self, form, context, *args, **kwargs):
        raise SuspiciousOperation('No such action in editor')

    def post(self, request, *args, **kwargs):
        allowed_actions = self.get_allowed_actions()
        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list)
        if self.action_form_argument_name not in request.POST:
            return self.render_to_response(context)
        action = request.POST[self.action_form_argument_name]
        if action in allowed_actions:
            editor_form = self.items_editor_form(request.POST)
            if editor_form.is_valid():
                result = getattr(self, action, self._not_found_action)(editor_form, context, *args, **kwargs)
                if result:
                    return result
            else:
                raise SuspiciousOperation('Invalid editor form')
        return self.render_to_response(context)
