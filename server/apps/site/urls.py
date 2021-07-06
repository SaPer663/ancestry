from django.urls import path

from . import views

app_name = 'site'

urlpatterns = [
    path('', views.index, name='home_page'),
    path('<int:pk>/<slug:family>', views.detail_family, name='detail_family')
]
