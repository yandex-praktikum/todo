from django.views.generic.base import TemplateView


class About(TemplateView):
    template_name = 'static_pages/about.html'
