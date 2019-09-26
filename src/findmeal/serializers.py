from .models import Recipe, Ingredient
from rest_framework import serializers

class IngredientSerializer(serializers.RelatedField):
    def to_representation(self, value):
        i = {}
        i['name'] = value.ingredient.name
        i['amount'] = value.amount
        return i


class DetailViewSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)

    steps = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='instructions'
    )

    class Meta:
        model = Recipe
        fields = '__all__'


class ListRecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'slug', 'image', 'prep_time', 'serving', 'calorie']


class ListIngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']


class RateRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['rating']

    def update(self, instance, validated_data):
        rating = int(validated_data.get('rating'))
        instance.rating = (instance.rating * instance.rate_count + rating) / (instance.rate_count + 1)
        instance.rate_count += 1
        instance.save()

        return instance
