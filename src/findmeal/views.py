from django.shortcuts import render
from django.views.generic import ListView

from .models import Recipe

# Create your views here.

class IndexView(ListView):
    model = Recipe
    template_name = 'findmeal/index.html'
