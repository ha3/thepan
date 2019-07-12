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
    readonly_fields = ('rating', 'rate_count',)
    formfield_overrides = {
        models.DurationField: {'widget': SelectTimeWidget(minute_step=5)},
    }

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
admin.site.register(IngredientType)
