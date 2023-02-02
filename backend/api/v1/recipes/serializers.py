from datetime import datetime

from django.db.models import Sum
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from recipes.models import Ingredient, RecipeIngredient, Recipe, Tag
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.fields import IntegerField, SerializerMethodField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer
from api.v1.users.serializers import CustomUserSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

User = get_user_model()


# # на стороне пользователя ингредиент должен описываться такими полями:
# Название.
# Количество.
# Единицы измерения.
# Все поля обязательны для заполнения.

class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')

# Рецепт
# Рецепт должен описываться такими полями:
# Автор публикации (пользователь).
# Название.
# Картинка.
# Текстовое описание.
# Ингредиенты: продукты для приготовления блюда по рецепту. Множественное поле, выбор из предустановленного списка, с указанием количества и единицы измерения.
# Тег (можно установить несколько тегов на один рецепт, выбор из предустановленных).
# Время приготовления в минутах.
# Все поля обязательны для заполнения.


class RecipeIngredientSerializer(ModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = ('ingredient', 'amount')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['ingredient'] = IngredientSerializer(instance.ingredient).data
        return data


class RecipeSerializer(ModelSerializer):
    tags = PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=True,
    )
    author = CustomUserSerializer(
        read_only=True,
    )
    ingredients = PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        many=True,
        required=True,
    )
    image = Base64ImageField(
        required=False,
    )
    is_favorite = SerializerMethodField(read_only=True)
    is_in_shopping_cart = SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorite',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_ingredients(self, obj):
        recipe = obj
        ingredients = recipe.ingredients.values(
            'id',
            'name',
            'measurement_unit',
            amount=F('ingredientinrecipe__amount')
        )
        return ingredients

    def get_is_favorite(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorite_recipes.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.shopping_cart.filter(recipe=obj).exists()

    def download_shopping_cart(self, request):
        user = request.user
        if not user.shopping_cart.exists():
            return Response(status=HTTP_400_BAD_REQUEST)

        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))

        today = datetime.today()
        shopping_list = (
            f'Список покупок для: {user.get_full_name()}\n\n'
            f'Дата: {today:%Y-%m-%d}\n\n'
        )
        shopping_list += '\n'.join([
            f'- {ingredient["ingredient__name"]} '
            f'({ingredient["ingredient__measurement_unit"]})'
            f' - {ingredient["amount"]}'
            for ingredient in ingredients
        ])
        shopping_list += f'\n\nFoodgram ({today:%Y})'

        filename = f'{user.username}_shopping_list.txt'
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response



class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')




class RecipeBaseSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class ShoppingCartSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['ingredients'] = RecipeIngredientSerializer(
            instance.ingredients.all(),
            many=True,
        ).data
        return data

class FavouriteSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

    

