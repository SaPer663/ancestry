from django.urls import path

from server.apps.site.views import index

app_name = 'site'

urlpatterns = [
    path('', index, name='home_page'),
]
