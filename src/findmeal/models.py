from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.dateparse import parse_duration

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(default='', editable=False, max_length=100)
    image = models.ImageField(upload_to='recipe')
    prep_time = models.DurationField()
    serving = models.IntegerField()
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, default=0)
    rate_count = models.IntegerField(null=True, blank=True, default=0)
    calorie = models.IntegerField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        kwargs = {
            'pk': self.id,
            'slug': self.slug
        }

        return reverse('findmeal:detail', kwargs=kwargs)

    def display_prep_time(self):
        duration = parse_duration(str(self.prep_time))

        seconds = duration.seconds

        minutes = seconds // 60
        hours = minutes // 60
        minutes %= 60

        if hours > 0:
            if minutes == 0:
                return f'{str(hours)} saat'
            else:
                return f'{str(hours)} saat {str(minutes)} dakika'
        else:
            return f'{str(minutes)} dakika'


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
