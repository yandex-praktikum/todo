from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from deals.models import Task

User = get_user_model()


class TaskURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Создадим запись в БД для проверки доступности адреса task/test-slug/
        Task.objects.create(
            title='Тестовый заголовок',
            text='Тестовый текст',
            slug='test-slug',
        )

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем авторизованый клиент
        self.user = User.objects.create_user(username='StasBasov')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    # Проверяем общедоступные страницы
    def test_home_url_exists_at_desired_location(self):
        """Страница / доступна любому пользователю."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_task_added_url_exists_at_desired_location(self):
        """Страница /added/ доступна любому пользователю."""
        response = self.guest_client.get('/added/')
        self.assertEqual(response.status_code, 200)

    # Проверяем доступность страниц для авторизованного пользователя
    def test_task_list_url_exists_at_desired_location(self):
        """Страница /task/ доступна авторизованному пользователю."""
        response = self.authorized_client.get('/task/')
        self.assertEqual(response.status_code, 200)

    def test_task_detail_url_exists_at_desired_location_authorized(self):
        """Страница /task/test-slug/ доступна авторизованному пользователю."""
        response = self.authorized_client.get('/task/test-slug/')
        self.assertEqual(response.status_code, 200)

    # Проверяем редиректы для неавторизованного пользователя
    def test_task_list_url_redirect_anonymous_on_admin_login(self):
        """Страница /task/ перенаправит анонимного пользователя
        на страницу логина.
        """
        response = self.guest_client.get('/task/', follow=True)
        self.assertRedirects(
            response, '/admin/login/?next=/task/')

    def test_task_detail_url_redirect_anonymous_on_admin_login(self):
        """Страница /task/test_slug/ перенаправит анонимного пользователя
        на страницу логина.
        """
        response = self.client.get('/task/test-slug/', follow=True)
        self.assertRedirects(
            response, ('/admin/login/?next=/task/test-slug/'))

    # Проверка вызываемых шаблонов для каждого адреса
    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            'deals/home.html': '/',
            'deals/added.html': '/added/',
            'deals/task_list.html': '/task/',
            'deals/task_detail.html': '/task/test-slug/',
        }
        for template, url in templates_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)
