from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import HttpResponse, JsonResponse
from django.template import loader

from .models import Recipe, Ingredient, RecipeIngredient

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


class SearchView(ListView):
    template_name = 'findmeal/search.html'
    context_object_name = 'recipe_list'

    def get_queryset(self):
        query = self.request.GET.get('ingname')

        ingredients = query.split('-')

        ingredient_ids = [Ingredient.objects.get(name__iexact=ingredient) for ingredient in ingredients]
        recipe_ids = RecipeIngredient.objects.filter(ingredient__in=ingredient_ids).values_list('recipe', flat=True).distinct()

        return Recipe.objects.filter(id__in=recipe_ids)


def rate(request, recipe_id):
    if request.is_ajax():
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        rating = int(request.POST['value'])

        recipe.rating = (recipe.rating * recipe.rateuser + rating) / (recipe.rateuser + 1)
        recipe.rateuser += 1
        recipe.save()

        return HttpResponse(recipe.rating)


def ListIngredients(request):
    if request.is_ajax():
        name = request.POST['name'].capitalize()

        ingredients = Ingredient.objects.filter(name__startswith=name)
        return JsonResponse([ingredient.name for ingredient in ingredients], safe=False)
