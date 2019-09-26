from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core import mail, serializers
from rest_framework.generics import RetrieveAPIView, ListAPIView, UpdateAPIView
from rest_framework.response import Response

from .models import Recipe, Ingredient, RecipeIngredient
from .forms import ContactForm
from .serializers import DetailViewSerializer, ListRecipesSerializer, ListIngredientsSerializer, RateRecipeSerializer

class IndexView(generic.TemplateView):
    template_name = 'findmeal/index.html'


class DetailView(RetrieveAPIView):
    queryset = Recipe.objects.all()
    serializer_class = DetailViewSerializer


class SearchView(ListAPIView):
    serializer_class = ListRecipesSerializer

    def get_queryset(self):
        ingredients = self.request.GET.getlist('i')

        ingredient_ids = Ingredient.objects.filter(id__in=ingredients)
        recipe_ids = RecipeIngredient.objects.filter(ingredient__in=ingredient_ids).values_list('recipe', flat=True).distinct()

        return Recipe.objects.filter(id__in=recipe_ids)


class RecipesView(ListAPIView):
    queryset = Recipe.objects.all().order_by('-id')
    serializer_class = ListRecipesSerializer


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

            mail.send_mail(subject, message, sender, recipients)
            return HttpResponseRedirect('/about/')

        return render(request, self.template_name, {'form': form})

    def get(self, request, *args, **kwargs):
        form = self.form_class()

        return render(request, self.template_name, {'form': form})


class ListIngredients(ListAPIView):
    serializer_class = ListIngredientsSerializer

    def get_queryset(self):
        name = self.request.GET.get('name').capitalize()
        response = Ingredient.objects.filter(name__icontains=name)

        return response


class RateRecipeView(UpdateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RateRecipeSerializer

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
