from django.db import models

# Create your models here.

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='recipe')
    prep = models.IntegerField()

    def __str__(self):
        return self.name

class IngredientType(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=150)

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

    def __str__(self):
        return str(self.recipe)

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return str(self.recipe)
