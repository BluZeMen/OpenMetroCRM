from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy

from .views import DialogView, DialogListView, DialogCreate, MessageCreateView

urlpatterns = [
    url(r'^$', DialogListView.as_view(), name='dialog-list'),
    url(r'^(?P<pk>[0-9]+)$', DialogView.as_view(), name='dialog'),
    url(r'^new-dialog$', DialogCreate.as_view(success_url=reverse_lazy('messaging:dialog-list')), name='dialog-create'),
    url(r'^new-message$', MessageCreateView.as_view(success_url=reverse_lazy('messaging:dialog')),
        name='message-create'),
]
