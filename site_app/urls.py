"""site_app URL Configuration
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from registration.backends.default.views import RegistrationView
from registration.forms import RegistrationFormUniqueEmail

from .views import DashboardView

urlpatterns = [
    # Home
    url(r'^$', RedirectView.as_view(url=reverse_lazy('dashboard'), permanent=False), name='home'),

    # Site dashboard
    url(r'^dashboard$', DashboardView.as_view(), name='dashboard'),

    # Apps routing
    url(r'^messaging/', include('messaging.urls', namespace='messaging')),
    url(r'^personnel/', include('personnel.urls', namespace='personnel')),
    url(r'^items/', include('items.urls', namespace='items')),

    # Accounts routine
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, name='logout'),
    url(r'^accounts/password/reset/$', auth_views.password_reset,
        name='password_reset'),
    url(r'^accounts/password/change/done/$', auth_views.password_change_done, name='password_change_done'),
    url(r'^accounts/password/reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^accounts/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm,
        {'post_reset_redirect': reverse_lazy('password_reset_complete')}, name='password_reset_confirm'),
    url(r'^accounts/password/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

    # django-registration
    url(r'^accounts/register/$', RegistrationView.as_view(form_class=RegistrationFormUniqueEmail), name='registration_register'),
    url(r'^accounts/', include('registration.backends.default.urls')),

    # admin
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
