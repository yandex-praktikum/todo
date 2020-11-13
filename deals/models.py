from django.db import models
# pip3 install pytils не забыть установить!
from pytils.translit import slugify


class Task(models.Model):
    title = models.CharField(
        'Заголовок',
        default='Значение по-умолчанию',
        max_length=100,
        help_text='Дайте короткое название задаче'
    )
    text = models.TextField(
        'Текст',
        help_text='Опишите суть задачи'
    )
    slug = models.SlugField(
        'Адрес для страницы с задачей',
        max_length=100,
        unique=True,
        blank=True,
        help_text=('Укажите адрес для страницы задачи. Используйте только '
                   'латиницу, цифры, дефисы и знаки подчёркивания')
    )
    image = models.ImageField(
        'Картинка',
        upload_to='tasks/',
        blank=True,
        null=True,
        help_text='Загрузите картинку'
    )

    def __str__(self):
        return self.title

    # Расширение встроенного метода save(): если поле slug не заполнено -
    # транслитерировать в латиницу содержимое поля title и
    # обрезать до ста знаков
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:100]
        super().save(*args, **kwargs)
