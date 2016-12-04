from django.conf.urls import url

from .views import ContactsListView, ContactView


urlpatterns = [
    url(r'^$', ContactsListView.as_view(), name='contact-list'),
    url(r'^(?P<pk>[0-9]+)$', ContactView.as_view(), name='contact'),
]
