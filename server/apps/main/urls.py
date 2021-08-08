from django.urls import path

from server.apps.main.views import index

app_name = 'site'

urlpatterns = [
    path('hello/', index, name='hello'),
]
