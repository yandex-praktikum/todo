from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from deals.models import Task


class TaskPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создадим запись в БД
        Task.objects.create(
            title='Заголовок',
            text='Текст',
            slug='test-slug',
        )

    def setUp(self):
        # Создаем неавторизованного клиента
        self.guest_client = Client()
        # Создаем авторизованного клиента
        self.user = get_user_model().objects.create_user(username='StasBasov')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    # Проверяем, что шаблоны используют имена указанных в настройках
    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        _templates_page_names = {
            'deals/home.html': reverse('deals:home'),
            'deals/added.html': reverse('deals:task_added'),
            'deals/task_list.html': reverse('deals:task_list'),
            'deals/task_list.html': reverse('deals:task_list'),
            'deals/task_detail.html': (
                reverse('deals:task_detail', kwargs={'slug': 'test-slug'})
            ),
        }
        for template, reverse_name in _templates_page_names.items():
            with self.subTest():
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    # Проверяем словари контекста
    def test_home_page_show_correct_context(self):
        """Шаблон home сформирован с правильным контекстом."""
        response = self.guest_client.get(reverse('deals:home'))
        # Ожидаемые поля формы
        _form_fields = {
            'title': forms.fields.CharField,
            # в формах TextField преобразуется в CharField
            # с виджетом forms.Textarea
            'text': forms.fields.CharField,
            'slug': forms.fields.SlugField,
            'image': forms.fields.ImageField,
        }
        # Проверяем, что форма создана с ожидаемыми полями
        for value, expected in _form_fields.items():
            with self.subTest():
                form_field = response.context.get('form').fields.get(value)
                # Проверяет, что поле формы является экземпляром
                # указанного класса
                self.assertIsInstance(form_field, expected)

    def test_task_list_page_list_is_1(self):
        response = self.authorized_client.get(reverse('deals:task_list'))
        self.assertEqual(len(response.context['object_list']), 1)

    def test_task_list_page_show_correct_context(self):
        """Шаблон task_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('deals:task_list'))
        # Взяли первый элемнет из списка и провреили, что его содержание
        # совпадает с ожидаемым
        task_title_0 = response.context.get('object_list')[0].title
        task_text_0 = response.context.get('object_list')[0].text
        task_slug_0 = response.context.get('object_list')[0].slug
        self.assertEqual(task_title_0, 'Заголовок')
        self.assertEqual(task_text_0, 'Текст')
        self.assertEqual(task_slug_0, 'test-slug')

    def test_task_detail_pages_show_correct_context(self):
        """Шаблон task_detail сформирован с правильным контекстом."""
        response = self.authorized_client.\
            get(reverse('deals:task_detail', kwargs={'slug': 'test-slug'}))
        self.assertEqual(response.context.get('task').title, 'Заголовок')
        self.assertEqual(response.context.get('task').text, 'Текст')
        self.assertEqual(response.context.get('task').slug, 'test-slug')

    # Недоступность страниц неавторизованному пользователю мы проверяли в
    # test_urls
