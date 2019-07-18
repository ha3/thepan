import datetime

from django.test import TestCase, Client
from django.urls import reverse
from .models import Recipe, RecipeStep, RecipeIngredient, Ingredient, IngredientType

class ModelTests(TestCase):
    def test_strs(self):
        fruit = IngredientType(name='fruit')
        apple = Ingredient(name='Apple')
        apple_tart = Recipe(name='Apple Tart')
        ri_apple_tart = RecipeIngredient(recipe=apple_tart, ingredient=apple)
        rs_apple_tart = RecipeStep(recipe=apple_tart)

        self.assertEqual(apple.__str__(), apple.name)
        self.assertEqual(fruit.__str__(), fruit.name)
        self.assertEqual(apple_tart.__str__(), apple_tart.name)
        self.assertEqual(rs_apple_tart.__str__(), rs_apple_tart.recipe.name)
        self.assertEqual(ri_apple_tart.__str__(), ri_apple_tart.recipe.name)

    def test_display_prep_time(self):
        case_one = Recipe(prep_time=datetime.timedelta(seconds=5400))
        case_two = Recipe(prep_time=datetime.timedelta(seconds=7200))
        case_three = Recipe(prep_time=datetime.timedelta(seconds=2700))

        self.assertEqual(case_one.display_prep_time(), '1 saat 30 dakika')
        self.assertEqual(case_two.display_prep_time(), '2 saat')
        self.assertEqual(case_three.display_prep_time(), '45 dakika')

    def test_get_absolute_url(self):
        apple_tart = Recipe.objects.create(
            name='Apple Tart',
            prep_time = datetime.timedelta(seconds=5400),
            serving = 4,
            calorie = 1000
        )

        self.assertEqual(
            f'/recipe/{apple_tart.pk}/{apple_tart.slug}/',
            apple_tart.get_absolute_url()
        )

class SearchViewTests(TestCase):
    def setUp(self):
        # Create ingredient types
        self.fruit = IngredientType.objects.create(name='fruit')
        self.vegetable = IngredientType.objects.create(name='vegetable')

        # Create ingredients
        self.apple = Ingredient.objects.create(type=self.fruit, name='Apple')
        self.grape = Ingredient.objects.create(type=self.fruit, name='Grape')
        self.tomato = Ingredient.objects.create(type=self.vegetable, name='Tomato')

        # Create recipes
        self.apple_tart = Recipe.objects.create(
            name='Apple Tart',
            prep_time = datetime.timedelta(seconds=100),
            serving = 4,
            calorie = 1000
        )
        self.maple = Recipe.objects.create(
            name='Maple',
            prep_time = datetime.timedelta(seconds=250),
            serving = 2,
            calorie = 750
        )

        # Create recipe steps
        self.step_one_apple_tart = RecipeStep.objects.create(recipe=self.apple_tart, instructions='Step 1')
        self.step_one_maple = RecipeStep.objects.create(recipe=self.maple, instructions='Step 1')
        self.step_two_maple = RecipeStep.objects.create(recipe=self.maple, instructions='Step 2')

        # Create recipe ingredients
        self.ri_one_apple_tart = RecipeIngredient.objects.create(recipe=self.apple_tart, ingredient=self.apple, amount=1)
        self.ri_two_apple_tart = RecipeIngredient.objects.create(recipe=self.apple_tart, ingredient=self.grape, amount=2)
        self.ri_one_maple = RecipeIngredient.objects.create(recipe=self.maple, ingredient=self.grape, amount=1)
        self.ri_two_maple = RecipeIngredient.objects.create(recipe=self.maple, ingredient=self.tomato, amount=1)

    def test_no_ingredients(self):
        response = self.client.get(reverse('findmeal:search'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No recipes are available.')
        self.assertQuerysetEqual(response.context['recipe_list'], [])

    def test_search_recipe_with_distinct_ingredient(self):
        response = self.client.get(reverse('findmeal:search'), {'i': self.apple.id})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['recipe_list'],
            ['<Recipe: Apple Tart>']
        )

    def test_search_recipe_with_non_distinct_ingredient(self):
        response = self.client.get(reverse('findmeal:search'), {'i': self.grape.id})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['recipe_list'],
            ['<Recipe: Apple Tart>', '<Recipe: Maple>'],
            ordered=False
        )
