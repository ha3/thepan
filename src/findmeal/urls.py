from django.urls import path

from . import views
from django.contrib.flatpages import views as flat_views

app_name = 'findmeal'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('recipe/<int:pk>/<str:slug>/', views.DetailView.as_view(), name='detail'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('recipes/', views.RecipesView.as_view(), name='recipes'),
    path('contact/', views.ContactView, name='contact'),
    path('<int:recipe_id>/rate/', views.rate, name='rate'),
    path('listing/', views.ListIngredients, name='listing'),
    path('about/', flat_views.flatpage, {'url': '/about/'}, name='about')
]
