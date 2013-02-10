# Django imports
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'index.html'

class Option1View(TemplateView):
    template_name = 'option1.html'

class Option2View(TemplateView):
    template_name = 'option2.html'

class Option3View(TemplateView):
    template_name = 'option3.html'