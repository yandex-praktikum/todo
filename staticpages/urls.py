from django.urls import path

from .views import About

app_name = 'staticpages'

urlpatterns = [
    path('about/', About.as_view(), name='about'),
]
