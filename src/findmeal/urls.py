from django.urls import path

from . import views

app_name = 'findmeal'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('recipe/<int:pk>/<str:slug>/', views.DetailView.as_view(), name='detail'),
    path('<int:recipe_id>/rate/', views.rate, name='rate'),
]
