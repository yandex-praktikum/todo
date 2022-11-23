from django import forms
from django.core.exceptions import ValidationError
from pytils.translit import slugify

from .models import Task


class TaskCreateForm(forms.ModelForm):
    """Форма для создания задания."""
    class Meta:
        model = Task
        # Магия Джанго: через '__all__' создаётся форма из всех полей модели
        # labels и help_texts берутся из verbose_name и help_text
        fields = '__all__'

    # Валидация поля slug
    def clean_slug(self):
        """Обрабатывает случай, если slug не уникален."""
        cleaned_data = super().clean()
        slug = cleaned_data['slug']
        if not slug:
            title = cleaned_data['title']
            slug = slugify(title)[:100]
        if Task.objects.filter(slug=slug).exists():
            raise ValidationError(f'Адрес "{slug}" уже существует, '
                                  'придумайте уникальное значение')
        return slug
