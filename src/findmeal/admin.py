from django.contrib import admin
from django.db import models

from .models import Recipe, RecipeStep, RecipeIngredient, Ingredient, IngredientType
from .widgets import SelectTimeWidget

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient


class RecipeStepInline(admin.StackedInline):
    model = RecipeStep

class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeStepInline, RecipeIngredientInline]
    formfield_overrides = {
        models.DurationField: {'widget': SelectTimeWidget(minute_step=5, use_seconds=False)},
    }


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
admin.site.register(IngredientType)
