from django.contrib import admin
from django.contrib.auth.models import Group
from recipes.models import (FavouriteRecipe, Ingredient, Recipe,
                            RecipeIngredient, ShoppingCart, Tag)

admin.site.unregister(Group)


class RecipeIngredientAdmin(admin.StackedInline):
    model = RecipeIngredient
    autocomplete_fields = ('ingredient',)
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'get_author', 'name', 'text',
        'cooking_time', 'get_tags', 'get_ingredients', 'get_favorite_count')
    search_fields = (
        'name', 'cooking_time', 'tags__name',
        'author__email', 'ingredients__name')
    list_filter = ('tags', 'author', 'name')
    inlines = (RecipeIngredientAdmin,)

    @admin.display(description='Автор')
    def get_author(self, obj):
        return obj.author.username

    @admin.display(description='Теги')
    def get_tags(self, obj):
        return ', '.join([tag.name for tag in obj.tags.all()])

    @admin.display(description='Ингредиенты')
    def get_ingredients(self, obj):
        return ', '.join(
            [ingredient.name for ingredient in obj.ingredients.all()]
        )

    @admin.display(description='Количество в избранных')
    def get_favorite_count(self, obj):
        return obj.favorite_recipes.count()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    search_fields = ('name',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(FavouriteRecipe)
class FavouriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_recipe', 'date', 'get_user')
    search_fields = ('user__email', 'recipe__name')

    @admin.display(description='Email пользователя')
    def get_user(self, obj):
        return obj.user.email

    @admin.display(description='Название рецепта')
    def get_recipe(self, obj):
        return obj.recipe.name

    @admin.display(description='Дата создания')
    def date(self, obj):
        return obj.recipe.created_at


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_recipe', 'get_user', )
    search_fields = ('user__email', 'recipe__name')

    @admin.display(description='Email пользователя')
    def get_user(self, obj):
        return obj.user.email

    @admin.display(description='Название рецепта')
    def get_recipe(self, obj):
        return obj.recipe.name

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user=request.user)
