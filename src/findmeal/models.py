from django.db import models

# Create your models here.

class Recipe(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class IngredientType(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    type = models.ForeignKey(IngredientType, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class RecipeStep(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    instructions = models.TextField()

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount_required = models.IntegerField()
    step = models.ForeignKey(RecipeStep, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.recipe)
