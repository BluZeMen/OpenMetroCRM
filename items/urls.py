from django.conf.urls import url

from .views import MeasuringInstrumentView, MeasuringInstrumentListView


urlpatterns = [
    url(r'^mi$', MeasuringInstrumentListView.as_view(), name='mi-list'),
    url(r'^mi/(?P<pk>[0-9]+)$', MeasuringInstrumentView.as_view(), name='mi'),
]
