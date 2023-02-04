from .pagination import CustomPagination
from .serializers import CustomUserSerializer, SubscribeSerializer
from rest_framework import filters
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from users.models import Subscription
from datetime import datetime

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (FavouriteRecipe, Ingredient, RecipeIngredient, Recipe,
                            ShoppingCart, Tag)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .filters import IngredientFilter, RecipeFilter
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (FavouriteSerializer, IngredientSerializer,
                          RecipeBaseSerializer, RecipeReadSerializer, RecipeWriteSerializer, ShoppingCartSerializer, TagSerializer)

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = PageNumberPagination

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,),
        serializer_class=SubscribeSerializer
    )
    def subscribe(self, request, **kwargs):
        """Подписка на автора рецептов """
        user = request.user
        author_id = self.kwargs.get('id')
        author = get_object_or_404(User, id=author_id)

        serializer = self.get_serializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            if request.method == 'POST':
                Subscription.objects.get_or_create(
                    subscriber=user, author=author)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                Subscription.objects.filter(
                    subscriber=user, author=author).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        """Получение списка подписок пользователя

        :param request: запрос
        :return: список подписок пользователя
        :raise: 404 если пользователь не найден
        :raise: 403 если пользователь не авторизован
        :permission: Аутентифицированный пользователь

        """
        user = request.user
        queryset = User.objects.filter(following__subscriber=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(pages,
                                         many=True,
                                         context={'request': request})
        return self.get_paginated_response(serializer.data)


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = IngredientFilter
    search_fields = ('^name',)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = CustomPagination
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.add_to(FavouriteRecipe, request.user, pk)
        else:
            return self.delete_from(FavouriteRecipe, request.user, pk)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.add_to(ShoppingCart, request.user, pk)
        else:
            return self.delete_from(ShoppingCart, request.user, pk)

    def add_to(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response({'errors': 'Рецепт уже добавлен!'},
                            status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeBaseSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_from(self, model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Рецепт уже удален!'},
                        status=status.HTTP_400_BAD_REQUEST)
