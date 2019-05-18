from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import HttpResponse

from .models import Recipe

# Create your views here.

class IndexView(ListView):
    model = Recipe
    template_name = 'findmeal/index.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['home_page'] = 'active'
        return data


def rate(request, recipe_id):

    recipe = get_object_or_404(Recipe, pk=recipe_id)

    rating = int(request.POST['value'])

    recipe.rating = (recipe.rating * recipe.rateuser + rating) / (recipe.rateuser + 1)
    recipe.rateuser += 1
    recipe.save()

    return HttpResponse(recipe.rating)
