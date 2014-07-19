from django.conf.urls import patterns, include, url
from .views import EnvayaSMSBackendView

urlpatterns = patterns('',
    (r'^$',  EnvayaSMSBackend.as_view(backend_name='envayasms')),
)
