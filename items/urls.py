from django.conf.urls import url

from .views import (MeasuringInstrumentView, MeasuringInstrumentListView, MeasuringInstrumentCreateView,
                    MeasuringInstrumentUpdateView, MeasuringInstrumentListEditorView)

urlpatterns = [
    url(r'^mi$', MeasuringInstrumentListEditorView.as_view(), name='mi-list'),
    url(r'^mi/(?P<pk>[0-9]+)$', MeasuringInstrumentView.as_view(), name='mi'),
    url(r'^mi/(?P<pk>[0-9]+)/update$', MeasuringInstrumentUpdateView.as_view(), name='mi-update'),
    url(r'^mi/new-instrument', MeasuringInstrumentCreateView.as_view(), name='mi-create'),
]
