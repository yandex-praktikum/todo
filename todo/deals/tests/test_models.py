# deals/tests/tests_models.py
from django.test import TestCase
from deals.models import Task


class TaskModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаём тестовую запись в БД
        # Не указываем значение slug, ждем, что при создании
        # оно создастся автоматически из text.
        # Ожидаем, что оно обрежется до 100 и будет 50 раз zh
        Task.objects.create(
            title='Ж'*100,
            text='Тестовый текст'
        )
        # Сохраняем созданную запись в качестве переменной класса
        cls.task = Task.objects.get(id=1)

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        task = TaskModelTest.task
        field_verboses = {
            'title': 'Заголовок',
            'text': 'Текст',
            'slug': 'Адрес для страницы с задачей',
            'image': 'Картинка',
        }
        for value, expected in field_verboses.items():
            with self.subTest():
                self.assertEqual(
                    task._meta.get_field(value).verbose_name, expected)

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        task = TaskModelTest.task
        field_help_texts = {
            'title': 'Дайте короткое название задаче',
            'text': 'Опишите суть задачи',
            'slug': ('Укажите адрес для страницы задачи. Используйте только '
                     'латиницу, цифры, дефисы и знаки подчёркивания'),
            'image': 'Загрузите картинку',
        }
        for value, expected in field_help_texts.items():
            with self.subTest():
                self.assertEqual(
                    task._meta.get_field(value).help_text, expected)

    def test_text_convert_to_slug(self):
        """save преобразует в slug поле text."""
        task = TaskModelTest.task
        slug = task.slug
        self.assertEquals(slug, 'zh'*50)

    def test_text_slug_max_length_not_exceed(self):
        """Длинный slug обрезается и не больше slug max_length."""
        task = TaskModelTest.task
        max_length_slug = task._meta.get_field('slug').max_length
        length_slug = (len(task.slug))
        self.assertEquals(max_length_slug, length_slug)

    def test_object_name_is_title_fild(self):
        """__str__  task - это строчка с содержимым task.title."""
        task = TaskModelTest.task
        expected_object_name = task.title
        self.assertEquals(expected_object_name, str(task))
