from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView

from .forms import TaskCreateForm
from .models import Task


class Home(CreateView):
    """Форма добавления задания."""
    template_name = 'deals/home.html'
    form_class = TaskCreateForm
    success_url = reverse_lazy('deals:task_added')


class TaskList(LoginRequiredMixin, ListView):
    """Список всех доступных заданий."""
    login_url = '/admin/login/'
    model = Task
    template_name = 'deals/task_list.html'


class TaskDetail(LoginRequiredMixin, DetailView):
    """Задание подробно."""
    login_url = '/admin/login/'
    model = Task
    template_name = 'deals/task_detail.html'


class TaskAddSuccess(TemplateView):
    """Задание успешно добавлено."""
    template_name = 'deals/added.html'
