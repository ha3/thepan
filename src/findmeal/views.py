from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import HttpResponse, JsonResponse

from .models import Recipe, Ingredient

# Create your views here.

class IndexView(ListView):
    model = Recipe
    template_name = 'findmeal/index.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['home_page'] = 'active'
        return data


class DetailView(DetailView):
    model = Recipe
    template_name = 'findmeal/detail.html'
    query_pk_and_slug = True


def rate(request, recipe_id):
    if request.is_ajax():
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        rating = int(request.POST['value'])

        recipe.rating = (recipe.rating * recipe.rateuser + rating) / (recipe.rateuser + 1)
        recipe.rateuser += 1
        recipe.save()

        return HttpResponse(recipe.rating)


def listIngredients(request):
    if request.is_ajax():
        name = request.POST['name']

        ingredients = Ingredient.objects.filter(name__startswith=name)
        return JsonResponse([ingredient.name for ingredient in ingredients], safe=False)
