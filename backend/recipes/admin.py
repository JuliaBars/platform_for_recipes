from django.contrib import admin
from django.contrib.auth.models import Group

from recipes.models import (Ingredient, FavouriteRecipe, Recipe,
                     RecipeIngredient, ShoppingCart, Tag)

from users.models import Subscription


admin.site.unregister(Group)


class RecipeIngredientAdmin(admin.StackedInline):
    model = RecipeIngredient
    autocomplete_fields = ('ingredient',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'get_author', 'name', 'text',
        'cooking_time', 'get_tags', 'get_ingredients',
        'get_favorite_count')
    search_fields = (
        'name', 'cooking_time',
        'author__email', 'ingredients__name')
    list_filter = ('tags',)
    inlines = (RecipeIngredientAdmin,)

    @admin.display(description='Email автора')
    def get_author(self, obj):
        return obj.author.email

    @admin.display(description='Теги')
    def get_tags(self, obj):
        return ', '.join([tag.name for tag in obj.tags.all()])

    @admin.display(description='Ингредиенты')
    def get_ingredients(self, obj):
        return ', '.join(
            [ingredient.name for ingredient in obj.ingredients.all()]
        )

    @admin.display(description='Количество избранных')
    def get_favorite_count(self, obj):
        return obj.favorite_recipe.count()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    search_fields = ('name',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_subscriber', 'get_author')
    search_fields = ('subscriber__email', 'author__email')

    @admin.display(description='Email подписчика')
    def get_subscriber(self, obj):
        return obj.subscriber.email

    @admin.display(description='Email автора')
    def get_author(self, obj):
        return obj.author.email


@admin.register(FavouriteRecipe)
class FavouriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user', 'get_recipe', 'get_favorite_count')
    search_fields = ('user__email', 'recipe__name')

    @admin.display(description='Email пользователя')
    def get_user(self, obj):
        return obj.user.email

    @admin.display(description='Название рецепта')
    def get_recipe(self, obj):
        return [
            f'{item["name"]} ' for item in obj.recipe.values('name')[:5]]

    @admin.display(description='Количество избранных')
    def get_favorite_count(self, obj):
        return obj.recipe.favorite_recipe.count()


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user', 'get_recipe', 'get_count')
    search_fields = ('user__email', 'recipe__name')

    @admin.display(description='Email пользователя')
    def get_user(self, obj):
        return obj.user.email

    @admin.display(description='Название рецепта')
    def get_recipe(self, obj):
        return [
            f'{item["name"]} ' for item in obj.recipe.values('name')[:5]]

    @admin.display(description='Количество рецептов')
    def get_count(self, obj):
        return obj.recipe.count()
