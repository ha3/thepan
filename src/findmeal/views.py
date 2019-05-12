from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Recipe

# Create your views here.

class IndexView(ListView):
    model = Recipe
    template_name = 'findmeal/index.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['home_page'] = 'active'
        return data
