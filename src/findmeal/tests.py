import datetime

from django.test import TestCase
from .models import Recipe, RecipeStep, RecipeIngredient, Ingredient, IngredientType

class ModelTests(TestCase):
    def setUp(self):
        # Create two ingredient types
        self.fruit = IngredientType.objects.create(name='fruit')
        self.vegetable = IngredientType.objects.create(name='vegetable')

        # Create four ingredients
        self.apple = Ingredient.objects.create(type=self.fruit, name='Apple')
        self.grape = Ingredient.objects.create(type=self.fruit, name='Grape')
        self.tomato = Ingredient.objects.create(type=self.vegetable, name='Tomato')
        self.spinach = Ingredient.objects.create(type=self.vegetable, name='Spinach')

        # Create two recipes
        self.apple_tart = Recipe.objects.create(
            name='Apple Tart',
            prep_time = datetime.timedelta(seconds=5400),
            serving = 4,
            calorie = 1000
        )
        self.maple = Recipe.objects.create(
            name='Maple',
            prep_time = datetime.timedelta(seconds=7200),
            serving = 2,
            calorie = 750
        )

        # Create recipe steps
        self.step1_apple_tart = RecipeStep.objects.create(recipe=self.apple_tart, instructions="Step 1")
        self.step2_apple_tart = RecipeStep.objects.create(recipe=self.apple_tart, instructions="Step 2")
        self.step1_maple = RecipeStep.objects.create(recipe=self.maple, instructions="Step 1")
        self.step2_maple = RecipeStep.objects.create(recipe=self.maple, instructions="Step 2")

        # Create recipe ingredients
        self.apple_apple_tart = RecipeIngredient.objects.create(recipe=self.apple_tart, ingredient=self.apple, amount=1)
        self.grape_apple_tart = RecipeIngredient.objects.create(recipe=self.apple_tart, ingredient=self.grape, amount=2)
        self.grape_maple = RecipeIngredient.objects.create(recipe=self.maple, ingredient=self.grape, amount=1)
        self.tomato_maple = RecipeIngredient.objects.create(recipe=self.maple, ingredient=self.tomato, amount=1)
        self.spinach_maple = RecipeIngredient.objects.create(recipe=self.maple, ingredient=self.spinach, amount=3)

    def test_find_recipe_with_distinct_ingredient(self):
        r = RecipeIngredient.objects.get(ingredient=self.apple)
        self.assertEqual(self.apple_tart, r.recipe)

    def test_find_recipe_with_non_distinct_ingredient(self):
        r = RecipeIngredient.objects.filter(ingredient=self.grape)
        self.assertEqual([self.apple_tart, self.maple], [q.recipe for q in r])

    def test_str_representations(self):
        self.assertEqual(self.apple.__str__(), self.apple.name)
        self.assertEqual(self.fruit.__str__(), self.fruit.name)
        self.assertEqual(self.apple_tart.__str__(), self.apple_tart.name)
        self.assertEqual(self.step1_apple_tart.__str__(), self.step1_apple_tart.recipe.name)
        self.assertEqual(self.apple_apple_tart.__str__(), self.apple_apple_tart.recipe.name)

    def test_display_prep_time(self):
        case_one = Recipe(prep_time=datetime.timedelta(seconds=5400))
        case_two = Recipe(prep_time=datetime.timedelta(seconds=7200))
        case_three = Recipe(prep_time=datetime.timedelta(seconds=2700))

        self.assertEqual(case_one.display_prep_time(), '1 saat 30 dakika')
        self.assertEqual(case_two.display_prep_time(), '2 saat')
        self.assertEqual(case_three.display_prep_time(), '45 dakika')
