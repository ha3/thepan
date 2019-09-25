from .models import Recipe
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
