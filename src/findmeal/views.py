from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.db.models.functions import Upper

from .models import Recipe, Ingredient, RecipeIngredient
from .forms import ContactForm

# Create your views here.

class IndexView(TemplateView):
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
        ingredients = self.request.GET.getlist('i')

        ingredient_ids = [Ingredient.objects.get(name__iexact=ingredient) for ingredient in ingredients]
        recipe_ids = RecipeIngredient.objects.filter(ingredient__in=ingredient_ids).values_list('recipe', flat=True).distinct()

        return Recipe.objects.filter(id__in=recipe_ids)


class RecipesView(ListView):
    template_name = 'findmeal/recipes.html'
    context_object_name = 'recipes_list'

    def get_queryset(self):
        return Recipe.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(*kwargs)
        data['recipes'] = 'active'
        return data


def ContactView(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            sender = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            recipients = ['h.ozdemir@yandex.com']

            send_mail(subject, message + sender, sender, recipients)
            return HttpResponseRedirect('/about/')

    else:
        form = ContactForm()

    return render(request, 'findmeal/contact.html', {'form': form, 'contact': 'active'})

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

        ingredients = Ingredient.objects.filter(name__icontains=name)
        return JsonResponse([ingredient.name for ingredient in ingredients], safe=False)
