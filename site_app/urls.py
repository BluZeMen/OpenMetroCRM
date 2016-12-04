"""site_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from .views import DashboardView


urlpatterns = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy('dashboard'), permanent=False), name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^personnel/', include('personnel.urls', namespace='personnel')),
    url(r'^items/', include('items.urls', namespace='items')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    # urlpatterns += [url(r'^static/(.*)$', 'django.views.static.serve', {
    #                     'document_root': settings.STATIC_ROOT
    #                 }),
    #                 url(r'^media/(.*)$', 'django.views.static.serve', {
    #                     'document_root': settings.MEDIA_ROOT
    #                 })
    # ]
