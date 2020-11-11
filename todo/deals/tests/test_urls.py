from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from deals.models import Task
# дергаем нейм и спотри кактой урл отозвался

class TaskURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создадим запись в БД, для проверки того, что при добавлении в БД
        # создается страница по адресу detail/<slug:slug>
        Task.objects.create(
            title='Тестовый заголовок',
            text='Тестовый текст',
            slug='test-slug'
        )

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем авторизованый клиент
        user = get_user_model()
        self.user = user.objects.create_user(username='StasBasov')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    # Проверяем общедоступные страницы
    def test_home_url_exists_at_desired_location(self):
        """Страница по адресу / доступна любому пользователю."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_task_added_url_exists_at_desired_location(self):
        """Страница по адресу /added/ доступна любому пользователю."""
        response = self.guest_client.get('/added/')
        self.assertEqual(response.status_code, 200)

    # Проверяем доступность страниц для авторизованного пользователя
    def test_task_list_url_exists_at_desired_location(self):
        """Страница по адресу /task/ доступна авторизованному пользователю."""
        response = self.authorized_client.get('/task/')
        self.assertEqual(response.status_code, 200)

    def test_task_detail_url_exists_at_desired_location_authorized(self):
        """Страница по адресу /task/test-slug/ доступна авторизованному
        пользователю."""
        response = self.authorized_client.get('/task/test-slug/')
        self.assertEqual(response.status_code, 200)

    # Проверяем редиректы для неавторизованного пользователя
    def test_task_list_url_redirect_anonymous_on_admin_login(self):
        """Страница по адресу /task/ перенаправит анонимного
        пользователя на страницу логина.
        """
        response = self.guest_client.get('/task/', follow=True)
        self.assertRedirects(
            response, '/admin/login/?next=/task/')

    def test_task_detail_url_redirect_anonymous_on_admin_login(self):
        """Страница по адресу /task/test_slug/ перенаправит анонимного
        пользователя на страницу логина.
        """
        response = self.client.get('/task/test-slug/', follow=True)
        self.assertRedirects(
            response, ('/admin/login/?next=/task/test-slug/'))

    # Шаблоны по адресам
    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            'deals/home.html': '/',
            'deals/added.html': '/added/',
            'deals/task_list.html': '/task/',
            'deals/task_detail.html': '/task/test-slug/',
        }
        for template, url in templates_url_names.items():
            with self.subTest():
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)
