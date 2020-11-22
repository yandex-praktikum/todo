from django.urls import path

from .views import About

app_name = 'static_pages'

urlpatterns = [
    path('about/', About.as_view(), name='about'),
]
