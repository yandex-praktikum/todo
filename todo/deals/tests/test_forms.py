import os
import shutil
import tempfile
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from deals.forms import TaskCreateForm
from deals.models import Task


class TaskCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаем временную папку для медиа-файлов
        # на момент теста медиа папка будет перопределена
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        # Создаем запись в базе данных для проверки сушествующего slug
        Task.objects.create(
            title='Тестовый заголовок',
            text='Тестовый текст',
            slug='first'
        )
        # Создаем форму, если нужна проверка атрибутов
        cls.form = TaskCreateForm()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        # Создаем неавторизованного клиента
        self.guest_client = Client()

    def test_create_task(self):
        """Валидная форма создает запись в Task."""
        # Проверим количество постов
        tasks_count = Task.objects.count()
        # Подготавливаем данные для передачи в форму
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00'
            b'\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
            b'\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        form_data = {
            'title': 'Тестовый заголовок',
            'text': 'Тестовый текст',
            'image': uploaded,
        }
        response = self.guest_client.post(
            reverse('deals:home'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, '/added/')
        self.assertEqual(Task.objects.count(), tasks_count+1)

    def test_cant_create_existing_slug(self):
        tasks_count = Task.objects.count()
        form_data = {
            'title': 'Заголовок из формы',
            'text': 'Текст из формы',
            'slug': 'first',
        }
        response = self.guest_client.post(
            reverse('deals:home'),
            data=form_data,
            follow=True
        )
        # Запись в базе данных не создалась
        self.assertEqual(Task.objects.count(), tasks_count)
        # Форма вернула ошибку с ожидаемым текстом
        self.assertFormError(
            response, 'form', 'slug', 'first уже существует'
        )
        # Но ничего не упало
        self.assertEqual(response.status_code, 200)

    # если не тестировали в models или переопределили
    def test_title_label(self):
        title_label = TaskCreateFormTests.form.fields['title'].label
        self.assertTrue(title_label, 'Заголовок')

    def test_title_help_text(self):
        title_help_text = TaskCreateFormTests.form.fields['title'].help_text
        self.assertTrue(title_help_text, 'Хелп для title')
