from django.test import TestCase
from .models import Recipe, RecipeStep, RecipeIngredient, Ingredient, IngredientType
# Create your tests here.

class IngTest(TestCase):
    def setUp(self):
        # Create two ingredient types
        self.fruit = IngredientType.objects.create(name='fruit')
        self.vegetable = IngredientType.objects.create(name='vegetable')

        #Create nine ingredients
        self.apple = Ingredient.objects.create(type=self.fruit, name='Apple')
        self.grape = Ingredient.objects.create(type=self.fruit, name='Grape')
        self.melon = Ingredient.objects.create(type=self.fruit, name='Melom')
        self.blueberry = Ingredient.objects.create(type=self.fruit, name='Blueberry')
        self.tomato = Ingredient.objects.create(type=self.vegetable, name='Tomato')
        self.spinach = Ingredient.objects.create(type=self.vegetable, name='Spinach')
        self.onion = Ingredient.objects.create(type=self.vegetable, name='Onion')
        self.garlic = Ingredient.objects.create(type=self.vegetable, name='Garlic')
        self.rosemary = Ingredient.objects.create(type=self.vegetable, name='rosemary')

        #Create three recipes
        self.appleTart = Recipe.objects.create(name='Apple Tart')
        self.maple = Recipe.objects.create(name='Maple')
        self.tupple = Recipe.objects.create(name='Tupple')

        self.step1 = RecipeStep.objects.create(recipe=self.appleTart, instructions="AAA")
        self.step2 = RecipeStep.objects.create(recipe=self.appleTart, instructions="AAA")
        self.step3 = RecipeStep.objects.create(recipe=self.appleTart, instructions="AAA")
        self.step4 = RecipeStep.objects.create(recipe=self.maple, instructions="AAA")
        self.step5 = RecipeStep.objects.create(recipe=self.maple, instructions="AAA")
        self.step6 = RecipeStep.objects.create(recipe=self.maple, instructions="AAA")
        self.step7 = RecipeStep.objects.create(recipe=self.tupple, instructions="AAA")
        self.step8 = RecipeStep.objects.create(recipe=self.tupple, instructions="AAA")
        self.step9 = RecipeStep.objects.create(recipe=self.tupple, instructions="AAA")

        # Create recipe step ingredients
        RecipeIngredient.objects.create(recipe=self.appleTart, ingredient=self.apple, step=self.step1, amount_required=1)
        RecipeIngredient.objects.create(recipe=self.appleTart, ingredient=self.grape, step=self.step2, amount_required=1)
        RecipeIngredient.objects.create(recipe=self.appleTart, ingredient=self.blueberry, step=self.step3, amount_required=1)
        RecipeIngredient.objects.create(recipe=self.maple, ingredient=self.apple, step=self.step4, amount_required=1)
        RecipeIngredient.objects.create(recipe=self.maple, ingredient=self.melon, step=self.step5, amount_required=1)
        RecipeIngredient.objects.create(recipe=self.maple, ingredient=self.tomato, step=self.step6, amount_required=1)
        RecipeIngredient.objects.create(recipe=self.tupple, ingredient=self.onion, step=self.step7, amount_required=1)
        RecipeIngredient.objects.create(recipe=self.tupple, ingredient=self.garlic, step=self.step8, amount_required=1)
        RecipeIngredient.objects.create(recipe=self.tupple, ingredient=self.tomato, step=self.step9, amount_required=1)

    def test_find_recipe_with_distinct_ingredient(self):
        o = RecipeIngredient.objects.get(ingredient=self.melon)
        self.assertEqual(self.maple, o.recipe)

    def test_find_recipe_with_non_distinct_ingredient(self):
        step_ingredients = RecipeIngredient.objects.filter(ingredient=self.tomato)
        self.assertEqual([self.maple, self.tupple], [s.recipe for s in step_ingredients])
