from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(default='', editable=False, max_length=100)
    image = models.ImageField(upload_to='recipe')
    prep = models.IntegerField()
    serving = models.IntegerField()
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, default=0)
    rateuser = models.IntegerField(null=True, blank=True, default=0)
    calorie = models.IntegerField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        kwargs = {
            'pk': self.id,
            'slug': self.slug
        }

        return reverse('findmeal:detail', kwargs=kwargs)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def prep_time(self):
        hours = self.prep // 60
        minutes = self.prep % 60

        if minutes == 0: # Check if it is a full hour
            return str(hours) + ' saat'
        elif minutes > 60:
            return str(hours) + ' saat ' + str(minutes) + ' dakika'
        else:
            return str(minutes) + ' dakika'

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
