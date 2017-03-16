from django.conf.urls import url

from .views import ContactsListView, ContactView, ContractorListView, ContractorView

urlpatterns = [
    url(r'^contact$', ContactsListView.as_view(), name='contact-list'),
    url(r'^contact/(?P<pk>[0-9]+)$', ContactView.as_view(), name='contact'),
    url(r'^contractor$', ContractorListView.as_view(), name='contractor-list'),
    url(r'^contractor/(?P<pk>[0-9]+)$', ContractorView.as_view(), name='contractor'),
]
