from django.contrib import admin

from .models import Recipe, RecipeStep, RecipeIngredient, Ingredient, IngredientType

# Register your models here.

class RecipeStepInline(admin.StackedInline):
    model = RecipeStep
    extra = 3

class RecipeIngredientInline(admin.StackedInline):
    model = RecipeIngredient
    extra = 3

class RecipeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
    ]

    inlines = [RecipeIngredientInline, RecipeStepInline]


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
admin.site.register(IngredientType)
