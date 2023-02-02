# from django.contrib.auth import get_user_model
# from django.db import transaction
# from django.db.models import F
# from django.shortcuts import get_object_or_404
# from djoser.serializers import UserCreateSerializer, UserSerializer
# from drf_extra_fields.fields import Base64ImageField
# from recipes.models import Ingredient, IngredientInRecipe, Recipe, Tag
# from rest_framework import status
# from rest_framework.exceptions import ValidationError
# from rest_framework.fields import IntegerField, SerializerMethodField
# from rest_framework.relations import PrimaryKeyRelatedField
# from rest_framework.serializers import ModelSerializer
# from users.models import Subscribe

# User = get_user_model()


# class IngredientSerializer(ModelSerializer):
#     class Meta:
#         model = Ingredient
#         fields = ('id', 'name', 'measurement_unit')


# class TagSerializer(ModelSerializer):
#     class Meta:
#         model = Tag
#         fields = ('id', 'name', 'color', 'slug')


# class RecipeIngredientSerializer(ModelSerializer):
#     id = IntegerField(write_only=True)
#     name = SerializerMethodField()
#     measurement_unit = SerializerMethodField()

#     class Meta:
#         model = IngredientInRecipe
#         fields = ('id', 'name', 'measurement_unit', 'amount')

#     def get_name(self, obj):
#         return obj.ingredient.name

#     def get_measurement_unit(self, obj):
#         return obj.ingredient.measurement_unit


# class RecipeSerializer(ModelSerializer):
#     image = Base64ImageField(required=False)
#     tags = PrimaryKeyRelatedField(
#         many=True,
#         queryset=Tag.objects.all(),
#         required=False
#     )
#     ingredients = RecipeIngredientSerializer(many=True, required=False)

#     class Meta:
#         model = Recipe
#         fields = '__all__'

#     def validate_ingredients(self, ingredients):
#         if not ingredients:
#             raise ValidationError(
#                 'Необходимо указать ингредиенты')
#         return ingredients

#     def validate_tags(self, tags):
#         if not tags:
#             raise ValidationError(
#                 'Необходимо указать теги')
#         return tags

#     @transaction.atomic
#     def create(self, validated_data):
#         ingredients_data = validated_data.pop('ingredients')
#         recipe = Recipe.objects.create(**validated_data)
#         for ingredient_data in ingredients_data:
#             IngredientInRecipe.objects.create(
#                 recipe=recipe,
#                 ingredient_id=ingredient_data['id'],
#                 amount=ingredient_data['amount']
#             )
#         return recipe

#     @transaction.atomic
#     def update(self, instance, validated_data):
#         ingredients_data = validated_data.pop('ingredients')
#         for ingredient_data in ingredients_data:
#             ingredient = get_object_or_404(
#                 IngredientInRecipe,
#                 recipe=instance,
#                 ingredient_id=ingredient_data['id']
#             )
#             ingredient.amount = ingredient_data['amount']
#             ingredient.save()
#         return super().update(instance, validated_data)
