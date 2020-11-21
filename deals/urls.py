from django.urls import path

from .views import Home, TaskAddSuccess, TaskDetail, TaskList

app_name = 'deals'

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('task/', TaskList.as_view(), name='task_list'),
    path('task/<slug:slug>/', TaskDetail.as_view(), name='task_detail'),
    path('added/', TaskAddSuccess.as_view(), name='task_added'),
]
