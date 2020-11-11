from django.core.exceptions import ValidationError
from django import forms
from pytils.translit import slugify

from .models import Task


class TaskCreateForm(forms.ModelForm):
    """Форма для создания задания."""
    class Meta:
        model = Task
        # Магия Джанго. Кортеж из всех полей
        # labels и help_texts берутся из полей модели
        fields = ('__all__')

    # Валидация поля slug.
    def clean_slug(self):
        """Обрабатывает случай, если slug уже существует."""
        cleaned_data = super(TaskCreateForm, self).clean()
        slug = cleaned_data.get('slug')
        if not slug:
            title = cleaned_data.get('title')
            slug = slugify(title)[:100]
        if Task.objects.filter(slug=slug).exists():
            raise ValidationError(f'{slug} уже существует')
        return slug
