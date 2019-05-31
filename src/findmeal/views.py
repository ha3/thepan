from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.mail import send_mail

from .models import Recipe, Ingredient, RecipeIngredient
from .forms import ContactForm

# Create your views here.

class IndexView(generic.TemplateView):
    template_name = 'findmeal/index.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['home_page'] = 'active'
        return data


class DetailView(generic.DetailView):
    model = Recipe
    template_name = 'findmeal/detail.html'
    query_pk_and_slug = True


class SearchView(generic.ListView):
    template_name = 'findmeal/search.html'
    context_object_name = 'recipe_list'

    def get_queryset(self):
        ingredients = self.request.GET.getlist('i')

        ingredient_ids = [Ingredient.objects.get(name__iexact=ingredient) for ingredient in ingredients]
        recipe_ids = RecipeIngredient.objects.filter(ingredient__in=ingredient_ids).values_list('recipe', flat=True).distinct()

        return Recipe.objects.filter(id__in=recipe_ids)


class RecipesView(generic.ListView):
    template_name = 'findmeal/recipes.html'
    context_object_name = 'recipes_list'

    def get_queryset(self):
        return Recipe.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(*kwargs)
        data['recipes'] = 'active'
        return data


class ContactView(View):
    form_class = ContactForm
    template_name = 'findmeal/contact.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            sender = form.cleaned_data['sender']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            recipients = ['h.ozdemir@yandex.com']

            send_mail(subject, message + sender, sender, recipients)
            return HttpResponseRedirect('/about/')

        return render(request, self.template_name, {'form': form, 'contact': 'active'})

    def get(self, request, *args, **kwargs):
        form = self.form_class()

        return render(request, self.template_name, {'form': form, 'contact': 'active'})


class ListIngredients(View):
    def post(self, request):
        if request.is_ajax():
            name = request.POST['name'].capitalize()

            ingredients = Ingredient.objects.filter(name__icontains=name)
            return JsonResponse([ingredient.name for ingredient in ingredients], safe=False)


def rate(request, recipe_id):
    if request.is_ajax():
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        rating = int(request.POST['value'])

        recipe.rating = (recipe.rating * recipe.rateuser + rating) / (recipe.rateuser + 1)
        recipe.rateuser += 1
        recipe.save()

        return HttpResponse(recipe.rating)
