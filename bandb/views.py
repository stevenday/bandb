# Django imports
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'index.html'

class HutView(TemplateView):
    template_name = 'hut.html'

class RatesView(TemplateView):
    template_name = 'rates.html'

class AreaView(TemplateView):
    template_name = 'area.html'

class AvailabilityView(TemplateView):
    template_name = 'availability.html'

class ThingsToKnowView(TemplateView):
    template_name = 'things-to-know.html'

class FindView(TemplateView):
    template_name = 'find.html'

class GalleryView(TemplateView):
    template_name = 'gallery.html'