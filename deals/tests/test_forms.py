import shutil
import tempfile

from deals.forms import TaskCreateForm
from deals.models import Task
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

# Создаем временную папку для медиа-файлов;
# на момент теста медиа папка будет переопределена
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


# Для сохранения media-файлов в тестах будет использоватьсяgs
# временная папка TEMP_MEDIA_ROOT, а потом мы ее удалим
@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TaskCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
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
        super().tearDownClass()
        # Модуль shutil - библиотека Python с прекрасными инструментами 
        # для управления файлами и директориями: 
        # создание, удаление, копирование, перемещение, изменение папок и файлов
        # Метод shutil.rmtree удаляет директорию и всё её содержимое
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()

    def test_create_task(self):
        """Валидная форма создает запись в Task."""
        # Подсчитаем количество записей в Task
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
        # Проверяем, сработал ли редирект
        self.assertRedirects(response, reverse('deals:task_added'))
        # Проверяем, увеличилось ли число постов
        self.assertEqual(Task.objects.count(), tasks_count+1)
        # Проверяем, что создалась запись с нашим слагом
        self.assertTrue(
            Task.objects.filter(
                slug='testovyij-zagolovok',
                text='Тестовый текст',
                image='tasks/small.gif'
                ).exists()
        )

    def test_cant_create_existing_slug(self):
        # Подсчитаем количество записей в Task
        tasks_count = Task.objects.count()
        form_data = {
            'title': 'Заголовок из формы',
            'text': 'Текст из формы',
            'slug': 'first',  # отправим в форму slug, который уже есть в БД
        }
        # Отправляем POST-запрос
        response = self.guest_client.post(
            reverse('deals:home'),
            data=form_data,
            follow=True
        )
        # Убедимся, что запись в базе данных не создалась:
        # сравним количество записей в Task до и после отправки формы
        self.assertEqual(Task.objects.count(), tasks_count)
        # Проверим, что форма вернула ошибку с ожидаемым текстом:
        # из объекта responce берём словарь 'form',
        # указываем ожидаемую ошибку для поля 'slug' этого словаря
        self.assertFormError(
            response,
            'form',
            'slug',
            'Адрес "first" уже существует, придумайте уникальное значение'
        )
        # Проверим, что ничего не упало и страница отдаёт код 200
        self.assertEqual(response.status_code, 200)

    # Если не тестировали содержимое лейблов в models
    # или переопределили их при создании формы - тестируем так:
    def test_title_label(self):
        title_label = TaskCreateFormTests.form.fields['title'].label
        self.assertEqual(title_label, 'Заголовок')

    def test_title_help_text(self):
        title_help_text = TaskCreateFormTests.form.fields['title'].help_text
        self.assertEqual(title_help_text, 'Дайте короткое название задаче')
