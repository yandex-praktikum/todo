# deals/tests/tests_models.py
from django.test import TestCase

from deals.models import Task


class TaskModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаём тестовую запись в БД и
        # сохраняем ее в качестве переменной класса
        # Не указываем значение slug, ждем, что при создании
        # оно создастся автоматически из title.
        # А title сделаем таким, чтобы после транслитерации он стал
        # более 100 символов (буква "ж" транслитерируется в два символа: "zh")
        #
        cls.task = Task.objects.create(
            title='Ж'*100,
            text='Тестовый текст'
        )

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
            with self.subTest(value=value):
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
            with self.subTest(value=value):
                self.assertEqual(
                    task._meta.get_field(value).help_text, expected)

    def test_text_convert_to_slug(self):
        """Содержимое поля title преобразуется в slug."""
        task = TaskModelTest.task
        slug = task.slug
        self.assertEquals(slug, 'zh'*50)

    def test_text_slug_max_length_not_exceed(self):
        """
        Длинный slug обрезается и не превышает max_length поля slug в модели.
        """
        task = TaskModelTest.task
        max_length_slug = task._meta.get_field('slug').max_length
        length_slug = len(task.slug)
        self.assertEqual(max_length_slug, length_slug)

    def test_object_name_is_title_fild(self):
        """В поле __str__  объекта task записано значение поля task.title."""
        task = TaskModelTest.task
        expected_object_name = task.title
        self.assertEqual(expected_object_name, str(task))
