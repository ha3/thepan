from django.contrib import admin

from .models import Recipe, RecipeStep, RecipeIngredient, Ingredient, IngredientType
from .widgets import DurationInput

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 3


class RecipeStepInline(admin.StackedInline):
    model = RecipeStep
    extra = 3

class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeStepInline, RecipeIngredientInline]
    formfield_overrides = {
        models.DurationField: {'widget': DurationInput},
    }


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
admin.site.register(IngredientType)
